import pandas as pd
import json
import random

'''
This script convert the output file of our inference processor to target formation of OpenCompass evaluator server
'''

predictions = json.load(open('mmbench_test_20230712.json'))

index2predictions = {}
for pred in predictions:
    index2predictions[pred['index']] = pred['prediction']

from collections import Counter

def most_common_elements(lst):
    counter = Counter(lst)
    max_count = max(counter.values())
    most_common = [element for element, count in counter.items() if count == max_count]
    print(most_common)
    return random.choice(most_common)
    # return most_common

datas = pd.read_csv("data/mmbench/mmbench_test_20230712/mmbench_test_20230712.tsv", sep='\t')

datas = datas.drop('image', axis=1)

glb_opts = ['A', 'B', 'C', 'D']
index2choices = {}
for idx in range(len(datas)):
    data = datas.iloc[idx]
    
    choices = []
    for opt in glb_opts:
        if not pd.isna(data[opt]):
            choices.append(data[opt])
    index2choices[data['index']] = choices

identity_indexes = list(set([int(_ % 1e6) for _ in index2predictions.keys()]))


processed_index2predictions = {}
for index in identity_indexes:
    raw_preds = []
    for _ in range(4):
        cycle_index = int(_ * 1e6 + index)
        if index2predictions.get(cycle_index, None) is not None:
            raw_pred = index2choices[cycle_index][index2predictions[cycle_index]]
            raw_preds.append(raw_pred)
    
    if len(set(raw_preds)) == 1:
        pred_answer = raw_preds[0]
    else:
        pred_answer = most_common_elements(raw_preds)

    print(index, pred_answer)
    for _ in range(4):
        cycle_index = int(_ * 1e6 + index)
        if index2predictions.get(cycle_index, None) is not None:
            processed_index2predictions[cycle_index] = index2choices[cycle_index].index(pred_answer)


predictions = []
for idx in range(len(datas)):
    data = datas.iloc[idx]
    index = data['index']
    prediction = glb_opts[processed_index2predictions[index]]
    predictions.append(prediction)

datas['prediction'] = predictions
datas.to_excel("mmbench_test_20230712_230831_constrained.xlsx", index=False)
# constrained means we force the model predict same answer when tested on a question for multiple times
