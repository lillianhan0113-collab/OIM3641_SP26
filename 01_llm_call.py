import os
import re
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()
print("env loaded, key exists:", bool(os.getenv("GOOGLE_API_KEY")))

# Initialize client (API key is read from .env automatically)
client = genai.Client()


def generate_prompt():
    return """write the python code to calculate
a loan payment with the following inputs: interest,
term, present value. return code only wrapped in a Markdown
code block (triple backticks). Do not add any extra text or
explanation outside the code block."""


# Generate content from the model
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=generate_prompt()
)

# Extract python code from a markdown code block
match = re.search(r"```(?:python)?\s*(.*?)```", response.text, re.DOTALL)

if not match:
    print("No code block found in response:")
    print(response.text)
    raise SystemExit

code_content = match.group(1).strip()

print("--- Extracted code ---")
print(code_content)

# Save extracted code into a new file
with open("loan_calc.py", "w", encoding="utf-8") as f:
    f.write(code_content)


