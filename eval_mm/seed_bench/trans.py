import os
import av
import json

import torch
import numpy as np
from PIL import Image
from tqdm import tqdm
from decord import VideoReader, cpu

# path of SEED-Bench.json, download from https://huggingface.co/datasets/AILab-CVC/SEED-Bench/blob/main/SEED-Bench.json
seed_bench_input_path = 'SEED-Bench.json'
# root directory of evaluation dimension 1-9, following https://github.com/AILab-CVC/SEED-Bench/blob/main/DATASET.md
cc3m_dir = "/YOUR_PATH_TO/seed_bench_image"
# root directory of evaluation dimension 10
dimension10_dir = "/YOUR_PATH_TO/SSV2/videos"
# root directory of evaluation dimension 11
dimension11_dir = "/YOUR_PATH_TO/EPIC-KITCHENS/3h91syskeag572hl6tvuovwv4d/videos/test"
# root directory of evaluation dimension 12
dimension12_dir = "/YOUR_PATH_TO/BreakfastII_15fps_qvga_sync"

def is_integer_string(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def filter_questions(data, task='all'):
    if task == "image":
        return [q for q in data if 1 <= q["question_type_id"] <= 9]
    elif task == "video":
        return [q for q in data if 10 <= q["question_type_id"] <= 12]
    elif task == "all":
        return data
    elif is_integer_string(task):
        return [q for q in data if q["question_type_id"] == int(task)]
    else:
        raise ValueError(f"Invalid task: {task}")

def get_index(num_frames, num_segments):
    if num_segments > num_frames:
        offsets = np.array([
            idx for idx in range(num_frames)
        ])
    else:
        # uniform sampling
        seg_size = float(num_frames - 1) / num_segments
        start = int(seg_size / 2)
        offsets = np.array([
            start + int(np.round(seg_size * idx)) for idx in range(num_segments)
        ])
    return offsets

with open(seed_bench_input_path) as fin:
    qa_anno = json.load(fin)['questions']

fout = open('image_input.jsonl', 'w')
i_anno = filter_questions(qa_anno, 'image')
for qa_item in tqdm(i_anno):
    data_path = cc3m_dir + qa_item['data_id']
    choices = [qa_item['choice_a'], qa_item['choice_b'], qa_item['choice_c'], qa_item['choice_d']]
    choice_list = []
    for i, c in enumerate(choices):
        choice_list.append('{}. {}'.format(chr(i + 65), c))
    choice_txt = '\n'.join(choice_list)
    prompt = '<img>{}</img>\nQuestion: {}\nOptions: {}\nAnswer:'.format(
        data_path, qa_item['question'], choice_txt)
    print(json.dumps({
        'question_id': qa_item['question_id'],
        'prompt': prompt,
        'answer': qa_item['answer'],
    }), file=fout)
fout.close()

n_frames = 8
os.system('rm -rf video_input_' + str(n_frames))
os.makedirs('video_imgs_' + str(n_frames), exist_ok=True)

fout = open('video_input_{}.jsonl'.format(n_frames), 'w')
v_anno = filter_questions(qa_anno, 'video')
for qa_item in tqdm(v_anno):
    if qa_item['question_type_id'] == 12:
        data_path = dimension12_dir + qa_item['data_id']
    elif qa_item['question_type_id'] == 11:
        data_path = dimension11_dir + qa_item['data_id'].split('/')[-1]
    elif qa_item['question_type_id'] == 10:
        data_path = dimension10_dir + qa_item['data_id']
    else:
        assert False, str(qa_item)
    print(data_path)

    use_pyav = False
    if 'segment' in qa_item.keys():
        segment = qa_item['segment']
        if isinstance(segment[0], int):
            # using pyav for decoding videos in evaluation dimension 12
            use_pyav = True
        start, end = segment[0], segment[1]
    else:
        start = 0.0
        end = 0.0

    if use_pyav:
        # using pyav for decoding videos in evaluation dimension 12
        reader = av.open(data_path)
        frames = [torch.from_numpy(f.to_rgb().to_ndarray()) for f in reader.decode(video=0)]
        video_len = len(frames)
        start_frame, end_frame = start, end
        end_frame = min(end_frame, video_len)
        offset = get_index(end_frame - start_frame, n_frames)
        frame_indices = offset + start_frame
        images = torch.stack([frames[idx] for idx in frame_indices]).numpy()
    else:
        # using decord for decoding videos in evaluation dimension 10-11
        try:
            vr = VideoReader(data_path, num_threads=1, ctx=cpu(0))
            video_len = len(vr)
            fps = vr.get_avg_fps()
            if 'segment' in qa_item.keys():
                # obtain start and end frame for the video segment in evaluation dimension 11
                start_frame = int(min(max(start * fps, 0), video_len - 1))
                end_frame = int(min(max(end * fps, 0), video_len - 1))
                tot_frames = int(end_frame - start_frame)
                offset = get_index(tot_frames, n_frames)
                frame_indices = offset + start_frame
            else:
                # sample frames of the video in evaluation dimension 10
                frame_indices = get_index(video_len - 1, n_frames)
            vr.seek(0)
            images = vr.get_batch(frame_indices).asnumpy()
        except Exception as e:
            print(json.dumps({
                'question_id': qa_item['question_id'],
                'prompt': "Error" + str(e),
                'answer': qa_item['answer'],
            }), file=fout)
            continue

    prompt = ''
    for i in range(images.shape[0]):
        data = Image.fromarray(images[i])
        img_path = 'video_imgs_{}/{}_{}.jpg'.format(n_frames, qa_item['question_id'], i)
        data.save(img_path)
        prompt += '<img>' + img_path + '</img>\n'

    choices = [qa_item['choice_a'], qa_item['choice_b'], qa_item['choice_c'], qa_item['choice_d']]
    choice_list = []
    for i, c in enumerate(choices):
        choice_list.append('{}. {}'.format(chr(i + 65), c))
    choice_txt = '\n'.join(choice_list)

    prompt += 'Question: {}\nOptions: {}\nAnswer:'.format(qa_item['question'], choice_txt)
    print(json.dumps({
        'question_id': qa_item['question_id'],
        'prompt': prompt,
        'answer': qa_item['answer'],
    }), file=fout)
fout.close()
