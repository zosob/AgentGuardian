from agentguardian.scoring import calculate_risk_score


def test_low_risk_profile():
    profile = {
        "agent_name": "Simple Assistant",
        "agent_purpose": "Answers user questions using a public knowledge base.",
        "tools": ["Calendar"],
        "data_types": ["Public data"],
        "external_inputs": ["User messages"],
        "autonomy_level": "Suggests only",
        "human_approval": "Always required",
    }
    result = calculate_risk_score(profile)
    assert result["score"] < 30
    assert result["risk_level"] == "Low"


def test_high_risk_invoice_approval_profile():
    profile = {
        "agent_name": "Invoice Approval Agent",
        "agent_purpose": "Reads invoices and automatically approves payments under a threshold.",
        "tools": ["Email", "Files", "Database", "Payment system", "CRM"],
        "data_types": ["Financial data", "Customer records", "Credentials or secrets"],
        "external_inputs": ["Emails", "Uploaded files", "API responses"],
        "autonomy_level": "Executes automatically",
        "human_approval": "Not required",
    }
    result = calculate_risk_score(profile)
    assert result["score"] >= 80
    assert result["risk_level"] == "Critical"
    assert any(r["category"] == "Prompt Injection" for r in result["risks"])
    assert any(r["category"] == "Excessive Autonomy" for r in result["risks"])


def test_configurable_weights_can_shift_score():
    base = calculate_risk_score({
        "agent_name": "Weighted Test",
        "agent_purpose": "Test profile",
        "tools": ["Email"],
        "data_types": ["Financial data"],
        "external_inputs": ["Emails"],
        "autonomy_level": "Suggests only",
        "human_approval": "Always required",
    })

    custom_config = {
        "categories": ["Prompt Injection", "Tool Misuse", "Sensitive Data Exposure", "Autonomy", "Human Oversight", "Privilege and Access", "Output Handling", "Logging"],
        "weights": {
            "prompt_injection": 50,
            "tool_misuse_base": 10,
            "tool_misuse_per_tool": 3,
            "sensitive_data_base": 10,
            "sensitive_data_per_item": 4,
            "autonomy_executes_automatically": 25,
            "autonomy_executes_after_approval": 10,
            "autonomy_drafts_actions": 5,
            "human_oversight_not_required": 20,
            "human_oversight_partial": 20,
            "privilege_and_access_threshold": 5,
            "privilege_and_access_score": 12,
            "output_handling_score": 8,
            "logging_score": 7,
        },
        "thresholds": {"Low": 30, "Medium": 60, "High": 80},
        "tool_names": {"high_impact": ["Email"], "output_sensitive": ["Email"]},
        "sensitive_data": ["Financial data"],
        "prompt_injection_inputs": ["Emails"],
    }

    adjusted = calculate_risk_score({
        "agent_name": "Weighted Test",
        "agent_purpose": "Test profile",
        "tools": ["Email"],
        "data_types": ["Financial data"],
        "external_inputs": ["Emails"],
        "autonomy_level": "Suggests only",
        "human_approval": "Always required",
    }, config=custom_config)

    assert adjusted["score"] > base["score"]
