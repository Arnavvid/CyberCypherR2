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
    
    CURRENT TELEMETRY:
    {json.dumps(telemetry, indent=2)}

    AVAILABLE TOOLS:
    [{tools_list_str}]

    --- DIAGNOSTIC LOGIC (FOLLOW STRICTLY) ---
    
    1. CHECK FOR FIBER CUT (Priority #1):
       - RULE: Is Throughput == 0 OR Packet Loss == 100%?
       - DIAGNOSIS: Fiber Cut (Hard Down).
       - ACTION: 'escalate_to_engineers'.

    2. CHECK FOR DDoS ATTACK (Priority #2):
       - RULE: Is Throughput > 2000 Mbps? (Normal is ~850).
       - DIAGNOSIS: DDoS Attack (Volumetric).
       - ACTION: 'enable_ddos_protection' OR 'apply_rate_limiting'.

    3. CHECK FOR FIRMWARE FAILURE (Priority #3):
       - RULE: Is Device Health 'Critical' OR Routing Status 'Flapping'?
       - DIAGNOSIS: Firmware Corruption.
       - ACTION: 'rollback_firmware'.

    4. CHECK FOR CONGESTION (Priority #4):
       - RULE: Is Latency > 100ms BUT Throughput is normal (<1500)?
       - DIAGNOSIS: Network Congestion.
       - ACTION: 'reroute_traffic' OR 'deploy_load_balancer'.

    -----------------------------------

    INSTRUCTIONS:
    1. Go through the priorities 1 to 4 in order.
    2. Pick the FIRST matching diagnosis.
    3. Select the "ACTION" for that diagnosis.
    4. You MUST pick exactly one tool from the AVAILABLE TOOLS list.
    5. Output JSON only.
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