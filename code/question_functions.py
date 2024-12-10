from code.utils import *
from code.prompts import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def question_decomposer(question):
    # get the question template
    question_template = call_gpt(question_template_prompt + question)

    return question_template

def answering_code_builder(question, chart_data):
    question_answering_code = call_gpt(answering_code_prompt + question + chart_data)
    question_answering_code = clean_code(question_answering_code)

    return question_answering_code

def question_builder(chart_img, answering_code):
    new_question = call_gpt_chart_image(chart_img, question_prompt + answering_code)

    return new_question

def answer_builder(answering_code, chart_data):
    context = {}
    exec(answering_code, globals(), context)
    exec(chart_data, globals(), context)

    answer = context["answer_question"](context["chart_data"])

    return answer