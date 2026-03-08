# agent/memory.py
import json
import os

MEMORY_FILE = "agent_memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)


def classify_cluster(telemetry):
    """
    Simple telemetry -> cluster classifier. Tune these rules as you like.
    """
    latency = telemetry.get("latency", 0)
    throughput = telemetry.get("throughput", 0)
    routing = telemetry.get("routing_status", "")
    device = telemetry.get("device_health", "")

    if routing == "Flapping":
        return "routing_instability"

    if device == "Critical":
        return "device_failure"

    if latency > 250 and throughput > 4000:
        return "traffic_flood"

    if latency > 120 and throughput < 1000:
        return "network_congestion"

    return "general_issue"


def update_memory(telemetry, tool, success):
    """
    Record an outcome (success True/False) for tool under the telemetry cluster.
    """
    cluster = classify_cluster(telemetry)
    mem = load_memory()

    if cluster not in mem:
        mem[cluster] = {}

    if tool not in mem[cluster]:
        mem[cluster][tool] = {"success": 0, "fail": 0}

    if success:
        mem[cluster][tool]["success"] += 1
    else:
        mem[cluster][tool]["fail"] += 1

    save_memory(mem)


def get_tool_score(telemetry, tool):
    """
    Returns success ratio in [0,1] for (cluster,tool).
    If no history, returns 0.5 as neutral to avoid over-penalizing unknown tools.
    """
    cluster = classify_cluster(telemetry)
    mem = load_memory()

    if cluster not in mem:
        return 0.5

    stats = mem[cluster].get(tool)
    if not stats:
        return 0.5

    success = stats.get("success", 0)
    fail = stats.get("fail", 0)
    total = success + fail

    if total == 0:
        return 0.5

    return success / total


def get_tool_bias(telemetry, tool):
    """
    Convenience alias used by app.run_autonomous_cycle.
    Returns a bias value in [0,1] (success ratio) derived from historical data.
    """
    return get_tool_score(telemetry, tool)