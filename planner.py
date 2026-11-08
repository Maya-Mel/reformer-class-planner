import json

with open("data/exercises.json", encoding="utf-8") as file:
    exercises = json.load(file)

print("Number of exercises:", len(exercises))

def find_exercises(level, condition):
    results = []
    for exercise in exercises:
        if exercise["level"] == level and condition not in exercise["contraindications"]:
            results.append(exercise)
    return results

safe_exercises = find_exercises("beginner", "knee_injury")
print("Matching exercises:", len(safe_exercises))
for exercise in safe_exercises:
    print(exercise["name"])

