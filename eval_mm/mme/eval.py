import os
from tqdm import tqdm

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

checkpoint = 'Qwen/Qwen-VL-Chat'
tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    checkpoint, device_map='cuda', trust_remote_code=True).eval()

model.generation_config = GenerationConfig.from_pretrained(checkpoint, trust_remote_code=True)
model.generation_config.top_p = 0.01


root = 'Your_Results'
output = 'Qwen-VL-Chat'
os.makedirs(output, exist_ok=True)
for filename in os.listdir(root):
    with open(os.path.join(root, filename), 'r') as fin, open(os.path.join(output, filename), 'w') as fout:
        lines = fin.read().splitlines()
        filename = filename.replace('.txt', '')
        for line in tqdm(lines):
            img, question, gt = line.strip().split('\t')
            img_path = os.path.join('images', filename, img)
            assert os.path.exists(img_path), img_path
            query = f'<img>{img_path}</img>\n{question}'
            response, _ = model.chat(tokenizer, query=query, history=None)

            print(img, question, gt, response, sep='\t', file=fout)
