import argparse
import itertools
import json
import os
from functools import partial

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig


def collate_fn(batches, pad_token_id):

    input_tokens = [_['input_tokens'] for _ in batches]
    target_lengths = [_['target_lengths'] for _ in batches]
    answers = [_['answer'] for _ in batches]
    question_id = [_['question_id'] for _ in batches]

    chunk_sizes = [len(_) for _ in input_tokens]

    input_tokens = [_ for _ in itertools.chain.from_iterable(input_tokens)]

    max_lengths = max([len(_) for _ in input_tokens])
    input_tokens = [[pad_token_id] * (max_lengths - len(_)) + _
                    for _ in input_tokens]
    input_tokens = torch.LongTensor(input_tokens)

    attention_mask = 1 - input_tokens.eq(pad_token_id).float()

    return input_tokens, attention_mask, target_lengths, answers, chunk_sizes, question_id


class MultipleChoiceDataste(torch.utils.data.Dataset):

    def __init__(self, test, tokenizer):
        self.datas = []
        with open(test) as fin:
            for line in tqdm(fin):
                self.datas.append(json.loads(line.strip()))
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):

        data = self.datas[idx]
        prompt = data['prompt']

        prompt_tokens = self.tokenizer(prompt).input_ids
        target_tokens = [
            self.tokenizer(' ' + _).input_ids
            for _ in ['A', 'B', 'C', 'D']
        ]

        return {
            'input_tokens': [prompt_tokens + _ for _ in target_tokens],
            'target_lengths': [len(_) for _ in target_tokens],
            'answer': data['answer'],
            'question_id': data['question_id'],
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
    model.generation_config = GenerationConfig.from_pretrained(args.checkpoint, trust_remote_code=True)
    model.generation_config.top_p = 0.01

    dataset = MultipleChoiceDataste(test=args.dataset, tokenizer=tokenizer)
    dataloader = torch.utils.data.DataLoader(
        dataset=dataset,
        # sampler=InferenceSampler(1000),
        sampler=InferenceSampler(len(dataset)),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=True,
        drop_last=False,
        collate_fn=partial(collate_fn, pad_token_id=tokenizer.eod_id),
    )

    results = []
    fout = open('result_{}.jsonl'.format(torch.distributed.get_rank()), 'w')
    with torch.no_grad():
        for _, (input_tokens, attention_mask, target_lengths, answers,
                chunk_sizes, question_ids) in tqdm(enumerate(dataloader)):

            outputs = model(
                input_ids=input_tokens[:, :-1].cuda(),
                attention_mask=attention_mask[:, :-1].cuda(),
                return_dict=True,
            )
            losses = torch.nn.functional.cross_entropy(outputs.logits.permute(
                0, 2, 1),
                                                       input_tokens[:,
                                                                    1:].cuda(),
                                                       reduction='none')

            losses = losses.split(chunk_sizes, dim=0)

            for loss, target_length, answer, question_id in zip(losses, target_lengths,
                                                   answers, question_ids):

                target_loss = loss.mean(-1)
                for _ in range(len(target_length)):
                    target_loss[_] = loss[_, -target_length[_]:].mean()
                pred = target_loss.argmin().item()
                pred = chr(pred + 65)
                if pred == answer:
                    results.append(1)
                else:
                    results.append(0)
                answer_record = {
                    'question_id': question_id,
                    'prediction': pred
                }
                print(json.dumps(answer_record), file=fout)
    fout.close()

    torch.distributed.barrier()

    world_size = torch.distributed.get_world_size()
    merged_results = [None for _ in range(world_size)]
    torch.distributed.all_gather_object(merged_results, results)

    merged_results = [_ for _ in itertools.chain.from_iterable(merged_results)]

    if torch.distributed.get_rank() == 0:
        print(f"Evaluating {args.dataset} ...")
        print(f'Acc@1: {sum(merged_results) / len(merged_results)}')

    torch.distributed.barrier()
