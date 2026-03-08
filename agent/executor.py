from .observer import get_observed_data
from .reasoner import run_analysis
from . import tools

def get_agent_decision(excluded_tools=None):
    """
    Step 1: Observe and Reason.
    Returns the decision (JSON) but DOES NOT execute the tool.
    Accepts excluded_tools to prevent re-selecting rejected actions.
    """
    if excluded_tools is None:
        excluded_tools = []

    # 1. Observe
    observed = get_observed_data()

    # 2. Add available tools (Filter out the excluded ones)
    all_tools = list(tools.AVAILABLE_TOOLS.keys())
    observed["available_tools"] = [t for t in all_tools if t not in excluded_tools]

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