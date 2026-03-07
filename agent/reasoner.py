# agent/reasoner.py
import json
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from . import tools 

class ReasonerOutput(BaseModel):
    tool: str = Field(description="The exact name of the tool to use")
    thought: str = Field(description="Reasoning behind the decision")
    risk: int = Field(description="Risk level from 0 to 100")

def run_analysis(observed_data: dict):

    telemetry = observed_data["telemetry"]
    allowed_tools = observed_data["available_tools"]

    # 1. Setup Model
    llm = ChatOllama(
        model="qwen2.5:7b", 
        temperature=0
    )

    tools_list_str = ", ".join(f"'{t}'" for t in allowed_tools)

    # --- THE TUNED CHEAT SHEET ---
    prompt = f"""
    You are a Network Operations AI.
    
    CURRENT TELEMETRY DATA:
    {json.dumps(telemetry, indent=2)}

    AVAILABLE TOOLS:
    [{tools_list_str}]

    --- REFERENCE RANGES (NORMAL) ---
    - Latency: 20-30 ms
    - Packet Loss: 0-1%
    - Throughput: 800-900 Mbps
    - Device Health: "Healthy"

    --- DIAGNOSTIC RULES (EVALUATE EACH) ---
    
    [RULE 1] DDoS CHECK
    IF (Throughput > 2000 Mbps) -> DIAGNOSIS: DDoS -> ACTION: 'enable_ddos_protection'

    [RULE 2] FIRMWARE CHECK
    IF (Device Health == "Critical" OR Routing Status == "Flapping") -> DIAGNOSIS: Firmware Corruption -> ACTION: 'rollback_firmware'

    [RULE 3] FIBER CUT CHECK
    IF (Throughput == 0 OR Packet Loss == 100) -> DIAGNOSIS: Fiber Cut -> ACTION: 'escalate_to_engineers'

    [RULE 4] CONGESTION CHECK
    IF (Latency > 100 ms AND Throughput < 1500) -> DIAGNOSIS: Congestion -> ACTION: 'reroute_traffic'

    -----------------------------------

    INSTRUCTIONS:
    1. FIRST, analyze the CURRENT TELEMETRY against the REFERENCE RANGES.
    2. SECOND, go through Rules 1-4 and find which specific condition is TRUE.
    3. IGNORE rules where the condition is FALSE.
    4. Select the tool corresponding to the TRUE rule.
    5. Output valid JSON only.
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