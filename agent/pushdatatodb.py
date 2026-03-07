from vectordb import add_incident

add_incident(
    {
        "latency": 320,
        "packet_loss": 28,
        "throughput": 5200,
        "device_health": "Healthy",
        "routing_status": "Stable"
    },
    "DDoS attack",
    "enable_ddos_protection"
)

add_incident(
    {
        "latency": 30,
        "packet_loss": 100,
        "throughput": 0,
        "device_health": "Healthy",
        "routing_status": "Unreachable"
    },
    "Fiber cut",
    "escalate_to_engineers"
)

add_incident(
    {
        "latency": 150,
        "packet_loss": 3,
        "throughput": 700,
        "device_health": "Healthy",
        "routing_status": "Stable"
    },
    "Network congestion",
    "reroute_traffic"
)

add_incident(
    {
        "latency": 40,
        "packet_loss": 5,
        "throughput": 850,
        "device_health": "Critical",
        "routing_status": "Flapping"
    },
    "Firmware corruption",
    "rollback_firmware"
)