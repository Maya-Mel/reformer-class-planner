from google.genai import types
from ai_client import client

models_to_try = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
]

for model in models_to_try:
    try:
        response = client.models.generate_content(
            model=model,
            contents="Say hi in one word.",
            config=types.GenerateContentConfig(
                http_options=types.HttpOptions(timeout=20000),
            ),
        )
        print("OK   ", model, "->", response.text.strip())
    except Exception as error:
        print("FAIL ", model, "->", str(error)[:80])