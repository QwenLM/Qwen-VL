import pandas as pd
import json

'''
This script provides `global top-1 accuracy` metric calculation for mmbench_dev.
'''

predictions = json.load(open('mmbench_dev_20230712.json'))

index2predictions = {}
for pred in predictions:
    index2predictions[pred['index']] = pred['prediction']

datas = pd.read_csv("data/mmbench/mmbench_dev_20230712/mmbench_dev_20230712.tsv", sep='\t')

glb_opts = ['A', 'B', 'C', 'D']
index2answer = {}
for idx in range(len(datas)):
    data = datas.iloc[idx]
    index2answer[data['index']] = glb_opts.index(data['answer'])

identity_indexes = list(set([int(_ % 1e6) for _ in index2predictions.keys()]))

correct = 0
total = 0
for index in identity_indexes:
    for _ in range(4):
        cycle_index = int(_ * 1e6 + index)
        if index2predictions.get(cycle_index, None) is not None:
            if index2predictions[cycle_index] == index2answer[cycle_index]:
                continue
            else:
                print(cycle_index)
                break
    else:
        correct += 1
    total += 1

print(correct, total)
