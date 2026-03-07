from flask import Flask, render_template, jsonify, request
import simulation
import agent.tools as tools
from agent.memory import get_tool_bias, update_memory
import requests 
import json
# Import the new split functions
from agent.executor import get_agent_decision, execute_tool

RISK_THRESHOLD = 50

app = Flask(__name__)

# !!! UPDATE THIS TO YOUR PARTNER'S URL !!!
ACTIVE_PROBLEMS = "http://localhost:5000/api/run_agent"

# --- Pages ---
@app.route('/')
def index(): return render_template('status.html')

@app.route('/test')
def test_page(): return render_template('test.html')

@app.route('/admin')
def admin_page(): return render_template('admin.html')

@app.route('/api/problems')
def get_problems():
    return jsonify(simulation.PROBLEM_CATALOG)

@app.route("/api/active_symptoms")
def active_symptoms():
    data = simulation.get_live_data()
    return jsonify({
        "telemetry": {
            "latency": data["latency"],
            "packet_loss": data["packet_loss"],
            "throughput": data["throughput"],
            "device_health": data["device_health"],
            "routing_status": data["routing_status"]
        }
    })

@app.route("/api/run_agent", methods=["POST"])
def run_agent_endpoint():
    # 1. THINK: Get the decision ONLY (No execution yet)
    decision = get_agent_decision()

    tool = decision.get("tool")
    thought = decision.get("thought")
    risk = decision.get("risk", 0)

    # Apply reinforcement learning bias
    bias = get_tool_bias(tool)
    risk = max(0, min(100, risk - (bias * 10)))

    # 2. CHECK RISK
    if risk > RISK_THRESHOLD:
        # HIGH RISK: Stop here. Log as Pending. Do NOT execute.
        simulation.log_ai_action(
            thought,
            tool,
            risk,
            "Pending Approval"
        )
        return jsonify({
            "decision": decision,
            "execution_result": "Awaiting admin approval"
        })

    # 3. LOW RISK: Execute immediately.
    result = execute_tool(tool)
    
    simulation.log_ai_action(
        thought,
        tool,
        risk,
        "Executed"
    )

    return jsonify({
        "decision": decision,
        "execution_result": result
    })

@app.route("/api/approve_action", methods=["POST"])
def approve_action():
    data = request.json
    tool_name = data.get("tool")

    if tool_name in tools.AVAILABLE_TOOLS:
        # 1. Execute the tool now
        result = execute_tool(tool_name)
        update_memory(tool_name, +1)
        # 2. Find and Update the existing 'Pending' log
        # This prevents duplicate rows in the Admin panel
        found = False
        for log in simulation.network_state["ai_logs"]:
            if log["action"] == tool_name and log["status"] == "Pending Approval":
                log["status"] = "Executed"
                log["thought"] += " [Admin Approved]"
                found = True
                break  # Update only the most recent pending one

        if not found:
            # Fallback if logs were cleared
            simulation.log_ai_action("Manual Approval", tool_name, 0, "Executed")

        return jsonify({"result": result})

    return jsonify({"error": "Invalid tool"})


@app.route("/api/reject_action", methods=["POST"])
def reject_action():

    data = request.json
    tool_name = data.get("tool")

    update_memory(tool_name, -1)

    for log in simulation.network_state["ai_logs"]:
        if log["action"] == tool_name and log["status"] == "Pending Approval":
            log["status"] = "Rejected"
            log["thought"] += " [Admin Rejected]"
            break

    return jsonify({"status": "rejected"})

@app.route('/api/status')
def get_status():
    return jsonify(simulation.get_live_data())

@app.route('/api/logs')
def get_logs():
    return jsonify(simulation.network_state["ai_logs"])

# --- THE TRIGGER LOGIC ---
@app.route('/api/trigger_scenario', methods=['POST'])
def trigger_scenario():
    problem = request.json.get('problem')
    
    # A. Inject
    simulation.inject_problem(problem)
    
    # B. Run the endpoint logic internally
    # We call the same logic as the /api/run_agent endpoint to ensure consistency
    try:
        # 1. Think
        decision = get_agent_decision()
        tool_name = decision.get("tool")
        thought = decision.get("thought")
        risk = decision.get("risk", 0)

        # 2. Risk Check
        if risk > RISK_THRESHOLD:
            simulation.log_ai_action(thought, tool_name, risk, "Pending Approval")
            return jsonify({
                "decision": decision,
                "execution_result": "Awaiting admin approval"
            })
        
        # 3. Execute
        result = execute_tool(tool_name)
        simulation.log_ai_action(thought, tool_name, risk, "Executed")

        return jsonify({
            "decision": decision,
            "execution_result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)