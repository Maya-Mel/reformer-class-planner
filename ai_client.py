import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=120000,
        retry_options=types.HttpRetryOptions(attempts=1),
    ),
)
MODELS = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.7-flash"]

def generate_with_fallback(contents, config):
    for model in MODELS:
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
        except errors.ServerError as error:
            print(f"{model} is busy ({error.code}), trying the next model...")

    raise RuntimeError("All models are busy right now. Please try again later.")

def ask_ai(prompt):
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
    )
    response = generate_with_fallback(prompt, config)
    return response.text
    
if __name__ == "__main__":
    answer = ask_ai("Explain what a Pilates reformer is in two sentences.")
    print(answer)
