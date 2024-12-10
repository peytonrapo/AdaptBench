# creates chart_data object
chart_data_prompt = "Generate a numpy.array chart_data which contains the underlying data in this chart. Make the data as detailed as possible. Output only the chart_data object."

# creates plot_chart function
chart_code_prompt = "Generate a function plot_chart which takes in a numpy.array chart_data and uses matplotlib to plot chart_data to recreate the given chart. Output only the plot_chart function. Chart Data: " # + the data

# creates a generic version of a question
question_template_prompt = "Parameterize this question for this chart so that it is applicable of any chart, but captures the same essence. Output only the new question. Question: " # + question

# Create the question that this code is trying to answer
question_prompt = "Write the question for the given chart for which the following code is trying to answer. Output only the new question. Code: "

# Create an answer_question function to answer the question for the chart
answering_code_prompt = "Generate a function answer_question which takes in a numpy.array chart_data and returns the answer to the following question. Ensure the function has no syntax errors or missing parentheses. Output only the answer_question function. Question: "