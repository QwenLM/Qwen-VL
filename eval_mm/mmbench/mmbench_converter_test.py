import pandas as pd
import io
import base64
import json
from PIL import Image

'''
This script convert mmbench_test tsv file to jsonl
This script is very similar to mmbench_converter_dev except there's no answer for accuracy calculation
'''

datas = pd.read_csv("data/mmbench/mmbench_test_20230712/mmbench_test_20230712.tsv", sep='\t')

global_choices = ['A', 'B', 'C', 'D']

def decode_base64_to_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image


with open('./data/mmbench/mmbench_test_20230712/mmbench_test_20230712.jsonl', 'w') as f:
    for idx in range(len(datas)):
        data = datas.iloc[idx]
        
        index = int(data['index'])
        question = data['question']
        hint = data['hint'] if not pd.isna(data['hint']) else 'N/A'

        choices = []
        for opt in global_choices:
            if pd.isna(data[opt]):
                continue
            choices.append(data[opt])

        # answer = global_choices.index(data['answer'])

        image = decode_base64_to_image(data['image'])
        image.save("data/mmbench/mmbench_test_20230712/images/%d.jpg" % index)

        f.write(json.dumps({
            "index": index,
            "image": "data/mmbench/mmbench_test_20230712/images/%d.jpg" % index,
            "hint": hint,
            "question": question,
            "choices": choices, 
            # "answer": answer,
        }) + "\n")

