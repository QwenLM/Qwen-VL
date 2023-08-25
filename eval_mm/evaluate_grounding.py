import argparse
import itertools
import json
import os
import re
from functools import partial

import torch
from torchvision.ops.boxes import box_area
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

ds_collections = {
    'refcoco_val': 'data/refcoco/refcoco_val.jsonl',
    'refcoco_testA': 'data/refcoco/refcoco_testA.jsonl',
    'refcoco_testB': 'data/refcoco/refcoco_testB.jsonl',
    'refcoco+_val': 'data/refcoco+/refcoco+_val.jsonl',
    'refcoco+_testA': 'data/refcoco+/refcoco+_testA.jsonl',
    'refcoco+_testB': 'data/refcoco+/refcoco+_testB.jsonl',
    'refcocog_val': 'data/refcocog/refcocog_val.jsonl',
    'refcocog_test': 'data/refcocog/refcocog_test.jsonl',
}


def box_iou(boxes1, boxes2):
    area1 = box_area(boxes1)
    area2 = box_area(boxes2)

    lt = torch.max(boxes1[:, None, :2], boxes2[:, :2])  # [N,M,2]
    rb = torch.min(boxes1[:, None, 2:], boxes2[:, 2:])  # [N,M,2]

    wh = (rb - lt).clamp(min=0)  # [N,M,2]
    inter = wh[:, :, 0] * wh[:, :, 1]  # [N,M]

    union = area1[:, None] + area2 - inter

    iou = inter / union
    return iou, union


def collate_fn(batches, tokenizer):

    texts = [_['text'] for _ in batches]
    bboxes = [_['bbox'] for _ in batches]
    hws = [_['hw'] for _ in batches]

    input_ids = tokenizer(texts, return_tensors='pt', padding='longest')

    return input_ids.input_ids, input_ids.attention_mask, bboxes, hws


class RefCOCODataset(torch.utils.data.Dataset):

    def __init__(self, test, tokenizer, prompt):
        self.datas = open(test).readlines()
        self.tokenizer = tokenizer
        self.prompt = prompt

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):
        data = json.loads(self.datas[idx].strip())
        image = data['image']
        text = data['sent']
        bbox = data['bbox']

        w, h = data['width'], data['height']

        return {
            'text': self.prompt.format(image, text),
            'bbox': bbox,
            'hw': (h, w),
        }


class InferenceSampler(torch.utils.data.sampler.Sampler):

    def __init__(self, size):
        self._size = int(size)
        assert size > 0
        self._rank = torch.distributed.get_rank()
        self._world_size = torch.distributed.get_world_size()
        self._local_indices = self._get_local_indices(size, self._world_size,
                                                      self._rank)

    @staticmethod
    def _get_local_indices(total_size, world_size, rank):
        shard_size = total_size // world_size
        left = total_size % world_size
        shard_sizes = [shard_size + int(r < left) for r in range(world_size)]

        begin = sum(shard_sizes[:rank])
        end = min(sum(shard_sizes[:rank + 1]), total_size)
        return range(begin, end)

    def __iter__(self):
        yield from self._local_indices

    def __len__(self):
        return len(self._local_indices)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, default='')
    parser.add_argument('--dataset', type=str, default='')
    parser.add_argument('--batch-size', type=int, default=1)
    parser.add_argument('--num-workers', type=int, default=1)
    args = parser.parse_args()

    torch.distributed.init_process_group(
        backend='nccl',
        world_size=int(os.getenv('WORLD_SIZE', '1')),
        rank=int(os.getenv('RANK', '0')),
    )

    torch.cuda.set_device(int(os.getenv('LOCAL_RANK', 0)))

    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint, device_map='cuda', trust_remote_code=True).eval()

    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint,
                                              trust_remote_code=True)
    tokenizer.padding_side = 'left'
    tokenizer.pad_token_id = tokenizer.eod_id

    prompt = '<img>{}</img><ref>{}</ref><box>'

    dataset = RefCOCODataset(test=ds_collections[args.dataset],
                             tokenizer=tokenizer,
                             prompt=prompt)

    dataloader = torch.utils.data.DataLoader(
        dataset=dataset,
        sampler=InferenceSampler(len(dataset)),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=True,
        drop_last=True,
        collate_fn=partial(collate_fn, tokenizer=tokenizer),
    )

    outputs = []
    for _, (input_ids, attention_mask, bboxes,
            hws) in tqdm(enumerate(dataloader)):
        pred = model.generate(
            input_ids=input_ids.cuda(),
            attention_mask=attention_mask.cuda(),
            do_sample=False,
            num_beams=1,
            max_new_tokens=28,
            min_new_tokens=10,
            length_penalty=1,
            num_return_sequences=1,
            use_cache=True,
            pad_token_id=tokenizer.eod_id,
            eos_token_id=tokenizer.eod_id,
        )
        answers = [
            tokenizer.decode(_[input_ids.size(1):].cpu(),
                             skip_special_tokens=True) for _ in pred
        ]

        for bbox, hw, answer in zip(bboxes, hws, answers):
            outputs.append({
                'answer': answer,
                'gt_bbox': bbox,
                'hw': hw,
            })

    torch.distributed.barrier()

    world_size = torch.distributed.get_world_size()
    merged_outputs = [None for _ in range(world_size)]
    torch.distributed.all_gather_object(merged_outputs, outputs)

    merged_outputs = [_ for _ in itertools.chain.from_iterable(merged_outputs)]
    PATTERN = re.compile(r'\((.*?)\),\((.*?)\)')

    if torch.distributed.get_rank() == 0:
        correct = total_cnt = 0
        for i, output in enumerate(merged_outputs):
            predict_bbox = re.findall(PATTERN, output['answer'])
            try:
                if ',' not in predict_bbox[0][0] or ',' not in predict_bbox[0][
                        1]:
                    predict_bbox = (0., 0., 0., 0.)
                else:
                    x1, y1 = [
                        float(tmp) for tmp in predict_bbox[0][0].split(',')
                    ]
                    x2, y2 = [
                        float(tmp) for tmp in predict_bbox[0][1].split(',')
                    ]
                    predict_bbox = (x1, y1, x2, y2)
            except:
                predict_bbox = (0., 0., 0., 0.)
            target_bbox = torch.tensor(output['gt_bbox'],
                                       dtype=torch.float32).view(-1, 4)
            predict_bbox = torch.tensor(predict_bbox,
                                        dtype=torch.float32).view(-1, 4) / 999
            predict_bbox[:, 0::2] *= output['hw'][1]
            predict_bbox[:, 1::2] *= output['hw'][0]
            iou, _ = box_iou(predict_bbox, target_bbox)
            iou = iou.item()
            total_cnt += 1
            if iou >= 0.5:
                correct += 1

        print(f"Evaluating {args.dataset} ...")
        print(f'Precision @ 1: {correct / total_cnt} \n')
    torch.distributed.barrier()
