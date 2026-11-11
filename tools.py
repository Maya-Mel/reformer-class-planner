import json

with open("data/exercises.json", encoding="utf-8") as file:
    exercises = json.load(file)

def find_exercises(level: str, conditions: list[str]) -> list[dict]:
    """Find reformer exercises that match a level and are safe for the client's conditions.

    Args:
        level: The client's level: "beginner", "intermediate" or "advanced".
        conditions: The client's contraindications, for example ["pregnancy", "knee_injury"].
            Use an empty list if there are none.
    """
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

def get_exercise_details(exercise_id: str) -> dict | None:
    """Return the details of a reformer exercise by its ID. If not found, return None.
    
    Args:
        exercise_id: The ID of the exercise, for example "round_back".
    """
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise
    return None

def check_class_safety(exercise_ids: list[str], conditions: list[str]) -> list[str]:
    """Check if a list of exercises is safe for a client with given conditions.

    Args:
        exercise_ids: A list of exercise IDs, for example ["round_back", "hundred"].
        conditions: A list of the client's contraindications.

    Returns:
        A list of problems. An empty list means the class is safe.
    """
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
 