from code.utils import *
from code.prompts import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Takes in a base64 chart img and returns an approximate set of chart_data
# and chart_code
def chart_decomposer(chart_img):
    # Get the underlying data of the chart
    chart_data = remove_code_block_markers(call_gpt_chart_image(chart_img, chart_data_prompt))

    # Get chart gen code from chart + the data table
    chart_code = remove_code_block_markers(call_gpt_chart_image(chart_img, chart_code_prompt + chart_data))
    chart_code = replace_show_with_save(chart_code)

    return chart_data, chart_code

# takes in chart_data and chart_code and returns a base64 chart img
def chart_builder(chart_data, chart_code):
    # Create chart from underlying data
    context = {}
    exec(chart_data, globals(), context)
    exec(chart_code, globals(), context)

    # clear plt before creating the chart on it.
    plt.clf()
    chart_img = convert_plt_to_base64(context["plot_chart"](context["chart_data"]))
    return chart_img