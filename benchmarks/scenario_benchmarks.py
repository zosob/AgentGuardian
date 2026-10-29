from __future__ import annotations

from agentguardian.scoring import calculate_risk_score


BENCHMARK_SCENARIOS = {
    "low_risk_public_assistant": {
        "profile": {
            "agent_name": "Public Assistant",
            "agent_purpose": "Answers general user questions using public content only.",
            "tools": ["Web browser"],
            "data_types": ["Public data"],
            "external_inputs": ["User messages"],
            "autonomy_level": "Suggests only",
            "human_approval": "Always required",
        },
        "expected_score": 0,
        "expected_risk_level": "Low",
    },
    "medium_risk_email_agent": {
        "profile": {
            "agent_name": "Email Drafting Agent",
            "agent_purpose": "Drafts responses to incoming customer messages.",
            "tools": ["Email", "Files"],
            "data_types": ["Customer records"],
            "external_inputs": ["Emails"],
            "autonomy_level": "Drafts actions",
            "human_approval": "Required for high-risk actions",
        },
        "expected_score": 27,
        "expected_risk_level": "Medium",
    },
    "critical_invoice_agent": {
        "profile": {
            "agent_name": "Invoice Approval Agent",
            "agent_purpose": "Approves invoices and sends payment requests automatically.",
            "tools": ["Email", "Files", "Database", "Payment system", "CRM"],
            "data_types": ["Financial data", "Customer records", "Credentials or secrets"],
            "external_inputs": ["Emails", "Uploaded files", "API responses"],
            "autonomy_level": "Executes automatically",
            "human_approval": "Not required",
        },
        "expected_score": 100,
        "expected_risk_level": "Critical",
    },
}


def run_benchmarks() -> dict:
    results = {}
    for name, benchmark in BENCHMARK_SCENARIOS.items():
        result = calculate_risk_score(benchmark["profile"])
        results[name] = {
            "score": result["score"],
            "risk_level": result["risk_level"],
            "matches_expected": (
                result["score"] == benchmark["expected_score"]
                and result["risk_level"] == benchmark["expected_risk_level"]
            ),
        }
    return results


if __name__ == "__main__":
    print(run_benchmarks())
