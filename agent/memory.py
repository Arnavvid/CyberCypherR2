import json
import os

MEMORY_FILE = "agent_memory.json"

# Default memory
DEFAULT_MEMORY = {
    "reroute_traffic": 0,
    "deploy_load_balancer": 0,
    "enable_ddos_protection": 0,
    "apply_rate_limiting": 0,
    "rollback_firmware": 0,
    "reset_bgp_session": 0,
    "escalate_to_engineers": 0
}

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY.copy()

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(mem):

    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)


def update_memory(tool, delta):

    mem = load_memory()

    if tool not in mem:
        mem[tool] = 0

    mem[tool] += delta

    save_memory(mem)


def get_tool_bias(tool):

    mem = load_memory()

    return mem.get(tool, 0)