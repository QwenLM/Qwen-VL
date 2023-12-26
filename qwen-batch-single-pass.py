import os
import re
import torch
import time
import argparse
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

# Argument Parsing
parser = argparse.ArgumentParser(description='Image Captioning Script')
parser.add_argument('--imgdir', type=str, default='path/to/img/dir', help='Directory containing images')
parser.add_argument('--exist', type=str, default='replace', choices=['skip', 'add', 'replace'], help='Handling of existing captions')
parser.add_argument('--prompt', type=str, default='describe this image in detail, in less than 35 words', help='Prompt to use for image captioning')
args = parser.parse_args()

# Function to check for unwanted elements in the caption
def has_unwanted_elements(caption):
    patterns = [r'<ref>.*?</ref>', r'<box>.*?</box>']
    return any(re.search(pattern, caption) for pattern in patterns)

# Function to clean up the caption
def clean_caption(caption):
    caption = re.sub(r'<ref>(.*?)</ref>', r'\1', caption)
    caption = re.sub(r'<box>.*?</box>', '', caption)
    return caption.strip()

# Supported image types
image_types = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

# Initialize the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat-Int4", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat-Int4", device_map="cuda", trust_remote_code=True, use_flash_attn=True).eval()

# Get the list of image files in the specified directory
files = [f for f in os.listdir(args.imgdir) if os.path.splitext(f)[1].lower() in image_types]

# Initialize the progress bar
pbar = tqdm(total=len(files), desc="Captioning", dynamic_ncols=True, position=0, leave=True)
start_time = time.time()

print("Captioning phase:")
for i in range(len(files)):
    filename = files[i]
    image_path = os.path.join(args.imgdir, filename)

    # Handle based on the argument 'exist'
    txt_filename = os.path.splitext(filename)[0] + '.txt'
    txt_path = os.path.join(args.imgdir, txt_filename)
    
    if args.exist == 'skip' and os.path.exists(txt_path):
        pbar.update(1)
        continue
    elif args.exist == 'add' and os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # Generate the caption using the model
    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': args.prompt},
    ])
    response, _ = model.chat(tokenizer, query=query, history=None)

    # Clean up the caption if necessary
    if has_unwanted_elements(response):
        response = clean_caption(response)
    
    # Write the caption to the corresponding .txt file
    with open(txt_path, 'w', encoding='utf-8') as f:
        if args.exist == 'add' and os.path.exists(txt_path):
            f.write(existing_content + "\n" + response)
        else:
            f.write(response)

    # Update progress bar with some additional information about the process
    elapsed_time = time.time() - start_time
    images_per_sec = (i + 1) / elapsed_time
    estimated_time_remaining = (len(files) - i - 1) / images_per_sec
    pbar.set_postfix({"Time Elapsed": f"{elapsed_time:.2f}s", "ETA": f"{estimated_time_remaining:.2f}s", "Speed": f"{images_per_sec:.2f} img/s"})
    pbar.update(1)

pbar.close()