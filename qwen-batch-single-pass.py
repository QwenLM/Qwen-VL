import os
import re
import shutil
import torch
import time
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

# Function to check for unwanted elements in the caption
def has_unwanted_elements(caption):
    patterns = [r'<ref>.*?</ref>', r'<box>.*?</box>', r'\[\d+\]', r'\(\[\d+\]\)']
    return any(re.search(pattern, caption) for pattern in patterns)

# Function to clean up the caption
def clean_caption(caption):
    caption = re.sub(r'<ref>(.*?)</ref>', r'\1', caption)
    caption = re.sub(r'<box>.*?</box>', '', caption)
    return caption.strip()

# Directory containing the images
image_directory = '/path/to/img_dir/here'

# Supported image types
image_types = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

# Initialize the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL", device_map="cuda", trust_remote_code=True).eval()

# First pass with initial seed
torch.manual_seed(1234)
files = [f for f in os.listdir(image_directory) if os.path.splitext(f)[1].lower() in image_types]

# Initialize tqdm with custom settings
pbar = tqdm(total=len(files), desc="Captioning", dynamic_ncols=True, position=0, leave=True)
start_time = time.time()

print("Captioning phase:")
for i in range(len(files)):
    filename = files[i]
    image_path = os.path.join(image_directory, filename)
    
    query = tokenizer.from_list_format([
        {'image': image_path},
        {'text': 'describe this image in detail, as if you are an art critic.'},
    ])
    
    response, _ = model.chat(tokenizer, query=query, history=None)
    
    # If the caption has unwanted elements, clean it up
    if has_unwanted_elements(response):
        response = clean_caption(response)
    
    # Save the cleaned caption to a text file in the main directory
    txt_filename = os.path.splitext(filename)[0] + '.txt'
    txt_path = os.path.join(image_directory, txt_filename)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(response)

    elapsed_time = time.time() - start_time
    images_per_sec = (i + 1) / elapsed_time
    estimated_time_remaining = (len(files) - i - 1) / images_per_sec

    pbar.set_postfix({"Time Elapsed": f"{elapsed_time:.2f}s", "ETA": f"{estimated_time_remaining:.2f}s", "Speed": f"{images_per_sec:.2f} img/s"})
    pbar.update(1)

pbar.close()