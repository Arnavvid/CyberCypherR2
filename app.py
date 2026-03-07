from flask import Flask, render_template, jsonify, request
import simulation
import tools
import requests 
import json

app = Flask(__name__)

# !!! UPDATE THIS TO YOUR PARTNER'S URL !!!
# Example: "http://192.168.1.5:8000/analyze_network"
PARTNER_AI_URL = "http://localhost:5000/api/post_solution" 

# --- Pages ---
@app.route('/')
def index(): return render_template('status.html')

@app.route('/test')
def test_page(): return render_template('test.html')

@app.route('/admin')
def admin_page(): return render_template('admin.html')

# --- APIs ---
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
    
    # C. Prepare Payload (Raw JSON)
    # This is exactly what your partner will receive
    payload = {
        "telemetry": {
            "latency": data['latency'],
            "packet_loss": data['packet_loss'],
            "throughput": data['throughput'],
            "device_health": data['device_health'],
            "routing_status": data['routing_status']
        },
        "available_tools": list(tools.AVAILABLE_TOOLS.keys())
    }

    # D. Send to Partner
    try:
        # Sending the POST request
        response = requests.post(PARTNER_AI_URL, json=payload, timeout=5)
        
        # Expecting Partner to return: {"tool": "name", "risk": 0-100, "thought": "..."}
        ai_response = response.json() 
        
        # E. Execute their decision
        tool_name = ai_response.get("tool")
        risk = ai_response.get("risk", 0)
        thought = ai_response.get("thought", "External AI Decision")

        if tool_name in tools.AVAILABLE_TOOLS:
            if risk > 50:
                status = "Pending Approval"
                simulation.log_ai_action(thought, tool_name, risk, status)
                return jsonify({"status": "Queued", "message": "High risk action queued."})
            else:
                result = tools.AVAILABLE_TOOLS[tool_name]()
                simulation.log_ai_action(thought, tool_name, risk, "Executed")
                return jsonify({"status": "Executed", "output": result, "ai_thought": thought})
        else:
            return jsonify({"error": f"AI suggested unknown tool: {tool_name}"})

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Partner AI is offline. Check URL."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)