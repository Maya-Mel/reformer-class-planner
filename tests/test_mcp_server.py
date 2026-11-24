import asyncio

from mcp_server import mcp


def test_mcp_server_has_the_three_tools():
    tools = asyncio.run(mcp.list_tools())
    names = {tool.name for tool in tools}
    assert names == {"find_exercises", "get_exercise_details", "check_class_safety"}


def test_mcp_safety_check_finds_a_problem():
    result = asyncio.run(mcp.call_tool(
        "check_class_safety",
        {"exercise_ids": ["hundred"], "conditions": ["pregnancy"]},
    ))
    assert len(result.structured_content["result"]) == 1