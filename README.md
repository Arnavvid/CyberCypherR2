# CyberCypher: Autonomous Network Remediation Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange.svg)
![ChromaDB](https://img.shields.io/badge/VectorDB-Chroma-purple.svg)

CyberCypher is a self-healing network operations system that utilizes Generative AI and Chaos Engineering to simulate, detect, diagnose, and resolve network failures in real-time.

It features a Retrieval-Augmented Generation (RAG) engine to learn from historical data and a Human-in-the-Loop approval system for high-risk interventions.

## Key Features

* **Chaos Engineering Simulator:** Inject real-world faults like DDoS Attacks, BGP Route Leaks, Firmware Corruption, Broadcast Storms, and Fiber Cuts.
* **RAG-Powered Reasoning:** Uses ChromaDB to recall historical incident data, ensuring the AI makes decisions based on proven past solutions rather than hallucination.
* **Autonomous Remediation:** An AI Agent (powered by Qwen 2.5 via Ollama) analyzes telemetry (latency, packet loss, throughput) to select the correct tool.
* **Risk Guardrails:** Actions with a Risk Score greater than 50% are automatically paused and sent to an Admin Dashboard for manual approval.
* **Reinforcement Learning:** If an Admin rejects a solution, the system records a negative bias, immediately retries, and proposes an alternative solution.

## System Architecture

1. **Simulation Engine:** Generates synthetic live telemetry data (Latency, Packet Loss, Throughput, Device Health).
2. **Observer:** Monitors the telemetry stream for anomalies.
3. **Vector Database:** Queries ChromaDB for similar historical incidents to determine the best tool and risk level.
4. **Reasoner (LLM):** The AI Agent analyzes the live data and historical context to propose a fix.
5. **Executor:**
    * Low Risk: Executes the fix immediately.
    * High Risk: Queues the action for Admin Approval.

## Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML5, JavaScript (Real-time polling)
* **AI / LLM:** Ollama (running Qwen 2.5:7b or Llama 3)
* **Database:** ChromaDB (Vector Store), JSON (Configuration/Memory)
* **Orchestration:** LangChain

## Installation & Setup

### Prerequisites
1. Python 3.10+ installed.
2. Ollama installed and running.
3. Pull the required model:
   ```bash
   ollama pull qwen2.5:7b
4. Install requirements:
   ```bash
   pip install -r requirements.txt
