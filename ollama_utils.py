import ollama


def generate_ollama_summary(profile, risk_result, model_name="llama3.2"):
    """
    Generate a local LLM-powered security summary using Ollama.

    The deterministic risk engine creates the score and findings.
    Ollama only explains the findings in a readable analyst-style format.
    """

    risks_text = "\n".join(
        [
            f"- {risk['category']} ({risk['severity']}): {risk['reason']}"
            for risk in risk_result.get("risks", [])
        ]
    )

    recommendations_text = "\n".join(
        [
            f"- {recommendation}"
            for recommendation in risk_result.get("recommendations", [])
        ]
    )

    prompt = f"""
You are a cybersecurity analyst reviewing an agentic AI workflow for deployment risk.

Write a concise but practical security review for an engineering and security team.
Use clear, professional language.
Focus on deployment risk, business impact, and concrete mitigations.
Base the review ONLY on the provided information.
Do not invent tools, data types, or risks that are not supported by the input.

Agent Profile:
Agent Name: {profile.get("agent_name", "Unnamed Agent")}
Purpose: {profile.get("agent_purpose", "Not provided")}
Tools: {", ".join(profile.get("tools", [])) if profile.get("tools") else "None selected"}
Data Types: {", ".join(profile.get("data_types", [])) if profile.get("data_types") else "None selected"}
External Inputs: {", ".join(profile.get("external_inputs", [])) if profile.get("external_inputs") else "None selected"}
Autonomy Level: {profile.get("autonomy_level", "Not provided")}
Human Approval: {profile.get("human_approval", "Not provided")}

Rule-Based Risk Assessment:
Risk Score: {risk_result.get("score")}/100
Risk Level: {risk_result.get("risk_level")}

Detected Risks:
{risks_text if risks_text else "No major risks detected."}

Recommended Controls:
{recommendations_text if recommendations_text else "No recommendations generated."}

Return your answer in this exact structure:

## Executive Summary
A short paragraph explaining the overall risk.

## Most Likely Attack Scenario
Describe one realistic attack or misuse scenario.

## Priority Fixes
List 3 to 5 practical controls the team should implement first.

## Deployment Recommendation
State whether this agent is ready for production, needs safeguards, or should not be deployed yet.
"""

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:
        return (
            "Ollama summary could not be generated.\n\n"
            "Possible fixes:\n"
            "1. Make sure Ollama is installed.\n"
            "2. Make sure the Ollama app/server is running.\n"
            f"3. Make sure the model '{model_name}' is pulled locally.\n\n"
            f"Error details: {error}"
        )