from mcp.server.mcpserver import MCPServer

from tools import find_exercises, get_exercise_details, check_class_safety

mcp = MCPServer("reformer-class-planner")

mcp.add_tool(find_exercises)
mcp.add_tool(get_exercise_details)
mcp.add_tool(check_class_safety)

if __name__ == "__main__":
    mcp.run()