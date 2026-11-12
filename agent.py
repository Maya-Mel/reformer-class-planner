from google.genai import types
from ai_client import generate_with_fallback
from tools import find_exercises, get_exercise_details, check_class_safety

SYSTEM_INSTRUCTION = """
You are an experienced Pilates reformer instructor.

The instructor will describe the client. Understand the client's level and contraindications from the request.

Rules for using the tools:
- Get exercises ONLY with the find_exercises tool. Never use an exercise that did not come from the tools.
- Before giving the final class, ALWAYS check it with the check_class_safety tool.
- If check_class_safety finds problems, replace those exercises and check again.
- Use the springs exactly as they appear in the tool results. Do not invent spring colors.

Class requirements:
- Total length: 50 minutes.
- About 18 exercises, around 10 repetitions each.
- Start with a Footwork warm-up and end with Stretching.
- The class MUST include all of these (check the body_focus field of each exercise):
  - at least 4 exercises for core
  - at least 3 exercises for glutes
  - at least 4 exercises for arms
  - at least 3 exercises from the Leg Series (legs in straps)
- Keep exercises from the same series together, in a logical order.

For each exercise write: name, springs, repetitions, and one short cue for the instructor.
Base each cue only on the exercise description. Do not invent technique details that are not in the description.
Write the cues in natural, simple Hebrew, the way an Israeli Pilates instructor talks in class.
Write the exercise names in English and everything else in Hebrew.
"""

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[find_exercises, get_exercise_details, check_class_safety],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
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
        response = generate_with_fallback(contents, config)
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