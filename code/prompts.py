# Creates chart_data object
chart_data_prompt = "Generate a pandas dataframe chart_data containing the data used to build the given chart."
chart_data_system_prompt = "Output chart_data only. chart_data must be convertible to a numpy array."

# Creates plot_chart function
chart_code_prompt = "Generate a function plot_chart which takes in a pandas dataframe chart_data and returns a matplotlib object plt in the style of the given chart. Chart Data: "
chart_code_system_prompt = "Output plot_chart only. Do not show the plot. Replace any color data with an equivalent sequence of matplotlib colors."

# Creates a generic version of a question
question_template_prompt = "Parameterize this question for this chart so that it is applicable of any chart, but captures the same essence. Question: "
question_template_system_prompt = "Output only the new question."

# Creates a specific version of a question from a template and data
intermediate_question_prompt = "Write a question that is answerable by chart_data and is in the style of the following question template. Question Template: "
intermediate_question_system_prompt = "Output only the new question."

# Create the question that this code is trying to answer
question_prompt = "Write the question for the given chart for which the following code is trying to answer. Code: "
question_system_prompt = "Output only the new question."

# Create an answer_question function to answer the question for the chart
answering_code_prompt = "Generate a function answer_question which takes in a pandas dataframe chart_data and returns the answer to the following question. Question: "
answering_code_system_prompt = "Output answer_question only. Make all parameters for answer_question optional except for chart_data."

# Try to fix compilation errors
compilation_error_prompt = "Fix the following code for the given error. Code: "
compilation_error_system_prompt = "Output code only. The prompt that created this code was: "

# Try to fix runtime errors
runtime_error_prompt = "Fix the following function for the given error when the given variable is passed as a parameter. Code: "
runtime_error_system_prompt = "Output code only. The prompt that created this function was: "
