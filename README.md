# AgentGuardian

AgentGuardian is a local-first AI security web app that scans agentic AI workflows for risks such as prompt injection, tool misuse, excessive autonomy, sensitive data exposure, insecure output handling, and lack of human oversight.

The project combines a deterministic rule-based risk scoring engine with optional local LLM-generated security analysis using Ollama. No external LLM API key is required.

---

## Why AgentGuardian?

AI agents are increasingly being connected to tools such as email, databases, files, calendars, CRMs, ticketing systems, and payment workflows. These capabilities create new security risks when agents receive untrusted input, access sensitive data, or take actions without proper human oversight.

AgentGuardian helps developers, security teams, educators, and students quickly evaluate an AI agent workflow before deployment.

---

## Features

- Streamlit-based web interface
- Rule-based AI agent risk scoring
- Risk score from 0 to 100
- Risk level classification: Low, Medium, High, or Critical
- Risk category breakdown chart
- Detected risks table
- Recommended security controls
- Optional local LLM security analysis using Ollama
- Downloadable Markdown security report
- Sample agent scenarios for testing
- Local-first design with no external API key required

---

## Risk Categories

AgentGuardian evaluates agentic AI workflows across several security risk categories:

- Prompt Injection
- Tool Misuse
- Sensitive Data Exposure
- Excessive Autonomy
- Human Oversight Gap
- Privilege and Access Risk
- Insecure Output Handling
- Logging and Accountability Gap

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Ollama

---

## Project Structure

```text
AgentGuardian/
├── app.py
├── risk_engine.py
├── ollama_utils.py
├── sample_scenarios.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/zosob/AgentGuardian.git
cd AgentGuardian

---

### 2. Create and activate a conda environment

```bash
conda create -n agentguardian python=3.11
conda activate agentguardian
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install and run Ollama

Download and install Ollama from:

```text
https://ollama.com
```

Pull a local model:

```bash
ollama pull llama3.2
```

For stronger local analysis, especially if you have a capable NVIDIA GPU, you can use:

```bash
ollama pull llama3.1:8b
```

---

### 5. Run the app

```bash
streamlit run app.py
```

The app should open locally in your browser, usually at:

```text
http://localhost:8501
```

---

## Example Use Case

An organization wants to deploy an AI agent that reads customer support tickets, checks CRM records, drafts refund responses, and sends emails to customers.

AgentGuardian can identify risks such as:

- Prompt injection through support tickets
- Sensitive data exposure from customer records
- Tool misuse through email and CRM access
- Need for human approval before customer-facing actions
- Need for logging and output validation

---

## Example High-Risk Scenario

```text
Agent Name:
Invoice Payment Agent

Purpose:
Reads invoices, verifies vendor records, and automatically approves payments under $5,000.

Tools:
Email, Files, Database, Payment system

Data Types:
Financial data, Customer records, Credentials or secrets

External Inputs:
Emails, Uploaded files, API responses

Autonomy Level:
Executes automatically

Human Approval:
Not required
```

Expected result: High or Critical risk.

---

## How It Works

AgentGuardian uses two layers of analysis:

### 1. Rule-Based Risk Engine

The deterministic risk engine assigns risk points based on the agent’s tools, data access, autonomy level, external inputs, and human approval requirements.

This makes the scoring explainable and consistent.

### 2. Local LLM Security Summary

If enabled, Ollama generates a readable security analysis based on the rule-based findings. The LLM does not determine the score. It explains the result in a practical analyst-style format.

This keeps the tool local-first and avoids dependency on external LLM APIs.


---

## Future Improvements

Possible next steps:

- Add clickable sample scenarios using Streamlit session state
- Add OWASP Agentic AI and OWASP LLM risk mappings
- Export reports as PDF
- Add Docker support
- Add comparison between multiple agent workflows
- Add policy recommendations for enterprise deployment
- Add configurable risk weights
- Add support for additional local models

---

## Disclaimer

AgentGuardian is a lightweight security review aid. It does not replace a formal security assessment, threat model, penetration test, privacy review, or compliance audit.

Use this tool as a starting point for identifying risks in agentic AI workflows before deployment.

---

## Author

Built by Bhaskar Ghosh
