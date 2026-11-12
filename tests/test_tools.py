from tools import exercises, find_exercises, get_exercise_details, check_class_safety


def test_find_exercises_returns_only_requested_level():
    results = find_exercises("beginner", [])
    for exercise in results:
        assert exercise["level"] == "beginner"

def test_hundred_is_not_safe_for_pregnancy():
    problems = check_class_safety(["hundred"], ["pregnancy"])
    assert len(problems) == 1

def test_safe_class_has_no_problems():
    problems = check_class_safety(["parallel_heels", "frog"], ["knee_injury"])
    assert len(problems) == 0


# find_exercises

def test_find_exercises_filters_out_condition():
    results = find_exercises("beginner", ["pregnancy"])
    result_ids = [exercise["id"] for exercise in results]
    for exercise in results:
        assert "pregnancy" not in exercise["contraindications"]
    assert "pulling_straps" not in result_ids

def test_find_exercises_filters_out_all_conditions():
    results = find_exercises("beginner", ["knee_injury", "hip_injury"])
    result_ids = [exercise["id"] for exercise in results]
    for exercise in results:
        assert "knee_injury" not in exercise["contraindications"]
        assert "hip_injury" not in exercise["contraindications"]
    assert "split_squat" not in result_ids

def test_find_exercises_without_conditions_returns_whole_level():
    expected = [exercise for exercise in exercises if exercise["level"] == "beginner"]
    results = find_exercises("beginner", [])
    assert len(results) == len(expected)


# get_exercise_details

def test_get_exercise_details_returns_the_right_exercise():
    exercise = get_exercise_details("hundred")
    assert exercise is not None
    assert exercise["id"] == "hundred"

def test_get_exercise_details_unknown_id_returns_none():
    assert get_exercise_details("no_such_exercise") is None


# check_class_safety

def test_unknown_exercise_is_a_problem():
    problems = check_class_safety(["no_such_exercise"], [])
    assert len(problems) == 1
    assert "Unknown exercise" in problems[0]

def test_each_condition_is_reported_separately():
    problems = check_class_safety(["hundred"], ["pregnancy", "neck_injury"])
    assert len(problems) == 2

def test_mixed_class_reports_only_unsafe_exercises():
    problems = check_class_safety(["hundred", "pulling_straps", "parallel_heels"], ["pregnancy"])
    assert len(problems) == 2
    for problem in problems:
        assert "Parallel Heels" not in problem

def test_no_conditions_means_no_problems():
    problems = check_class_safety(["hundred"], [])
    assert len(problems) == 0


# Both tools together

def test_found_exercises_always_pass_safety_check():
    all_conditions = set()
    for exercise in exercises:
        all_conditions.update(exercise["contraindications"])

    for level in ["beginner", "intermediate", "advanced"]:
        for condition in all_conditions:
            results = find_exercises(level, [condition])
            ids = [exercise["id"] for exercise in results]
            assert check_class_safety(ids, [condition]) == []


# The data

def test_exercise_ids_are_unique():
    ids = [exercise["id"] for exercise in exercises]
    assert len(ids) == len(set(ids))

KNOWN_LEVELS = ["beginner", "intermediate", "advanced"]

KNOWN_CONDITIONS = [
    "achilles_injury",
    "elbow_injury",
    "high_blood_pressure",
    "hip_injury",
    "knee_injury",
    "lower_back_pain",
    "neck_injury",
    "osteoporosis",
    "pregnancy",
    "shoulder_injury",
    "wrist_injury",
]

def test_levels_and_conditions_are_known():
    for exercise in exercises:
        assert exercise["level"] in KNOWN_LEVELS, exercise["id"]
        for condition in exercise["contraindications"]:
            assert condition in KNOWN_CONDITIONS, f"{exercise['id']}: {condition}"
