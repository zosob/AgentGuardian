from __future__ import annotations

from typing import Dict, Any


SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Customer Support Agent": {
        "agent_name": "Customer Support Agent",
        "agent_purpose": "Reads support tickets, checks order history, drafts refund responses, and sends emails.",
        "tools": ["Email", "Files", "Database", "CRM"],
        "data_types": ["Customer records", "Personally identifiable information"],
        "external_inputs": ["Support tickets", "Emails", "User messages"],
        "autonomy_level": "Drafts actions",
        "human_approval": "Required for high-risk actions",
    },
    "HR Screening Agent": {
        "agent_name": "HR Screening Agent",
        "agent_purpose": "Reviews resumes, ranks candidates, and drafts interview recommendations.",
        "tools": ["Files", "CRM"],
        "data_types": ["Student records", "Personally identifiable information"],
        "external_inputs": ["Uploaded files", "User messages"],
        "autonomy_level": "Drafts actions",
        "human_approval": "Required for high-risk actions",
    },
    "Invoice Approval Agent": {
        "agent_name": "Invoice Approval Agent",
        "agent_purpose": "Reads invoices, checks vendor records, and approves payments under a threshold.",
        "tools": ["Email", "Files", "Database", "Payment system", "CRM"],
        "data_types": ["Financial data", "Customer records", "Credentials or secrets"],
        "external_inputs": ["Emails", "Uploaded files", "API responses"],
        "autonomy_level": "Executes automatically",
        "human_approval": "Not required",
    },
    "University Advising Agent": {
        "agent_name": "University Advising Agent",
        "agent_purpose": "Answers student questions using academic records and course catalog data.",
        "tools": ["Files", "Database"],
        "data_types": ["Student records", "Internal documents"],
        "external_inputs": ["User messages", "Support tickets"],
        "autonomy_level": "Executes after approval",
        "human_approval": "Required for high-risk actions",
    },
    "Senior Scam Awareness Agent": {
        "agent_name": "Senior Scam Awareness Agent",
        "agent_purpose": "Reviews suspicious messages and explains possible scam indicators.",
        "tools": ["Email", "Web browser"],
        "data_types": ["Public data"],
        "external_inputs": ["Emails", "Websites"],
        "autonomy_level": "Suggests only",
        "human_approval": "Always required",
    },
}


def get_scenario(name: str | None) -> Dict[str, Any] | None:
    if not name or name == "Custom":
        return None
    return SCENARIOS.get(name)
