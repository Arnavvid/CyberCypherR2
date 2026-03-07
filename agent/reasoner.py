# agent/reasoner.py
import json
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from .vectordb import search_similar
from . import tools 

class ReasonerOutput(BaseModel):
    tool: str = Field(description="The exact name of the tool to use")
    thought: str = Field(description="Reasoning behind the decision")
    risk: int = Field(description="Risk level from 0 to 100")

def run_analysis(observed_data: dict):

    telemetry = observed_data["telemetry"]
    allowed_tools = observed_data["available_tools"]
    similar_incidents = search_similar(telemetry)
    # 1. Setup Model
    llm = ChatOllama(
        model="qwen2.5:7b", 
        temperature=0
    )

    tools_list_str = ", ".join(f"'{t}'" for t in allowed_tools)

    incident_context = ""
    for i, inc in enumerate(similar_incidents):
        risk_score = inc.get('risk', 'Unknown')
        incident_context += f"""
        Incident {i+1}

        Telemetry:
        {inc['text']}

        Diagnosis:
        {inc['diagnosis']}

        Tool Used:
        {inc['tool']}

        Resulting Risk Score: 
        {risk_score}
        """

    prompt = f"""
    You are a Network Operations AI.

    CURRENT TELEMETRY:
    {json.dumps(telemetry, indent=2)}

    SIMILAR HISTORICAL INCIDENTS:
    {incident_context}

    AVAILABLE TOOLS:
    [{tools_list_str}]

    INSTRUCTIONS:
    1. Compare the CURRENT TELEMETRY with the historical incidents.
    2. Identify the most likely network issue.
    3. Select the correct tool to fix the issue.
    4. Output valid JSON.
    """

    structured_llm = llm.with_structured_output(ReasonerOutput)

    try:
        result = structured_llm.invoke(prompt)
        
        # ... (Same safe conversion logic as before) ...
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result

        # --- The Enforcer ---
        selected_tool = result_dict.get("tool")
        if selected_tool not in allowed_tools:
            print(f"!!! SYSTEM INTERCEPTION !!! AI tried to use fake tool: '{selected_tool}'")
            result_dict["tool"] = "escalate_to_engineers"
            result_dict["thought"] += " [System Auto-Correction: Invalid Tool]"
            result_dict["risk"] = 100

        return result_dict

    except Exception as e:
        print(f"AI ERROR: {e}")
        return {
            "tool": "escalate_to_engineers", 
            "thought": f"AI Crash: {str(e)}", 
            "risk": 100
        }