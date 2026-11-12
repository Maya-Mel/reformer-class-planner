from google.genai import types

from ai_client import client, MODELS
from tools import find_exercises, get_exercise_details, check_class_safety

config = types.GenerateContentConfig(
    tools=[find_exercises, get_exercise_details, check_class_safety],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

TOOLS = {
    "find_exercises": find_exercises,
    "get_exercise_details": get_exercise_details,
    "check_class_safety": check_class_safety,
}

MAX_STEPS = 10


def run_agent(request: str) -> str:
    contents = [types.Content(role="user", parts=[types.Part(text=request)])]

    for step in range(MAX_STEPS):
        response = client.models.generate_content(
            model=MODELS[0],
            contents=contents,
            config=config,
        )
        contents.append(response.candidates[0].content)

        if not response.function_calls:
            return response.text

        results = []
        for call in response.function_calls:
            print(f"Step {step + 1}: {call.name}({call.args})")
            function = TOOLS[call.name]
            result = function(**call.args)
            results.append(
                types.Part.from_function_response(name=call.name, response={"result": result})
            )
        contents.append(types.Content(role="user", parts=results))

    return "The agent stopped: too many steps."


if __name__ == "__main__":
    request = "Build a 50 minute beginner reformer class for a pregnant client."
    print(run_agent(request))