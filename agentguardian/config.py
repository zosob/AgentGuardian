from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


DEFAULT_CONFIG: Dict[str, Any] = {
    "categories": [
        "Prompt Injection",
        "Tool Misuse",
        "Sensitive Data Exposure",
        "Autonomy",
        "Human Oversight",
        "Privilege and Access",
        "Output Handling",
        "Logging",
    ],
    "weights": {
        "prompt_injection": 15,
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
    "thresholds": {
        "Low": 30,
        "Medium": 60,
        "High": 80,
    },
    "tool_names": {
        "high_impact": [
            "Email",
            "Code execution",
            "Payment system",
            "Database",
            "CRM",
            "Files",
        ],
        "output_sensitive": [
            "Email",
            "Slack/Teams",
            "Ticketing system",
            "CRM",
        ],
    },
    "sensitive_data": [
        "Personally identifiable information",
        "Financial data",
        "Health data",
        "Credentials or secrets",
        "Customer records",
        "Student records",
    ],
    "prompt_injection_inputs": [
        "User messages",
        "Emails",
        "Websites",
        "Uploaded files",
        "API responses",
        "Chat logs",
        "Support tickets",
    ],
}


def _coerce_mapping(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _load_from_file(file_path: Path) -> Dict[str, Any]:
    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        return json.loads(text)
    if file_path.suffix.lower() in {".yaml", ".yml"} and yaml is not None:
        return yaml.safe_load(text) or {}
    raise ValueError(f"Unsupported config format for {file_path}")


def _merge_config(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = json.loads(json.dumps(base))
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


def find_risk_config(paths: Iterable[Path] | None = None) -> Path | None:
    candidate_paths = list(paths or [])
    if not candidate_paths:
        candidate_paths = [
            Path("risk_config.json"),
            Path("risk_config.yaml"),
            Path("risk_config.yml"),
            Path("config/risk_config.json"),
            Path("config/risk_config.yaml"),
            Path("config/risk_config.yml"),
            Path(__file__).resolve().parent.parent / "risk_config.json",
            Path(__file__).resolve().parent.parent / "risk_config.yaml",
            Path(__file__).resolve().parent.parent / "risk_config.yml",
        ]
    for path in candidate_paths:
        if path.exists():
            return path
    return None


def load_risk_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    resolved_path = Path(config_path) if config_path else find_risk_config()
    config = DEFAULT_CONFIG.copy()
    if resolved_path is not None:
        file_config = _load_from_file(Path(resolved_path))
        config = _merge_config(config, _coerce_mapping(file_config))
    return config
