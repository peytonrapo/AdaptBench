from code.utils import *
from code.prompts import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Breaks a question down into a generic question template
def question_decomposer(question):
    # get the question template
    question_template = call_gpt(question_template_prompt + question, question_template_system_prompt)

    return question_template

# Takes in a question template and chart data and creates the code needed to 
# answer this question
def answering_code_builder(question_template, chart_data):
    question_answering_code = call_gpt(answering_code_prompt + question_template + chart_data, answering_code_system_prompt)
    question_answering_code = clean_code(question_answering_code)

    return question_answering_code

# Takes in a chart image and the code used to answer a question and returns the
# question being asked of the chart
def question_builder(chart_img, answering_code):
    new_question = call_gpt_chart_image(chart_img, question_prompt + answering_code, question_system_prompt)

    return new_question

# Runs the given answering code on the given chart data. Returns the answer.
def answer_builder(answering_code, chart_data):
    context = {}
    exec(answering_code, globals(), context)
    exec(chart_data, globals(), context)

    answer = context["answer_question"](context["chart_data"])

    return answer