import base64
import io
import re
from PIL import Image
import matplotlib.pyplot as plt
from openai import OpenAI

client = OpenAI()

# From ChaptGPT
def show_chart_img(chart_img):
    # Decode the Base64 string into bytes
    image_data = base64.b64decode(chart_img)

    # Convert the bytes to a PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Display the image using matplotlib
    plt.imshow(image)
    plt.axis('off')  # Hide axis for better visualization
    plt.show()

# From ChatGPT
def convert_plt_to_base64(plt):
    # Step 1: Save the image to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Step 2: Encode the image to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_base64

# From ChatGPT
def convert_pil_to_base64(img):
    # Step 1: Save the image to a BytesIO object
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Step 2: Encode the image to base64
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_base64

# From ChatGPT
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# From ChatGPT
def remove_code_block_markers(text):
    if text.startswith("```python\n"):
        text = text[len("```python\n"):]

    if text.endswith("```"):
        text = text[:-3]

    return text

# From ChatGPT
def clean_syntax_errors(code):
    """
    Cleans up simple syntax mistakes in Python code.
    :param code: str - The Python code to clean.
    :return: str - Cleaned Python code.
    """
    # Fix missing colons in function definitions and loops
    code = re.sub(r'(def\s+\w+\(.*?\))\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(for\s+.+?\s+in\s+.+?)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(if\s+.+?)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(elif\s+.+?)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(else)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(while\s+.+?)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(try)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(except\s+.+?)\s*$', r'\1:', code, flags=re.M)
    code = re.sub(r'(finally)\s*$', r'\1:', code, flags=re.M)

    # Fix inconsistent indentation (convert tabs to 4 spaces)
    code = code.replace('\t', '    ')

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



def replace_show_with_save(code_str):
    # Replace 'plt.show()' with 'plt.savefig("save_path")'
    updated_code = code_str.replace("plt.show()", "return convert_plt_to_base64(plt)")
    return updated_code

def call_gpt(prompt):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt,
            },
        ],
        }
    ],
    )

    return response.choices[0].message.content

def call_gpt_chart_image(chart_img, prompt):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt,
            },
            {
            "type": "image_url",
            "image_url": {
                "url":  f"data:image/jpeg;base64,{chart_img}"
            },
            },
        ],
        }
    ],
    )

    return response.choices[0].message.content

def call_gpt_chart_local(chart_path, prompt):
    # Getting the base64 string
    base64_image = encode_image(chart_path)

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt,
            },
            {
            "type": "image_url",
            "image_url": {
                "url":  f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    )

    return response.choices[0].message.content