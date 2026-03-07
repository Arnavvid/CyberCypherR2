from .observer import get_observed_data
from .reasoner import run_analysis
from . import tools


def run_agent():

    # 1. Observe
    observed = get_observed_data()

    # 2. Add available tools
    observed["available_tools"] = list(tools.AVAILABLE_TOOLS.keys())

    # 3. Reason
    decision = run_analysis(observed)

    tool_name = decision.get("tool")

    # 4. Execute
    if tool_name in tools.AVAILABLE_TOOLS:

        result = tools.AVAILABLE_TOOLS[tool_name]()

        return {
            "decision": decision,
            "execution_result": result
        }

    return {
        "decision": decision,
        "execution_result": "No valid tool selected"
    }