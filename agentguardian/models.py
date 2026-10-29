from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentProfile:
    """Structured representation of an agent workflow profile."""

    agent_name: str = ""
    agent_purpose: str = ""
    tools: List[str] = field(default_factory=list)
    data_types: List[str] = field(default_factory=list)
    external_inputs: List[str] = field(default_factory=list)
    autonomy_level: str = "Suggests only"
    human_approval: str = "Always required"
    use_ollama: bool = True
    ollama_model: str = "llama3.2"

    @classmethod
    def from_dict(cls, data: Dict[str, Any] | None) -> "AgentProfile":
        if data is None:
            data = {}
        return cls(
            agent_name=str(data.get("agent_name", "")),
            agent_purpose=str(data.get("agent_purpose", "")),
            tools=list(data.get("tools", []) or []),
            data_types=list(data.get("data_types", []) or []),
            external_inputs=list(data.get("external_inputs", []) or []),
            autonomy_level=str(data.get("autonomy_level", "Suggests only")),
            human_approval=str(data.get("human_approval", "Always required")),
            use_ollama=bool(data.get("use_ollama", True)),
            ollama_model=str(data.get("ollama_model", "llama3.2")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "agent_purpose": self.agent_purpose,
            "tools": self.tools,
            "data_types": self.data_types,
            "external_inputs": self.external_inputs,
            "autonomy_level": self.autonomy_level,
            "human_approval": self.human_approval,
            "use_ollama": self.use_ollama,
            "ollama_model": self.ollama_model,
        }
