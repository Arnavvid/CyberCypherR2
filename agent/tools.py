import simulation
import time

def reroute_traffic():
    time.sleep(1)

    if simulation.resolve_problem("fiber_cut"):
        return "Rerouted to another available working line."

    elif simulation.resolve_problem("congestion"):
        return "Traffic shifted to backup link."

    elif simulation.resolve_problem("bgp_leak"):
        return "Traffic temporarily rerouted while invalid routes are bypassed."

    return "Traffic rerouting attempted, but no routing issues were active."

def enable_ddos_protection():
    time.sleep(1.5)
    simulation.resolve_problem("ddos_attack")
    return "Scrubbing center activated. Bad traffic dropped."

def rollback_firmware():
    time.sleep(2)
    simulation.resolve_problem("firmware_corruption")
    return "Firmware rolled back to v4.2.1-stable."

def escalate_to_engineers():
    time.sleep(1)

    if simulation.resolve_problem("fiber_cut"):
        return "Fiber cut escalated. Field engineers dispatched."

    elif simulation.resolve_problem("firmware_corruption"):
        return "Firmware issue escalated to vendor support team."

    elif simulation.resolve_problem("bgp_leak"):
        return "Routing anomaly escalated to NOC engineers."

    return "Incident escalated to engineering team."

def deploy_load_balancer():
    """Fixes High Link Utilization without full reroute"""
    time.sleep(1)
    simulation.resolve_problem("congestion") 
    return "L7 Load Balancer deployed. Traffic distributed."

def reset_bgp_session():
    """Fixes Routing Flapping and BGP Leaks"""
    time.sleep(3)
    if simulation.resolve_problem("firmware_corruption"):
        return "BGP Session hard reset. Routes re-advertised."
    if simulation.resolve_problem("bgp_leak"):
        return "BGP Session cleared. Invalid routes flushed."
    return "BGP Reset attempted (No active BGP issues found)."

def apply_rate_limiting():
    """Fixes mild DDoS or Broadcast Storms"""
    time.sleep(0.5)
    if simulation.resolve_problem("broadcast_storm"):
        return "Rate limiting applied. Broadcast storm suppressed."
    if simulation.resolve_problem("ddos_attack"):
        return "Rate limiting applied to /24 subnet."
    return "Rate limiting applied."

AVAILABLE_TOOLS = {
    "reroute_traffic": reroute_traffic,
    "enable_ddos_protection": enable_ddos_protection,
    "rollback_firmware": rollback_firmware,
    "escalate_to_engineers": escalate_to_engineers,
    "deploy_load_balancer": deploy_load_balancer,
    "reset_bgp_session": reset_bgp_session,
    "apply_rate_limiting": apply_rate_limiting
}