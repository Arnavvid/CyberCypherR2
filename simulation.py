import random
import time

# --- CONFIGURATION: Define your problems here ---
PROBLEM_CATALOG = {
    "congestion": {
        "name": "Network Congestion",
        "description": "Simulates high traffic causing lag.",
        "color": "orange",
        "effects": {
            "latency": 150,          # Adds 150ms
            "link_utilization": 95,  # Sets to 95%
            "throughput": -500,       # Drops throughput slightly
            "packet_loss": 2.5       # Added small loss to make it detectable
        }
    },
    "ddos_attack": {
        "name": "DDoS Attack",
        "description": "Massive traffic spike and packet loss.",
        "color": "red",
        "effects": {
            "throughput": 5000,      # Adds 5000 Mbps (Massive spike)
            "packet_loss": 25.0,     # Adds 25% loss
            "latency": 300,
            "link_utilization": 100
        }
    },
    "firmware_corruption": {
        "name": "Firmware Corruption",
        "description": "Destabilizes device health and routing.",
        "color": "purple",
        "effects": {
            "packet_loss": 5.0,
            "device_health": "Critical", 
            "routing_status": "Flapping" 
        }
    },
    "fiber_cut": {
        "name": "Fiber Optic Cut",
        "description": "Complete physical link failure.",
        "color": "#34495e",
        "effects": {
            # These are placeholders. 
            # The 'Final Override' logic below guarantees 0 throughput.
            "throughput": -10000, 
            "packet_loss": 100,
            "routing_status": "Unreachable"
        }
    }
}

# Global State
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
    
    # 1. Start with Base Random Noise
    data = {
        "latency": max(5, base["latency"] + random.randint(-2, 2)),
        "packet_loss": max(0, base["packet_loss"] + random.uniform(-0.05, 0.05)),
        "throughput": max(0, base["throughput"] + random.randint(-20, 20)),
        "link_utilization": max(0, min(100, base["link_utilization"] + random.randint(-2, 2))),
        "device_health": "Healthy",
        "routing_status": "Stable"
    }

    # 2. Dynamic Rules Engine (Apply Catalog Effects)
    for problem_id in base["active_problems"]:
        if problem_id in PROBLEM_CATALOG:
            effects = PROBLEM_CATALOG[problem_id]["effects"]
            
            for param, value in effects.items():
                if isinstance(value, str):
                    data[param] = value
                else:
                    # Accumulate numeric values
                    if param in ["link_utilization", "packet_loss"]:
                        data[param] = min(100, max(0, data[param] + value))
                    elif param == "throughput":
                         data[param] = max(0, data[param] + value)
                    else:
                        data[param] += value

    # 3. FINAL OVERRIDES (The "Hard Truth" Logic)
    # This ensures critical failures look exactly as they should, 
    # overriding any noise or accumulation errors from above.
    
    if "fiber_cut" in base["active_problems"]:
        data["throughput"] = 0        # Force Hard Down
        data["packet_loss"] = 100     # Force Total Loss
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