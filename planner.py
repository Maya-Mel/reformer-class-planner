import json

with open("data/exercises.json", encoding="utf-8") as file:
    exercises = json.load(file)

print("Number of exercises:", len(exercises))

for exercise in exercises:
    if exercise["level"] == "beginner" and "pregnancy" not in exercise["contraindications"]:
        print(exercise["name"])