import random
import time
import json
import os

def load_problem_catalog():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'dummy', 'problems.json')
        
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading problems.json: {e}")
        return {}

PROBLEM_CATALOG = load_problem_catalog()

network_state = {
    "latency": 25,
    "packet_loss": 0.05,
    "throughput": 850,
    "link_utilization": 45,
    "device_health": "Healthy",
    "routing_status": "Stable",
    "active_problems": [],
    "ai_logs": []
}

def get_live_data():
    base = network_state
    
    data = {
        "latency": max(5, base["latency"] + random.randint(-2, 2)),
        "packet_loss": max(0, base["packet_loss"] + random.uniform(-0.05, 0.05)),
        "throughput": max(0, base["throughput"] + random.randint(-20, 20)),
        "link_utilization": max(0, min(100, base["link_utilization"] + random.randint(-2, 2))),
        "device_health": "Healthy",
        "routing_status": "Stable"
    }

    for problem_id in base["active_problems"]:
        if problem_id in PROBLEM_CATALOG:
            effects = PROBLEM_CATALOG[problem_id]["effects"]
            
            for param, value in effects.items():
                if isinstance(value, str):
                    data[param] = value
                else:
                    if param in ["link_utilization", "packet_loss"]:
                        data[param] = min(100, max(0, data[param] + value))
                    elif param == "throughput":
                         data[param] = max(0, data[param] + value)
                    else:
                        data[param] += value

    if "fiber_cut" in base["active_problems"]:
        data["throughput"] = 0
        data["packet_loss"] = 100
        data["routing_status"] = "Unreachable"

    if "firmware_corruption" in base["active_problems"]:
        data["device_health"] = "Critical"
        data["routing_status"] = "Flapping"

    return data

def inject_problem(problem_id):
    if problem_id in PROBLEM_CATALOG and problem_id not in network_state["active_problems"]:
        network_state["active_problems"].append(problem_id)

def resolve_problem(problem_id):
    if problem_id in network_state["active_problems"]:
        network_state["active_problems"].remove(problem_id)
        return True
    return False

def log_ai_action(thought, tool_name, risk, status):
    entry = {
        "timestamp": time.strftime("%H:%M:%S"),
        "thought": thought,
        "action": tool_name,
        "risk": risk,
        "status": status
    }
    network_state["ai_logs"].insert(0, entry)