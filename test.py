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
    old_chart = question_tuples[tuple_idx]['decoded_image']
    old_chart_img = convert_pil_to_base64(old_chart)
    old_question = question_tuples[tuple_idx]['question']
    old_answer = question_tuples[tuple_idx]['answer']

    try:
        new_chart_img, new_question, new_answer = modify_tuple(old_chart_img, old_question, False)
    except Exception as e:
        print(f"Question Tuple {tuple_idx} failed with error: {e}")
        
    print(f"Question Tuple: {tuple_idx}")
    print("Original Question: " + old_question)
    print("Original Answer:" + str(old_answer))
    old_chart.show()

    print()
    print("New Question: " + new_question)
    print("New Answer: " + str(new_answer))
    show_chart_img(new_chart_img)