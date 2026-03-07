import random
import time

# Global State
network_state = {
    "latency": 25,           # ms
    "packet_loss": 0.05,     # %
    "throughput": 850,       # Mbps
    "link_utilization": 45,  # %
    "device_health": "Healthy",
    "routing_status": "Stable",
    "active_problems": [],
    "ai_logs": []
}

def get_live_data():
    base = network_state
    
    # 1. Base Noise (Keep this)
    data = {
        "latency": max(5, base["latency"] + random.randint(-2, 2)),
        "packet_loss": max(0, base["packet_loss"] + random.uniform(-0.05, 0.05)),
        "throughput": max(0, base["throughput"] + random.randint(-20, 20)),
        "link_utilization": max(0, min(100, base["link_utilization"] + random.randint(-2, 2))),
        "device_health": base["device_health"],
        "routing_status": base["routing_status"]
    }
    
    # 2. Apply Problem Effects (OVERRIDES)
    
    # Congestion adds to existing values
    if "congestion" in base["active_problems"]:
        data["latency"] += random.randint(100, 150)
        data["link_utilization"] = random.randint(95, 99)
        data["packet_loss"] += random.uniform(1.0, 3.0) 

    # DDoS adds massive throughput
    if "ddos_attack" in base["active_problems"]:
        data["throughput"] += 5000 
        data["latency"] += 300
        data["packet_loss"] += random.uniform(15, 25)
        data["link_utilization"] = 100

    # Firmware sets critical flags
    if "firmware_corruption" in base["active_problems"]:
        data["device_health"] = "Critical"
        data["packet_loss"] += random.uniform(2, 8)
        data["routing_status"] = "Flapping"

    # Fiber Cut MUST be last to overwrite everything else with 0/100
    if "fiber_cut" in base["active_problems"]:
        data["throughput"] = 0        # HARD ZERO
        data["packet_loss"] = 100     # HARD 100%
        data["routing_status"] = "Unreachable"

    return data

def inject_problem(problem_type):
    if problem_type not in network_state["active_problems"]:
        network_state["active_problems"].append(problem_type)

def resolve_problem(problem_type):
    if problem_type in network_state["active_problems"]:
        network_state["active_problems"].remove(problem_type)
        # Reset specific flags if needed
        if problem_type == "firmware_corruption":
            network_state["device_health"] = "Healthy"
            network_state["routing_status"] = "Stable"
        if problem_type == "fiber_cut":
            network_state["routing_status"] = "Stable"
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