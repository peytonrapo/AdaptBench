from code.utils import *
from code.prompts import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Breaks a question down into a generic question template
def get_question_template(question):
    # get the question template
    question_template = call_gpt(question_template_prompt + question, system_prompt=question_template_system_prompt)

    return question_template

def get_intermediate_question(question_template, chart_data):
    intermediate_question = call_gpt(intermediate_question_prompt + question_template + chart_data, system_prompt=intermediate_question_system_prompt)

    return intermediate_question

# Takes in a question template and chart data and creates the code needed to 
# answer this question
def get_question_answering_code(intermediate_question, chart_data):
    question_answering_code = call_gpt(answering_code_prompt + intermediate_question + chart_data, system_prompt=answering_code_system_prompt)
    question_answering_code = clean_code(question_answering_code)

    # Verification: Code compiles and has no runtime errors
    compilation_error = test_code_compiles(question_answering_code)

    # Want to only really test for runtime errors if it compiles
    if compilation_error is None:
        runtime_error = test_function_accepts_parameter(question_answering_code, chart_data, "answer_question", "chart_data")

    attempt = 0
    while compilation_error or runtime_error:
        if attempt == max_attempts:
            raise RuntimeError("Max number of attempts failed for trying to get question answering code")
        else:
            attempt += 1
        
        original_prompt = answering_code_prompt + intermediate_question + chart_data + answering_code_system_prompt

        # Send code and error message to GPT to try to get a fixed answer
        if compilation_error:
            error_prompt = compilation_error_prompt + question_answering_code + compilation_error
            system_prompt = compilation_error_system_prompt+original_prompt
            
            question_answering_code = call_gpt(error_prompt, system_prompt=system_prompt)
            question_answering_code = clean_code(question_answering_code)

            compilation_error = test_code_compiles(question_answering_code)
        else: # runtime error
            error_prompt = runtime_error + question_answering_code + chart_data + runtime_error
            system_prompt = runtime_error_system_prompt+original_prompt

            question_answering_code = call_gpt(error_prompt, system_prompt=system_prompt)
            question_answering_code = clean_code(question_answering_code)

            compilation_error = test_code_compiles(question_answering_code)
            if compilation_error is None:
                runtime_error = test_function_accepts_parameter(question_answering_code, chart_data, "answer_question", "chart_data")

    return question_answering_code

# Takes in a chart image and the code used to answer a question and returns the
# question being asked of the chart
def get_question(chart_img, answering_code):
    new_question = call_gpt(question_prompt + answering_code, chart_img=chart_img, system_prompt=question_system_prompt)

    return new_question

# Runs the given answering code on the given chart data. Returns the answer.
def get_answer(answering_code, chart_data):
    context = {}
    exec(answering_code, globals(), context)
    exec(chart_data, globals(), context)

    answer = context["answer_question"](context["chart_data"])

    return answer