from code.chart_functions import *
from code.question_functions import *

# Takes in a chart base64 img and question string. Currently answer is not used.
# Returns a new chart object, a new question string, and an answer string
def modify_tuple(chart_img, question, debug=False):
    # New Chart
    new_chart_img, new_chart_data = chart_modifier(chart_img, debug)

    # New Question
    question_template = question_decomposer(question, debug)
    
    answering_code = answering_code_builder(question_template, new_chart_data, debug)
    
    new_question = question_builder(new_chart_img, answering_code, debug)
    
    # New Answer
    new_answer = answer_builder(answering_code, new_chart_data, debug)

    return new_chart_img, new_question, new_answer