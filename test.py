import json
import random as r
from datasets import load_dataset
from code.api import modify_tuple
from code.utils import convert_pil_to_base64, show_chart_img, save_chart_image

dataset = load_dataset("AI4Math/MathVista")

dataset_names = ["FigureQA", "DVQA", "ChartQA"]

question_tuples = []

for data in dataset["testmini"]:
    if data["metadata"]["source"] in dataset_names:
        question_tuples.append(data)


old_chart_image_path = "experiment_data/original_chart_images"
new_chart_image_path = "experiment_data/modified_chart_images"
new_question_tuple_path = "experiment_data/modified_question_tuples"
failed_question_tuple_indices_path = "experiment_data"

# num_samples = 5
# tuple_indices = r.sample(range(len(question_tuples)), num_samples)
tuple_indices = range(len(question_tuples))

debug = False

failed_question_tuple_indices = {}

for tuple_idx in tuple_indices:
    question_tuple_pid = question_tuples[tuple_idx]['pid']

    old_chart = question_tuples[tuple_idx]['decoded_image']
    old_chart_img = convert_pil_to_base64(old_chart)
    old_question = question_tuples[tuple_idx]['question']
    old_answer = question_tuples[tuple_idx]['answer']

    try:
        new_chart_img, new_question, new_answer, metrics = modify_tuple(old_chart_img, old_question, debug)

        # save old chart image
        save_chart_image(old_chart_img, old_chart_image_path + "/" + question_tuple_pid + ".png")

        # save new chart image
        save_chart_image(new_chart_img, new_chart_image_path + "/" + question_tuple_pid + ".png")

        metadata = {
            "original_chart_path": old_chart_image_path + "/" + question_tuple_pid,
            "original_question": old_question,
            "original_answer": str(old_answer),
            "metrics": metrics
        }

        new_question_tuple = {
            "chart_path": new_chart_image_path + "/" + question_tuple_pid,
            "question": new_question,
            "answer": str(new_answer),
            "pid": question_tuple_pid,
            "metadata": metadata
        }

        # save the new question tuple
        with open(new_question_tuple_path + "/" + question_tuple_pid + ".json", "w") as file:
            json.dump(new_question_tuple, file, indent=4) 
            
        if debug:
            print(f"Question Tuple: {tuple_idx}")
            print("Original Question: " + old_question)
            print("Original Answer:" + str(old_answer))
            show_chart_img(old_chart_img)

            print()
            print("New Question: " + new_question)
            print("New Answer: " + str(new_answer))
            show_chart_img(new_chart_img)

    except Exception as e:
        print(f"Question Tuple {tuple_idx} failed with error: {e}")
        failed_question_tuple_indices[tuple_idx] = e

# save the failed tuple indices
with open(failed_question_tuple_indices_path + "/failed_question_tuple_indices.json", "w") as file:
    json.dump(failed_question_tuple_indices, file, indent=4) 