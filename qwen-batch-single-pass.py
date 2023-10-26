import os
import re
import torch
import time
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import argparse

def has_unwanted_elements(caption):
    patterns = [r'<ref>.*?</ref>', r'<box>.*?</box>']
    return any(re.search(pattern, caption) for pattern in patterns)

def clean_caption(caption):
    caption = re.sub(r'<ref>(.*?)</ref>', r'\1', caption)
    caption = re.sub(r'<box>.*?</box>', '', caption)
    return caption.strip()

# Argument parsing
parser = argparse.ArgumentParser(description='Image Captioning Script')
parser.add_argument('--imgdir', type=str, default='img/dir/here', help='Path to image directory')
parser.add_argument('--exist', type=str, choices=['skip', 'add', 'replace'], default='replace', help='Handling of existing txt files')
args = parser.parse_args()

image_directory = args.imgdir
image_types = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat-Int4", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat-Int4", device_map="cuda", trust_remote_code=True, use_flash_attn=True).eval()

files = [f for f in os.listdir(image_directory) if os.path.splitext(f)[1].lower() in image_types]

pbar = tqdm(total=len(files), desc="Captioning", dynamic_ncols=True, position=0, leave=True)
start_time = time.time()

print("Captioning phase:")
for i in range(len(files)):
    filename = files[i]
    image_path = os.path.join(image_directory, filename)

    # Check for existing txt file and handle based on the argument
    txt_filename = os.path.splitext(filename)[0] + '.txt'
    txt_path = os.path.join(image_directory, txt_filename)
    
    if args.exist == 'skip' and os.path.exists(txt_path):
        pbar.update(1)
        continue
    elif args.exist == 'add' and os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': 'describe this image in detail, as if you are an art critic in less than 35 words'},
    ])
    response, _ = model.chat(tokenizer, query=query, history=None)
    
    if has_unwanted_elements(response):
        response = clean_caption(response)
    
    with open(txt_path, 'w', encoding='utf-8') as f:
        if args.exist == 'add' and os.path.exists(txt_path):
            f.write(existing_content + "\n" + response)
        else:
            f.write(response)

    elapsed_time = time.time() - start_time
    images_per_sec = (i + 1) / elapsed_time
    estimated_time_remaining = (len(files) - i - 1) / images_per_sec

    pbar.set_postfix({"Time Elapsed": f"{elapsed_time:.2f}s", "ETA": f"{estimated_time_remaining:.2f}s", "Speed": f"{images_per_sec:.2f} img/s"})
    pbar.update(1)

pbar.close()
