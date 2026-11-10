import json
from ai_client import ask_ai

with open("data/exercises.json", encoding="utf-8") as file:
    exercises = json.load(file)

print("Number of exercises:", len(exercises))

def find_exercises(level, conditions):
    results = []
    for exercise in exercises:
        if exercise["level"] != level:
            continue
        
        is_safe = True
        for condition in conditions:
            if condition in exercise["contraindications"]:
                is_safe = False
                break
        if is_safe:
            results.append(exercise)
    return results

level = "beginner"
conditions = ["knee_injury", "pregnancy"]

safe_exercises = find_exercises(level, conditions)
print("Matching exercises:", len(safe_exercises))

exercise_list = ""
for exercise in safe_exercises:
    exercise_list += f"- {exercise['name']}, {exercise['series']}, springs: {exercise['springs']}, {exercise['description']}\n"

prompt = f"""
You are an experienced Pilates reformer instructor.

Build a {level} level reformer class for a client with these conditions: {", ".join(conditions)}.

Use ONLY exercises from this list. Do not add any exercise that is not on the list:
{exercise_list}

Class requirements:
- Total length: 50 minutes.
- About 15 exercises, around 10 repetitions each.
- Start with a Footwork warm-up and end with Stretching.
- Cover the whole body: core, arms, glutes, and legs in straps.
- Keep exercises from the same series together, in a logical order.

For each exercise write: name, springs, repetitions, and one short cue for the instructor.
Base each cue only on the exercise description. Do not invent technique details that are not in the description.
Write the cues in natural, simple Hebrew, the way an Israeli Pilates instructor talks in class.
Write the exercise names in English and everything else in Hebrew.
"""

#lesson = ask_ai(prompt)
#print(lesson)