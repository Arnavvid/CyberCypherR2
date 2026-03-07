from .observer import get_observed_data
from .reasoner import run_analysis
from . import tools

def get_agent_decision():
    """
    Step 1: Observe and Reason.
    Returns the decision (JSON) but DOES NOT execute the tool.
    """
    # 1. Observe
    observed = get_observed_data()

    # 2. Add available tools
    observed["available_tools"] = list(tools.AVAILABLE_TOOLS.keys())

    # 3. Reason
    decision = run_analysis(observed)
    
    return decision

def execute_tool(tool_name):
    """
    Step 2: Execute the tool.
    Only called if risk is low OR admin approves.
    """
    if tool_name in tools.AVAILABLE_TOOLS:
        return tools.AVAILABLE_TOOLS[tool_name]()
    
    return "No valid tool selected"