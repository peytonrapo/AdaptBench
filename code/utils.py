import base64
import io
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from openai import OpenAI

client = OpenAI()

max_attempts = 10

###############################
# GPT Call Functions
###############################

# Calls GPT with the given prompt and returns the string response
def call_gpt(prompt, chart_img = None, system_prompt=None):
    content = [
                {
                "type": "text",
                "text": prompt
                }
            ]
    
    if chart_img:
        content.append({
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{chart_img}"
                }
                })
    
    messages = [
        {
            "role": "user",
            "content": content
        }
    ]

    if system_prompt:
        messages.append({
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": system_prompt
                    }
                ]
            })
        

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return response.choices[0].message.content

###############################
# Code Functions
###############################

# Returns None if code correctly compiles otherwise it returns the error
def test_code_compiles(code):
    try:
        context = {}
        exec(code, globals(), context)
        return None
    except Exception as e:
        return e
    
# Returns None if function code correctly runs while accepting the parameter code otherwise it returns the error
def test_function_accepts_parameter(function_code, parameter_code, function_name, parameter_name):
    try:
        context = {}
        exec(function_code, globals(), context)
        exec(parameter_code, globals(), context)

        context[function_name](context[parameter_name])
        return None
    except Exception as e:
        return e

# Cleans up the code output from GPT
def clean_code(code):
    code = remove_code_block_markers(code)
    code = remove_plt_display_code(code)
    code = clean_syntax_errors(code)
    return code

# Removes the python code block indicator from the GPT output
# Code from ChatGPT
def remove_code_block_markers(code):
    if code.startswith("```python\n"):
        code = code[len("```python\n"):]

    if code.endswith("```"):
        code = code[:-3]

    return code

# From ChatGPT
def remove_plt_display_code(code):
    """
    Remove any lines of code related to displaying or saving figures in Matplotlib.

    Parameters:
        code_string (str): The input Python code as a string.

    Returns:
        str: The modified code with display-related lines removed.
    """
    # Regular expression to match plt.show(), plt.savefig(), plt.close(), etc.
    display_patterns = [
        r"plt\.show\(.*?\)",  # Matches plt.show() with or without arguments
        r"plt\.savefig\(.*?\)",  # Matches plt.savefig() with arguments
        r"plt\.close\(.*?\)",  # Matches plt.close() with or without arguments
        r"plt\.figure\(.*?\)"  # Matches plt.figure() with or without arguments
    ]

    # Combine patterns into one
    combined_pattern = "|".join(display_patterns)

    # Remove lines matching the patterns
    modified_code = re.sub(combined_pattern, "", code, flags=re.MULTILINE)

    # Remove empty lines that may result
    modified_code = re.sub(r"^\s*\n", "", modified_code, flags=re.MULTILINE)

    return modified_code


# Closes open parantheses. GPT kept creating code that wouldn't compile
# Code from ChatGPT
def clean_syntax_errors(code):
    """
    Cleans up simple syntax mistakes in Python code.
    :param code: str - The Python code to clean.
    :return: str - Cleaned Python code.
    """

    # Fix unmatched parentheses
    open_paren = 0
    clean_code = ""
    for char in code:
        if char == '(':
            open_paren += 1
        elif char == ')':
            if open_paren > 0:
                open_paren -= 1
            else:
                # Skip unmatched closing parenthesis
                continue
        clean_code += char

    # Add missing closing parentheses
    clean_code += ')' * open_paren

    return clean_code

###############################
# Image Functions
###############################

# Opens the base64 chart image
# Code from ChaptGPT
def show_chart_img(chart_img):
    # Decode the Base64 string into bytes
    image_data = base64.b64decode(chart_img)

    # Convert the bytes to a PIL Image
    image = Image.open(io.BytesIO(image_data))

    # # clear the figure before loading the image (would still have the chart maybe)
    # plt.close()

    # Display the image using matplotlib
    plt.imshow(image)
    plt.axis('off')  # Hide axis for better visualization
    plt.show()

# Code from ChatGPT
def save_chart_image(chart_img, output_path):
    # Decode the Base64 string
    image_data = base64.b64decode(chart_img)

    # Write the binary data to the specified file location
    with open(output_path, "wb") as file:
        file.write(image_data)

    print(f"PNG image saved to {output_path}")

# Converts a matplotlib chart to a base64 image
# Code from ChatGPT
def convert_plt_to_base64(plt):
    # Step 1: Save the image to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Step 2: Encode the image to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_base64

# Converts a PIL Image to a base64 image
# Code from ChatGPT
def convert_pil_to_base64(img):
    # Step 1: Save the image to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Step 2: Encode the image to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_base64

# Function to encode the image
# Code from ChatGPT
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')