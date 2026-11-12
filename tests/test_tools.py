from tools import find_exercises, check_class_safety


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


