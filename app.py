from flask import Flask, render_template, jsonify, request
import simulation
import agent.tools as tools
from agent.memory import get_tool_bias, update_memory
from agent.observer import get_observed_data
import json
from agent.executor import get_agent_decision, execute_tool

RISK_THRESHOLD = 50

app = Flask(__name__)


def run_autonomous_cycle(excluded_tools=None):
    """
    Encapsulates the full agent lifecycle:
    Think -> Apply Bias -> Check Risk -> Execute or Pend
    """
    observed = get_observed_data()
    telemetry = observed.get("telemetry", {})

    decision = get_agent_decision(excluded_tools)

    tool = decision.get("tool")
    thought = decision.get("thought")
    risk = decision.get("risk", 0)

    bias = get_tool_bias(telemetry, tool)

    risk = max(0, min(100, int(risk - (bias * 10))))

    if risk > RISK_THRESHOLD:
        simulation.log_ai_action(
            thought,
            tool,
            risk,
            "Pending Approval"
        )
        return {
            "decision": decision,
            "execution_result": "Awaiting admin approval"
        }

    result = execute_tool(tool)

    simulation.log_ai_action(
        thought,
        tool,
        risk,
        "Executed"
    )

    return {
        "decision": decision,
        "execution_result": result
    }


@app.route('/')
def index():
    return render_template('status.html')


@app.route('/test')
def test_page():
    return render_template('test.html')


@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route('/api/problems')
def get_problems():
    return jsonify(simulation.PROBLEM_CATALOG)


@app.route('/api/active_problems')
def get_active_problems():
    return jsonify(simulation.network_state.get("active_problems", []))


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
    result = run_autonomous_cycle()
    return jsonify(result)


@app.route("/api/approve_action", methods=["POST"])
def approve_action():
    data = request.json
    tool_name = data.get("tool")

    if tool_name in tools.AVAILABLE_TOOLS:
        result = execute_tool(tool_name)

        observed = get_observed_data()
        telemetry = observed.get("telemetry", {})
        update_memory(telemetry, tool_name, True)

        found = False
        for log in simulation.network_state["ai_logs"]:
            if log["action"] == tool_name and log["status"] == "Pending Approval":
                log["status"] = "Executed"
                log["thought"] += " [Admin Approved]"
                found = True
                break

        if not found:
            simulation.log_ai_action("Manual Approval", tool_name, 0, "Executed")

        return jsonify({"result": result})

    return jsonify({"error": "Invalid tool"})


@app.route("/api/reject_action", methods=["POST"])
def reject_action():
    data = request.json
    tool_name = data.get("tool")

    observed = get_observed_data()
    telemetry = observed.get("telemetry", {})
    update_memory(telemetry, tool_name, False)

    for log in simulation.network_state["ai_logs"]:
        if log["action"] == tool_name and log["status"] == "Pending Approval":
            log["status"] = "Rejected"
            log["thought"] += " [Admin Rejected]"
            break

    print(f"!!! Re-running Agent excluding: {tool_name} !!!")

    retry_result = run_autonomous_cycle(excluded_tools=[tool_name])

    retry_decision = retry_result.get("decision", {})

    simulation.log_ai_action(
        retry_decision.get("thought", "Retrying decision"),
        retry_decision.get("tool", "unknown"),
        retry_decision.get("risk", 0),
        "Pending Approval"
    )

    return jsonify({
        "status": "rejected",
        "retry_decision": retry_result
    })


@app.route('/api/status')
def get_status():
    return jsonify(simulation.get_live_data())


@app.route('/api/logs')
def get_logs():
    return jsonify(simulation.network_state["ai_logs"])


@app.route('/api/trigger_scenario', methods=['POST'])
def trigger_scenario():
    problem = request.json.get('problem')
    simulation.inject_problem(problem)

    try:
        result = run_autonomous_cycle()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)