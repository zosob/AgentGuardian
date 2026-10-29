from __future__ import annotations

from typing import Any, Dict, List

from .config import load_risk_config
from .models import AgentProfile


def _determine_risk_level(score: int, thresholds: Dict[str, int]) -> str:
    if score >= thresholds.get("High", 80):
        return "Critical"
    if score >= thresholds.get("Medium", 60):
        return "High"
    if score >= thresholds.get("Low", 30):
        return "Medium"
    return "Low"


def calculate_risk_score(profile: Dict[str, Any] | AgentProfile, config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Analyze an agent workflow and return a structured score and findings."""
    profile_obj = profile if isinstance(profile, AgentProfile) else AgentProfile.from_dict(profile)
    config_data = load_risk_config() if config is None else config

    score = 0
    risks: List[Dict[str, str]] = []
    recommendations: List[str] = []
    category_scores = {category: 0 for category in config_data.get("categories", [])}

    tools = profile_obj.tools
    data_types = profile_obj.data_types
    external_inputs = profile_obj.external_inputs
    autonomy_level = profile_obj.autonomy_level
    human_approval = profile_obj.human_approval
    weights = config_data.get("weights", {})
    thresholds = config_data.get("thresholds", {})
    high_impact_tools = config_data.get("tool_names", {}).get("high_impact", [])
    sensitive_data = config_data.get("sensitive_data", [])
    prompt_injection_inputs = config_data.get("prompt_injection_inputs", [])
    output_sensitive_tools = config_data.get("tool_names", {}).get("output_sensitive", [])

    if any(item in external_inputs for item in prompt_injection_inputs):
        category_scores["Prompt Injection"] += weights.get("prompt_injection", 15)
        score += weights.get("prompt_injection", 15)
        risks.append({
            "category": "Prompt Injection",
            "severity": "High",
            "reason": "The agent receives external or user-controlled input that may contain malicious instructions.",
        })
        recommendations.append(
            "Treat all external input as untrusted. Add input validation, instruction separation, and prompt-injection testing."
        )

    selected_high_impact_tools = [tool for tool in tools if tool in high_impact_tools]
    if selected_high_impact_tools:
        tool_score = weights.get("tool_misuse_base", 10) + (len(selected_high_impact_tools) * weights.get("tool_misuse_per_tool", 3))
        score += tool_score
        category_scores["Tool Misuse"] += tool_score
        risks.append({
            "category": "Tool Misuse",
            "severity": "High",
            "reason": f"The agent has access to high-impact tools: {', '.join(selected_high_impact_tools)}.",
        })
        recommendations.append(
            "Restrict tool permissions using least privilege and require approval for high-impact actions."
        )

    selected_sensitive_data = [data for data in data_types if data in sensitive_data]
    if selected_sensitive_data:
        data_score = weights.get("sensitive_data_base", 10) + (len(selected_sensitive_data) * weights.get("sensitive_data_per_item", 4))
        score += data_score
        category_scores["Sensitive Data Exposure"] += data_score
        risks.append({
            "category": "Sensitive Data Exposure",
            "severity": "High",
            "reason": f"The agent handles sensitive data: {', '.join(selected_sensitive_data)}.",
        })
        recommendations.append(
            "Minimize sensitive data access, redact unnecessary fields, and avoid storing secrets in prompts or logs."
        )

    if autonomy_level == "Executes automatically":
        category_scores["Autonomy"] += weights.get("autonomy_executes_automatically", 25)
        score += weights.get("autonomy_executes_automatically", 25)
        risks.append({
            "category": "Excessive Autonomy",
            "severity": "Critical",
            "reason": "The agent can execute actions automatically without human review.",
        })
        recommendations.append(
            "Add human-in-the-loop approval for actions involving external communication, financial impact, or sensitive data."
        )
    elif autonomy_level == "Executes after approval":
        category_scores["Autonomy"] += weights.get("autonomy_executes_after_approval", 10)
        score += weights.get("autonomy_executes_after_approval", 10)
        risks.append({
            "category": "Controlled Autonomy",
            "severity": "Medium",
            "reason": "The agent can execute actions, but approval is required.",
        })
        recommendations.append(
            "Clearly define approval thresholds and log all approved actions."
        )
    elif autonomy_level == "Drafts actions":
        category_scores["Autonomy"] += weights.get("autonomy_drafts_actions", 5)
        score += weights.get("autonomy_drafts_actions", 5)
        risks.append({
            "category": "Drafted Action Risk",
            "severity": "Low",
            "reason": "The agent drafts actions that a human may later execute.",
        })
        recommendations.append(
            "Require users to review drafted outputs before sending or applying them."
        )

    if human_approval == "Not required":
        category_scores["Human Oversight"] += weights.get("human_oversight_not_required", 20)
        score += weights.get("human_oversight_not_required", 20)
        risks.append({
            "category": "Human Oversight Gap",
            "severity": "High",
            "reason": "The workflow does not require human approval.",
        })
        recommendations.append(
            "Require human approval for sensitive, irreversible, or externally visible actions."
        )
    elif human_approval == "Required for high-risk actions":
        category_scores["Human Oversight"] += weights.get("human_oversight_partial", 20)
        score += weights.get("human_oversight_partial", 20)
        risks.append({
            "category": "Partial Human Oversight",
            "severity": "Medium",
            "reason": "Human approval exists, but only for selected high-risk actions.",
        })
        recommendations.append(
            "Define what counts as a high-risk action and document escalation rules."
        )

    if len(tools) >= weights.get("privilege_and_access_threshold", 5):
        category_scores["Privilege and Access"] += weights.get("privilege_and_access_score", 12)
        score += weights.get("privilege_and_access_score", 12)
        risks.append({
            "category": "Excessive Tool Access",
            "severity": "High",
            "reason": "The agent has access to many tools, increasing the blast radius of misuse.",
        })
        recommendations.append(
            "Reduce tool access to only what the agent needs for its core task."
        )

    if any(tool in tools for tool in output_sensitive_tools):
        category_scores["Output Handling"] += weights.get("output_handling_score", 8)
        score += weights.get("output_handling_score", 8)
        risks.append({
            "category": "Insecure Output Handling",
            "severity": "Medium",
            "reason": "The agent may generate messages or records that affect external users or business workflows.",
        })
        recommendations.append(
            "Validate outputs before sending, especially messages, links, decisions, or customer-facing responses."
        )

    if autonomy_level in ["Executes automatically", "Executes after approval"]:
        category_scores["Logging"] += weights.get("logging_score", 7)
        score += weights.get("logging_score", 7)
        risks.append({
            "category": "Logging and Accountability",
            "severity": "Medium",
            "reason": "Agents that execute actions need strong audit logs for accountability.",
        })
        recommendations.append(
            "Log prompts, tool calls, approvals, outputs, and final actions for review and incident response."
        )

    score = min(score, 100)
    risk_level = _determine_risk_level(score, thresholds)

    unique_recommendations: List[str] = []
    for rec in recommendations:
        if rec not in unique_recommendations:
            unique_recommendations.append(rec)

    return {
        "score": score,
        "risk_level": risk_level,
        "risks": risks,
        "recommendations": unique_recommendations,
        "category_scores": category_scores,
    }
