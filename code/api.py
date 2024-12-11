from code.chart_functions import *
from code.question_functions import *

# Takes in a chart base64 img and question string. Currently answer is not used.
# Returns a new chart object, a new question string, and the new answer
def modify_tuple(chart_img, question, debug=False):
    # New Chart Data
    # Verification: New Chart Data Compiles. Recomputes otherwise
    new_chart_data, chart_data_retries = get_chart_data(chart_img)
    if debug: print("New chart data: " + new_chart_data)

    # Question Template
    # No Verification: No time to debug text output. Could add later
    question_template = get_question_template(question)
    if debug: print("New question template: " + question_template)

    # Intermediate Question
    # No Verification: No time to debug text output. Could add later
    intermediate_question = get_intermediate_question(question_template, new_chart_data)
    if debug: print("Intermediate Question: " + intermediate_question)
      
    # Answering Code
    # Verification: Answering Code compiles. Recomputes otherwise
    # Verification: Answering Code works with New Chart Data as an input. Modifies Answering Code otherwise
    answering_code, answer_code_retries = get_question_answering_code(intermediate_question, new_chart_data)
    if debug: print("Answering code: " + answering_code)

    # New Chart Code
    # Verification: New Chart Code Compiles. Recomputes New Chart Code otherwise
    # Verification: New Chart Code works with New Chart Data as an input. Modifies New Chart Code otherwise
    new_chart_code, chart_code_retries = get_chart_code(chart_img, new_chart_data)
    if debug: print("New chart code: " + new_chart_code)

    # New Chart Image
    new_chart_img = get_chart_img(new_chart_data, new_chart_code)
    if debug: show_chart_img(new_chart_img)

    # New Question
    new_question = get_question(new_chart_img, answering_code)
    if debug: print("New Question: " + new_question)

    # New Answer
    new_answer = get_answer(answering_code, new_chart_data)
    if debug: print("New answer" + str(new_answer))

    metrics = {
        "chart_data_retries": chart_data_retries, 
        "answering_code_retries": answer_code_retries, 
        "chart_code_retries": chart_code_retries
    }

    return new_chart_img, new_question, new_answer, metrics