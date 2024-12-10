from code.chart_functions import chart_decomposer

import random as r
from datasets import load_dataset
from code.api import modify_tuple
from code.utils import convert_pil_to_base64, show_chart_img

dataset = load_dataset("AI4Math/MathVista")

dataset_names = ["FigureQA", "DVQA", "ChartQA"]

question_tuples = []

for data in dataset["testmini"]:
    if data["metadata"]["source"] in dataset_names:
        question_tuples.append(data)

max_attempts = 10
num_samples = 10

tuple_indices = r.sample(range(len(question_tuples)), num_samples)

for tuple_idx in tuple_indices:
    old_chart_img = convert_pil_to_base64(question_tuples[tuple_idx]['decoded_image'])
    old_question = question_tuples[tuple_idx]['question']
    old_answer = question_tuples[tuple_idx]['answer']

    new_chart_data, new_chart_code = chart_decomposer(old_chart_img)
    print(new_chart_data)
    print(new_chart_code)