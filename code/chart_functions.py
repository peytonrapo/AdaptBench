from code.utils import *
from code.prompts import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Takes in a base64 chart img and returns an approximate set of chart_data
def get_chart_data(chart_img):
    # Get the underlying data of the chart
    chart_data = call_gpt(chart_data_prompt, chart_img=chart_img, system_prompt=chart_data_system_prompt)
    chart_data = clean_code(chart_data)

    # Verification: Code compiles

    compilation_error = test_code_compiles(chart_data)
    attempt = 0
    while compilation_error:
        if attempt == max_attempts:
            raise RuntimeError("Max number of attempts failed for trying to get chart data")
        else:
            attempt += 1
        
        # Send code and error message to GPT to try to get a fixed answer
        error_prompt = compilation_error_prompt + chart_data + str(compilation_error)
        system_prompt = compilation_error_system_prompt + chart_data_prompt+chart_data_system_prompt

        chart_data = call_gpt(error_prompt, chart_img=chart_img, system_prompt=system_prompt)
        chart_data = clean_code(chart_data)

        compilation_error = test_code_compiles(chart_data)

    return chart_data, attempt

# Takes in a base64 chart img and a pandas data frame and returns the code needed
# to render a chart in the style of chart_img
def get_chart_code(chart_img, chart_data):
    # Get chart gen code from chart + the data table
    chart_code = call_gpt(chart_code_prompt + chart_data, chart_img=chart_img, system_prompt=chart_code_system_prompt)
    chart_code = clean_code(chart_code)

    # Verification: Code compiles and has no runtime errors
    compilation_error = test_code_compiles(chart_code)

    # Want to only really test for runtime errors if it compiles
    if compilation_error is None:
        runtime_error = test_function_accepts_parameter(chart_code, chart_data, "plot_chart", "chart_data")

    attempt = 0
    while compilation_error or runtime_error:
        if attempt == max_attempts:
            raise RuntimeError("Max number of attempts failed for trying to get chart code")
        else:
            attempt += 1
        
        original_prompt = chart_code_prompt + chart_data + chart_code_system_prompt

        # Send code and error message to GPT to try to get a fixed answer
        if compilation_error:
            error_prompt = compilation_error_prompt + chart_code + str(compilation_error)
            system_prompt = compilation_error_system_prompt + original_prompt

            chart_code = call_gpt(error_prompt, system_prompt=system_prompt)
            chart_code = clean_code(chart_code)

        else: # runtime error
            error_prompt = runtime_error_prompt + chart_code + chart_data + str(runtime_error)
            system_prompt = runtime_error_system_prompt+original_prompt

            chart_code = call_gpt(error_prompt, system_prompt=system_prompt)
            chart_code = clean_code(chart_code)

        compilation_error = test_code_compiles(chart_code)
        if compilation_error is None:
            runtime_error = test_function_accepts_parameter(chart_code, chart_data, "plot_chart", "chart_data")

    return chart_code, attempt

# takes in chart_data and chart_code and returns a base64 chart img
def get_chart_img(chart_data, chart_code):
    # Create chart from underlying data
    context = {}
    exec(chart_data, globals(), context)
    exec(chart_code, globals(), context)

    # clear plt before creating the chart on it.
    plt.clf()
    chart_img = convert_plt_to_base64(context["plot_chart"](context["chart_data"]))
    return chart_img