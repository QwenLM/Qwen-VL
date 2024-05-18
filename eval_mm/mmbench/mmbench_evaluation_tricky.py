import pandas as pd
import json
import random

'''
This script provides metric calculation for mmbench_dev with the same accuarcy algo as OpenCompass server
'''

predictions = json.load(open('mmbench_dev_20230712.json'))

index2predictions = {}
for pred in predictions:
    index2predictions[pred['index']] = pred['prediction']


from collections import Counter

def most_common_elements(lst):
    counter = Counter(lst)
    max_count = max(counter.values())
    most_common = [element for element, count in counter.items() if count == max_count]
    return random.choice(most_common) # random sample from random choice

datas = pd.read_csv("data/mmbench/mmbench_dev_20230712/mmbench_dev_20230712.tsv", sep='\t')

glb_opts = ['A', 'B', 'C', 'D']
index2answer = {}
index2choices = {}
index2rawanswer = {}
for idx in range(len(datas)):
    data = datas.iloc[idx]
    
    choices = []
    for opt in glb_opts:
        if not pd.isna(data[opt]):
            choices.append(data[opt])
    index2choices[data['index']] = choices

    index2answer[data['index']] = glb_opts.index(data['answer'])
    index2rawanswer[data['index']] = choices[glb_opts.index(data['answer'])]

identity_indexes = list(set([int(_ % 1e6) for _ in index2predictions.keys()]))

correct = 0
total = 0
for index in identity_indexes:
    raw_preds = []
    raw_answer = []
    for _ in range(4):
        cycle_index = int(_ * 1e6 + index)
        if index2predictions.get(cycle_index, None) is not None:
            raw_answer = index2rawanswer[cycle_index]
            raw_pred = index2choices[cycle_index][index2predictions[cycle_index]]
            raw_preds.append(raw_pred)

    if len(set(raw_preds)) == 1:
        if raw_preds[0] == raw_answer:
            correct += 1
    else:
        result = most_common_elements(raw_preds)
        if result == raw_answer:
            correct += 1

    total += 1

print(correct, total, correct / total * 100.)
