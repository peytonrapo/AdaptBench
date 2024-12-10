from code.utils import *
from code.prompts import *
import numpy as np

def question_decomposer(question, debug=False):
    # get the question template
    question_template = call_gpt(question_template_prompt + question)
    if debug:
        print(question_template)

    return question_template

def answering_code_builder(question, chart_data, debug=False):
    question_answering_code = remove_code_block_markers(call_gpt(answering_code_prompt + question + chart_data))
    question_answering_code = clean_syntax_errors(question_answering_code)
    if debug:
        print(question_answering_code)

    return question_answering_code

def question_builder(chart_img, answering_code, debug=False):
    new_question = call_gpt_chart_image(chart_img, question_prompt + answering_code)
    if debug:
        print(new_question)

    return new_question

def answer_builder(answering_code, chart_data, debug=False):
    context = {}
    exec(answering_code, globals(), context)
    exec(chart_data, globals(), context)

    answer = context["answer_question"](context["chart_data"])
    if debug:
        print(answer)

    return answer