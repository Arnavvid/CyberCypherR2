from vectordb import add_incident

# -------------------------
# DDoS INCIDENTS
# -------------------------

add_incident(
{"latency":280,"packet_loss":22,"throughput":4800,"device_health":"Healthy","routing_status":"Stable"},
"DDoS attack","enable_ddos_protection", 25
)

add_incident(
{"latency":310,"packet_loss":25,"throughput":5200,"device_health":"Healthy","routing_status":"Stable"},
"DDoS attack","enable_ddos_protection", 20
)

add_incident(
{"latency":250,"packet_loss":18,"throughput":4100,"device_health":"Healthy","routing_status":"Stable"},
"DDoS attack","apply_rate_limiting", 70
)

add_incident(
{"latency":340,"packet_loss":30,"throughput":5600,"device_health":"Healthy","routing_status":"Stable"},
"DDoS attack","enable_ddos_protection", 15
)

add_incident(
{"latency":295,"packet_loss":21,"throughput":4300,"device_health":"Healthy","routing_status":"Stable"},
"DDoS attack","apply_rate_limiting", 80
)

# -------------------------
# FIBER CUT INCIDENTS
# -------------------------

add_incident(
{"latency":20,"packet_loss":100,"throughput":0,"device_health":"Healthy","routing_status":"Unreachable"},
"Fiber cut","escalate_to_engineers", 0
)

add_incident(
{"latency":25,"packet_loss":98,"throughput":0,"device_health":"Healthy","routing_status":"Unreachable"},
"Fiber cut","escalate_to_engineers", 0
)

add_incident(
{"latency":18,"packet_loss":99,"throughput":0,"device_health":"Healthy","routing_status":"Unreachable"},
"Fiber cut","escalate_to_engineers", 0
)

add_incident(
{"latency":30,"packet_loss":100,"throughput":0,"device_health":"Healthy","routing_status":"Unreachable"},
"Fiber cut","reroute_traffic", 20
)

add_incident(
{"latency":18,"packet_loss":99,"throughput":0,"device_health":"Healthy","routing_status":"Unreachable"},
"Fiber cut","reroute_traffic", 10
)

# -------------------------
# FIRMWARE INCIDENTS
# -------------------------

add_incident(
{"latency":35,"packet_loss":6,"throughput":830,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","rollback_firmware", 60
)

add_incident(
{"latency":40,"packet_loss":5,"throughput":850,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","rollback_firmware", 70
)

add_incident(
{"latency":32,"packet_loss":4.5,"throughput":820,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","reset_bgp_session", 90
)

add_incident(
{"latency":32,"packet_loss":4.5,"throughput":820,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","reset_bgp_session", 90
)

add_incident(
{"latency":32,"packet_loss":4.5,"throughput":820,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","reset_bgp_session", 80
)

add_incident(
{"latency":32,"packet_loss":4.5,"throughput":820,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","reset_bgp_session", 70
)

add_incident(
{"latency":38,"packet_loss":5.2,"throughput":840,"device_health":"Critical","routing_status":"Flapping"},
"Firmware corruption","rollback_firmware", 65
)

# -------------------------
# CONGESTION INCIDENTS
# -------------------------

add_incident(
{"latency":120,"packet_loss":2.1,"throughput":720,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","reroute_traffic", 30
)

add_incident(
{"latency":140,"packet_loss":2.5,"throughput":690,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","reroute_traffic", 30
)

add_incident(
{"latency":160,"packet_loss":3,"throughput":710,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","deploy_load_balancer", 60
)

add_incident(
{"latency":180,"packet_loss":3.2,"throughput":650,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","reroute_traffic", 30
)

add_incident(
{"latency":150,"packet_loss":2.8,"throughput":680,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","deploy_load_balancer", 60
)

add_incident(
{"latency":170,"packet_loss":3.1,"throughput":700,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","reroute_traffic", 30
)

add_incident(
{"latency":130,"packet_loss":2.2,"throughput":740,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","reroute_traffic", 30
)

add_incident(
{"latency":145,"packet_loss":2.6,"throughput":720,"device_health":"Healthy","routing_status":"Stable"},
"Network congestion","deploy_load_balancer", 60
)

# -------------------------
# BGP ROUTE LEAK INCIDENTS
# -------------------------

add_incident(
{"latency":280,"packet_loss":8,"throughput":750,"device_health":"Healthy","routing_status":"Flapping"},
"BGP Route Leak","reset_bgp_session", 90
)

add_incident(
{"latency":310,"packet_loss":9,"throughput":700,"device_health":"Healthy","routing_status":"Flapping"},
"BGP Route Leak","reset_bgp_session", 85
)

add_incident(
{"latency":260,"packet_loss":7.5,"throughput":780,"device_health":"Healthy","routing_status":"Flapping"},
"BGP Route Leak","reset_bgp_session", 90
)

add_incident(
{"latency":290,"packet_loss":8.2,"throughput":720,"device_health":"Healthy","routing_status":"Flapping"},
"BGP Route Leak","reset_bgp_session", 85
)

# -------------------------
# BROADCAST STORM INCIDENTS
# -------------------------

add_incident(
{"latency":90,"packet_loss":14,"throughput":2200,"device_health":"Degraded","routing_status":"Stable"},
"Broadcast Storm","apply_rate_limiting", 45
)

add_incident(
{"latency":85,"packet_loss":12,"throughput":2100,"device_health":"Degraded","routing_status":"Stable"},
"Broadcast Storm","apply_rate_limiting", 40
)

add_incident(
{"latency":95,"packet_loss":16,"throughput":2400,"device_health":"Degraded","routing_status":"Stable"},
"Broadcast Storm","apply_rate_limiting", 50
)

add_incident(
{"latency":100,"packet_loss":15,"throughput":2300,"device_health":"Degraded","routing_status":"Stable"},
"Broadcast Storm","apply_rate_limiting", 45
)

add_incident(
{"latency":88,"packet_loss":13,"throughput":2150,"device_health":"Degraded","routing_status":"Stable"},
"Broadcast Storm","apply_rate_limiting", 40
)