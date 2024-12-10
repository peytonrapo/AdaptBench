from code.utils import *
from code.prompts import *
import numpy as np
import matplotlib.pyplot as plt

# Takes in a base64 chart img and returns an approximate set of chart_data
# and chart_code
def chart_decomposer(chart_img, debug=False):
    # Get the underlying data of the chart
    chart_data = remove_code_block_markers(call_gpt_chart_image(chart_img, chart_data_prompt))
    if debug:
        print(chart_data)

    # Get chart gen code from chart + the data table
    chart_code = remove_code_block_markers(call_gpt_chart_image(chart_img, chart_code_prompt + chart_data))
    if debug:
        print(chart_code)

    chart_code = replace_show_with_save(chart_code)
    if debug:
        print(chart_code)

    return chart_data, chart_code

# takes in chart_data and chart_code and returns a base64 chart img
def chart_builder(chart_data, chart_code):
    # Create chart from underlying data
    context = {}
    exec(chart_data, globals(), context)
    exec(chart_code, globals(), context)

    chart_img = context["plot_chart"](context["chart_data"])
    return chart_img

# takes in a base64 chart img and will return the new_chart_img and the new_chart_data
def chart_modifier(chart_img, debug=False):
    new_chart_data, new_chart_code = chart_decomposer(chart_img, debug)

    new_chart_img = chart_builder(new_chart_data, new_chart_code)

    return new_chart_img, new_chart_data