def calculate_risk_score(profile):
    """
    Analyze an AI agent profile and return a structured security risk assessment.

    The scoring is intentionally rule-based and explainable.
    This makes the project useful even without an LLM.
    """

    score = 0
    risks = []
    recommendations = []

    category_scores = {
    "Prompt Injection": 0,
    "Tool Misuse": 0,
    "Sensitive Data Exposure": 0,
    "Autonomy": 0,
    "Human Oversight": 0,
    "Privilege and Access": 0,
    "Output Handling": 0,
    "Logging": 0
    }
    
    tools = profile.get("tools", [])
    data_types = profile.get("data_types", [])
    external_inputs = profile.get("external_inputs", [])
    autonomy_level = profile.get("autonomy_level", "")
    human_approval = profile.get("human_approval", "")

    # -----------------------------
    # Prompt Injection Risk
    # -----------------------------
    prompt_injection_inputs = [
        "User messages",
        "Emails",
        "Websites",
        "Uploaded files",
        "API responses",
        "Chat logs",
        "Support tickets"
    ]

    if any(item in external_inputs for item in prompt_injection_inputs):
        category_scores["Prompt Injection"] += 15
        risks.append({
            "category": "Prompt Injection",
            "severity": "High",
            "reason": "The agent receives external or user-controlled input that may contain malicious instructions."
        })
        recommendations.append(
            "Treat all external input as untrusted. Add input validation, instruction separation, and prompt-injection testing."
        )

    # -----------------------------
    # Tool Misuse Risk
    # -----------------------------
    high_impact_tools = [
        "Email",
        "Code execution",
        "Payment system",
        "Database",
        "CRM",
        "Files"
    ]

    selected_high_impact_tools = [tool for tool in tools if tool in high_impact_tools]

    if selected_high_impact_tools:
        tool_score = 10 + (len(selected_high_impact_tools) * 3)
        score += tool_score
        category_scores["Tool Misuse"] += tool_score
        risks.append({
            "category": "Tool Misuse",
            "severity": "High",
            "reason": f"The agent has access to high-impact tools: {', '.join(selected_high_impact_tools)}."
        })
        recommendations.append(
            "Restrict tool permissions using least privilege and require approval for high-impact actions."
        )

    # -----------------------------
    # Sensitive Data Exposure Risk
    # -----------------------------
    sensitive_data = [
        "Personally identifiable information",
        "Financial data",
        "Health data",
        "Credentials or secrets",
        "Customer records",
        "Student records"
    ]

    selected_sensitive_data = [data for data in data_types if data in sensitive_data]

    if selected_sensitive_data:
        data_score = 10 + (len(selected_sensitive_data) * 4)
        score += data_score
        category_scores["Sensitive Data Exposure"] += data_score    
        risks.append({
            "category": "Sensitive Data Exposure",
            "severity": "High",
            "reason": f"The agent handles sensitive data: {', '.join(selected_sensitive_data)}."
        })
        recommendations.append(
            "Minimize sensitive data access, redact unnecessary fields, and avoid storing secrets in prompts or logs."
        )

    # -----------------------------
    # Excessive Autonomy Risk
    # -----------------------------
    if autonomy_level == "Executes automatically":
        category_scores["Autonomy"] += 25
        risks.append({
            "category": "Excessive Autonomy",
            "severity": "Critical",
            "reason": "The agent can execute actions automatically without human review."
        })
        recommendations.append(
            "Add human-in-the-loop approval for actions involving external communication, financial impact, or sensitive data."
        )

    elif autonomy_level == "Executes after approval":
        category_scores["Autonomy"] += 10
        risks.append({
            "category": "Controlled Autonomy",
            "severity": "Medium",
            "reason": "The agent can execute actions, but approval is required."
        })
        recommendations.append(
            "Clearly define approval thresholds and log all approved actions."
        )

    elif autonomy_level == "Drafts actions":
        category_scores["Autonomy"] += 5
        risks.append({
            "category": "Drafted Action Risk",
            "severity": "Low",
            "reason": "The agent drafts actions that a human may later execute."
        })
        recommendations.append(
            "Require users to review drafted outputs before sending or applying them."
        )

    # -----------------------------
    # Human Approval Gap
    # -----------------------------
    if human_approval == "Not required":
        category_scores["Human Oversight"] += 20
        risks.append({
            "category": "Human Oversight Gap",
            "severity": "High",
            "reason": "The workflow does not require human approval."
        })
        recommendations.append(
            "Require human approval for sensitive, irreversible, or externally visible actions."
        )

    elif human_approval == "Required for high-risk actions":
        category_scores["Human Oversight"] += 20
        risks.append({
            "category": "Partial Human Oversight",
            "severity": "Medium",
            "reason": "Human approval exists, but only for selected high-risk actions."
        })
        recommendations.append(
            "Define what counts as a high-risk action and document escalation rules."
        )

    # -----------------------------
    # Privilege and Access Risk
    # -----------------------------
    if len(tools) >= 5:
        category_scores["Privilege and Access"] += 12
        risks.append({
            "category": "Excessive Tool Access",
            "severity": "High",
            "reason": "The agent has access to many tools, increasing the blast radius of misuse."
        })
        recommendations.append(
            "Reduce tool access to only what the agent needs for its core task."
        )

    # -----------------------------
    # Insecure Output Handling
    # -----------------------------
    output_sensitive_tools = [
        "Email",
        "Slack/Teams",
        "Ticketing system",
        "CRM"
    ]

    if any(tool in tools for tool in output_sensitive_tools):
        category_scores["Output Handling"] += 8
        risks.append({
            "category": "Insecure Output Handling",
            "severity": "Medium",
            "reason": "The agent may generate messages or records that affect external users or business workflows."
        })
        recommendations.append(
            "Validate outputs before sending, especially messages, links, decisions, or customer-facing responses."
        )

    # -----------------------------
    # Logging and Accountability
    # -----------------------------
    if autonomy_level in ["Executes automatically", "Executes after approval"]:
        category_scores["Logging"] += 7
        risks.append({
            "category": "Logging and Accountability",
            "severity": "Medium",
            "reason": "Agents that execute actions need strong audit logs for accountability."
        })
        recommendations.append(
            "Log prompts, tool calls, approvals, outputs, and final actions for review and incident response."
        )

    # Cap score at 100
    score = min(score, 100)

    # Determine risk level
    if score >= 80:
        risk_level = "Critical"
    elif score >= 60:
        risk_level = "High"
    elif score >= 30:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Remove duplicate recommendations while preserving order
    unique_recommendations = []
    for rec in recommendations:
        if rec not in unique_recommendations:
            unique_recommendations.append(rec)

    return {
        "score": score,
        "risk_level": risk_level,
        "risks": risks,
        "recommendations": unique_recommendations,
        "category_scores": category_scores
    }