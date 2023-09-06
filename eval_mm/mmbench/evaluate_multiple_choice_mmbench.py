import argparse
import itertools
import json
import os
from functools import partial

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

multiple_choices = ['A', 'B', 'C', 'D', 'E']

ds_collections = {
    'mmbench_dev_20230712': {
        'test': 'data/mmbench/mmbench_dev_20230712/mmbench_dev_20230712.jsonl',
    },
    'mmbench_test_20230712': {
        'test': 'data/mmbench/mmbench_test_20230712/mmbench_test_20230712.jsonl',
    }
}

def collate_fn(batches, pad_token_id):

    indexes = [_['index'] for _ in batches]

    input_tokens = [_['input_tokens'] for _ in batches]
    target_lengths = [_['target_lengths'] for _ in batches]

    chunk_sizes = [len(_) for _ in input_tokens]

    input_tokens = [_ for _ in itertools.chain.from_iterable(input_tokens)]

    max_lengths = max([len(_) for _ in input_tokens])
    input_tokens = [[pad_token_id] * (max_lengths - len(_)) + _
                    for _ in input_tokens]
    input_tokens = torch.LongTensor(input_tokens)

    attention_mask = 1 - input_tokens.eq(pad_token_id).float()

    return input_tokens, attention_mask, target_lengths, chunk_sizes, indexes


class MultipleChoiceDataste(torch.utils.data.Dataset):

    def __init__(self, test, prompt, tokenizer):
        self.datas = open(test).readlines()
        self.prompt = prompt
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):

        data = json.loads(self.datas[idx].strip())
        index = data['index']
        image = data['image']
        hint = data['hint'] if data['hint'] else 'N/A'
        question = data['question']

        choices = data['choices']
        choice_list = []
        for i, c in enumerate(choices):
            choice_list.append('{}. {}'.format(multiple_choices[i], c))
        choice_txt = '\n'.join(choice_list)

        prompt = self.prompt.format(image, hint, question, choice_txt)

        prompt_tokens = self.tokenizer(prompt).input_ids
        target_tokens = [
            self.tokenizer(' ' + _).input_ids
            for _ in multiple_choices[:len(choices)]
        ]

        return {
            'index': index,
            'input_tokens': [prompt_tokens + _ for _ in target_tokens],
            'target_lengths': [len(_) for _ in target_tokens],
            # 'answer': data['answer'],
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

    prompt = '<img>{}</img>Context: {}\nQuestion: {}\nOptions: {}\nAnswer:'

    dataset = MultipleChoiceDataste(test=ds_collections[args.dataset]['test'],
                                    prompt=prompt,
                                    tokenizer=tokenizer)
    dataloader = torch.utils.data.DataLoader(
        dataset=dataset,
        sampler=InferenceSampler(len(dataset)),
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=True,
        drop_last=False,
        collate_fn=partial(collate_fn, pad_token_id=tokenizer.eod_id),
    )

    results = []
    with torch.no_grad():
        for _, (input_tokens, attention_mask, target_lengths,
                chunk_sizes, indexes) in tqdm(enumerate(dataloader)):

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

            for loss, target_length, index in zip(losses, target_lengths, indexes):

                target_loss = loss.mean(-1)
                for _ in range(len(target_length)):
                    target_loss[_] = loss[_, -target_length[_]:].mean()
                pred = target_loss.argmin().item()

                results.append({
                    "index": index,
                    "prediction": pred,
                })

    torch.distributed.barrier()

    world_size = torch.distributed.get_world_size()
    merged_results = [None for _ in range(world_size)]
    torch.distributed.all_gather_object(merged_results, results)

    merged_results = [_ for _ in itertools.chain.from_iterable(merged_results)]

    if torch.distributed.get_rank() == 0:
        json.dump(merged_results, open(f"{args.dataset}.json", "w"))

    torch.distributed.barrier()
