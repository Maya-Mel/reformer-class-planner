import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.8-flash"

def ask_ai(prompt):
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

answer = ask_ai("Explain what a Pilates reformer is in two sentences.")
print(answer)