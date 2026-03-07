import json
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.tools import StructuredTool
from . import tools


class ReasonerOutput(BaseModel):
    tool: str = Field(description="Name of the tool to execute")
    thought: str = Field(description="Reasoning behind the decision")
    risk: int = Field(description="Risk level from 0 to 100")


def build_tools(allowed_tools):

    tool_objects = []

    for name in allowed_tools:
        if name in tools.AVAILABLE_TOOLS:

            func = tools.AVAILABLE_TOOLS[name]

            tool_objects.append(
                StructuredTool.from_function(
                    func=func,
                    name=name,
                    description=f"Network operation tool: {name}"
                )
            )

    return tool_objects


def run_analysis(observed_data: dict):

    telemetry = observed_data["telemetry"]
    allowed_tools = observed_data["available_tools"]

    llm = ChatOllama(
        model="qwen3.5:9b",
        temperature=0
    )

    tool_objects = build_tools(allowed_tools)

    llm_with_tools = llm.bind_tools(tool_objects)

    structured_llm = llm_with_tools.with_structured_output(ReasonerOutput)

    prompt = f"""
    Analyze this network telemetry and determine the most likely issue.

    Telemetry:
    {json.dumps(telemetry, indent=2)}

    Choose the best tool to fix the issue.
    Only select from the provided tools.

    Estimate risk between 0 and 100.
    """

    result = structured_llm.invoke(prompt)

    if hasattr(result, "model_dump"):
        result_dict = result.model_dump()
    elif isinstance(result, dict):
        result_dict = result
    else:
        # Fallback if the AI hallucinates an invalid format
        result_dict = {"tool": "escalate_to_engineers", "thought": "Parsing failed.", "risk": 100}

    return result_dict