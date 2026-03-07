from flask import Flask, render_template, jsonify, request
import simulation
import agent.tools as tools
import requests 
import json
from agent.executor import run_agent

RISK_THRESHOLD = 50

app = Flask(__name__)

# !!! UPDATE THIS TO YOUR PARTNER'S URL !!!
# Example: "http://192.168.1.5:8000/analyze_network"
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
    """Returns the list of available chaos scenarios to the frontend."""
    return jsonify(simulation.PROBLEM_CATALOG)


# --- APIs ---
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

    result = run_agent()

    decision = result["decision"]

    thought = decision.get("thought")
    tool = decision.get("tool")
    risk = decision.get("risk")

    # HIGH RISK → require approval
    if risk > RISK_THRESHOLD:

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

    # LOW RISK → auto execute
    simulation.log_ai_action(
        thought,
        tool,
        risk,
        "Executed"
    )

    return jsonify(result)

@app.route("/api/approve_action", methods=["POST"])
def approve_action():

    data = request.json
    tool_name = data.get("tool")

    if tool_name in tools.AVAILABLE_TOOLS:

        result = tools.AVAILABLE_TOOLS[tool_name]()

        simulation.log_ai_action(
            "Admin approved action",
            tool_name,
            0,
            "Executed"
        )

        return jsonify({"result": result})

    return jsonify({"error": "Invalid tool"})


@app.route('/api/status')
def get_status():
    return jsonify(simulation.get_live_data())

@app.route('/api/logs')
def get_logs():
    return jsonify(simulation.network_state["ai_logs"])

# --- THE TRIGGER LOGIC ---
@app.route('/api/trigger_scenario', methods=['POST'])
def trigger_scenario():
    """
    1. Injects the fault.
    2. Gathers raw telemetry data.
    3. POSTs raw JSON to Partner AI.
    4. Executes Partner's response.
    """
    problem = request.json.get('problem')
    
    # A. Inject the problem
    simulation.inject_problem(problem)
    
    # B. Gather the "Bad" Data
    data = simulation.get_live_data() 
    
    # D. Run the local AI agent
    try:
        result = run_agent()

        decision = result["decision"]

        tool_name = decision.get("tool")
        thought = decision.get("thought")
        risk = decision.get("risk")

        simulation.log_ai_action(thought, tool_name, risk, "Executed")

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)