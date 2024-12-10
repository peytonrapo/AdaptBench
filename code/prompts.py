# Instructions for all GPT calls
system_prompt = "Output only the question or code asked for. Do not provide any examples of code use."

# creates chart_data object
chart_data_prompt = "Generate a pandas dataframe chart_data containing the data used to build the given chart. chart_data must be convertible to a numpy array."

# creates plot_chart function
chart_code_prompt = "Generate a function plot_chart which takes in a pandas dataframe chart_data and returns a matplotlib object plt in the style of the given chart. Do not show the plot. Replace any color data with an equivalent sequence of matplotlib colors. Chart Data: " # + the data

# creates a generic version of a question
question_template_prompt = "Parameterize this question for this chart so that it is applicable of any chart, but captures the same essence. Question: " # + question

# Create the question that this code is trying to answer
question_prompt = "Write the question for the given chart for which the following code is trying to answer. Code: "

# Create an answer_question function to answer the question for the chart
answering_code_prompt = "Generate a function answer_question which takes in a pandas dataframe chart_data and returns the answer to the following question. If the function has parameters other than chart_data, make them optional with a reasonable default value. Ensure the function has no syntax errors or missing parentheses. Question: "