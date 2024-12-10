from code.chart_functions import *
from code.question_functions import *

# Takes in a chart base64 img and question string. Currently answer is not used.
# Returns a new chart object, a new question string, and an answer string
def modify_tuple(chart_img, question, debug=False):
    # New Chart
    new_chart_data, new_chart_code = chart_decomposer(chart_img)
    if debug: print("New chart data: " + new_chart_data)
    if debug: print("New chart code: " + new_chart_code)

    new_chart_img = chart_builder(new_chart_data, new_chart_code)
    if debug: show_chart_img(new_chart_img)

    # New Question & Answer
    question_template = question_decomposer(question)
    if debug: print("New question template: " + question_template)
    
    answering_code = answering_code_builder(question_template, new_chart_data)
    if debug: print("Answering code: " + answering_code)

    # New Answer
    new_answer = answer_builder(answering_code, new_chart_data)
    if debug: print("New answer" + str(new_answer))
    
    # New Question
    new_question = question_builder(new_chart_img, answering_code)
    if debug: print("New Question: " + new_question)

    return new_chart_img, new_question, new_answer