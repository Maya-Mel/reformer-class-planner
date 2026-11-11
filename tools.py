import json

with open("data/exercises.json", encoding="utf-8") as file:
    exercises = json.load(file)

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

def get_exercise_details(exercise_id):
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise
    return None

def check_class_safety(exercise_ids, conditions):
    problems = []
    for exercise_id in exercise_ids:
        exercise = get_exercise_details(exercise_id)
        if exercise is None:
            problems.append(f"Unknown exercise: {exercise_id}.")
            continue

        for condition in conditions:
            if condition in exercise["contraindications"]:
                problems.append(f"Exercise {exercise['name']} is not safe for {condition}.")
    return problems
 