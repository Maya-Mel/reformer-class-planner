# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

An AI agent (Google Gemini with function calling) that plans safe Pilates reformer classes from a plain-language request. The safety logic lives in plain Python code and in data written by an instructor. The model only chooses which tools to call and writes the final class.

## Commands

Setup (Windows, PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

You need a `.env` file in the repo root that contains `GEMINI_API_KEY=...`. It is loaded by `ai_client.py` through python-dotenv.

- `python agent.py`: runs the agent on the sample request in its `__main__` block.
- `python ai_client.py`: a smoke test of the Gemini client.
- `python test_models.py`: shows which Gemini models currently respond. This is a manual check, not a test suite.
- `python planner.py`: runs the older pipeline version. Its AI call is commented out.

The project has no test framework, linter or build step. Run every script from the repo root, because `tools.py` opens `data/exercises.json` with a relative path.

## Architecture

**Data (`data/exercises.json`).** Each exercise has `id`, `name`, `series`, `springs`, `position`, `level`, `body_focus` (list) and `contraindications` (list) fields, plus a `description`. The values in `contraindications` are a fixed snake_case vocabulary, such as `pregnancy`, `knee_injury` and `lower_back_pain`. The `conditions` arguments of the tools must use exactly these strings. The instructor wrote this data, so don't generate or "improve" exercise content.

**Tools (`tools.py`).** These are plain functions that work on the exercise list, which is loaded once when the module is imported. `find_exercises` matches the level exactly (asking for `beginner` returns only beginner exercises) and excludes any exercise that is contraindicated for any condition. `check_class_safety` returns a list of problem strings, and an empty list means the class is safe. Gemini builds each tool's schema from the function's **type hints and docstring**. Editing a signature or a docstring therefore changes what the model sees and how it calls the tool.

**Agent loop (`agent.py`).** Automatic function calling is turned off on purpose. Instead, `run_agent` runs the loop by hand:
1. It sends the whole `contents` history to the model.
2. It appends the model's reply to the history.
3. If the reply has function calls, it runs each one through the `TOOLS` name-to-function map, appends the results as one user turn, and repeats.

The loop stops when the reply has no function calls, or after `MAX_STEPS` (10) steps. A new tool must be added in three places: the import, `config.tools` and the `TOOLS` dict. `SYSTEM_INSTRUCTION` holds the class rules and the safety rules. These include a mandatory `check_class_safety` call before the final answer, a minimum number of exercises per muscle group (checked against `body_focus`), exercise names in English, and cues in natural Hebrew.

**AI client (`ai_client.py`).** It holds one shared `genai.Client` with a 120-second timeout and SDK retries turned off. `generate_with_fallback` tries each model in `MODELS` in order and moves to the next one only on `errors.ServerError` (503/504 errors on the free tier). Other errors, such as an invalid API key, are raised on purpose. Every model call should go through this function.

**`planner.py`** is the older pipeline. Code filters the exercises and passes them to a single prompt, with no tools involved. It is kept so the two approaches can be compared, and it is not used by the agent.

## Rules
- I'm learning. Explain every change in simple terms before making it, and ask before editing files.
- Never change contraindications in data/exercises.json without asking me. I'm the Pilates instructor, and safety data is my decision.
- Every tool in tools.py must keep its type hints and docstring, because the agent reads them.
- Never commit the .env file or any API key.