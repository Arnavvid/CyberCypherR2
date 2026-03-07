import requests

SYMPTOM_URL = "http://localhost:5000/api/active_symptoms"


def get_observed_data():

    try:
        response = requests.get(SYMPTOM_URL, timeout=3)
        data = response.json()

        return {
            "telemetry": data["telemetry"]
        }

    except Exception:
        return {
            "telemetry": {
                "latency": 0,
                "packet_loss": 0,
                "throughput": 0,
                "device_health": "Unknown",
                "routing_status": "Unknown"
            }
        }