from __future__ import annotations

import pandas as pd
import streamlit as st

from .reporting import generate_markdown_report
from .sample_scenarios import SCENARIOS
from .scoring import calculate_risk_score


def _apply_scenario_to_session(selected_name: str | None) -> None:
    if selected_name is None or selected_name == "Custom":
        return
    profile = SCENARIOS[selected_name]
    st.session_state["agent_name"] = profile.get("agent_name", "")
    st.session_state["agent_purpose"] = profile.get("agent_purpose", "")
    st.session_state["tools"] = profile.get("tools", [])
    st.session_state["data_types"] = profile.get("data_types", [])
    st.session_state["external_inputs"] = profile.get("external_inputs", [])
    st.session_state["autonomy_level"] = profile.get("autonomy_level", "Suggests only")
    st.session_state["human_approval"] = profile.get("human_approval", "Always required")


def render_app() -> None:
    st.set_page_config(page_title="AgentGuardian", page_icon="🛡️", layout="wide")
    st.title("AgentGuardian")
    st.subheader("Local-first AI Agent Security Risk Scanner")
    st.write(
        """
        AgentGuardian helps developers and security teams evaluate risks in agentic AI workflows.
        Describe an AI agent, select its tools and data access, and generate a practical security risk review.
        """
    )
    st.info(
        "This app uses a rule-based risk engine and can optionally generate explanations with a local Ollama model. No external LLM API key is required."
    )
    st.divider()

    st.sidebar.title("About")
    st.sidebar.info(
        """
        **AgentGuardian** is designed for quick AI agent security reviews.

        It focuses on risks such as:
        - Prompt injection
        - Tool misuse
        - Sensitive data exposure
        - Excessive autonomy
        - Lack of human oversight
        """
    )

    st.sidebar.title("Local LLM")
    use_ollama = st.sidebar.checkbox("Use Ollama summary", value=True)
    ollama_model = st.sidebar.text_input("Ollama model", value="llama3.2")

    tab1, tab2, tab3 = st.tabs(["🔍 Agent Workflow Scanner", "📚 Risk Knowledge Base", "🧪 Sample Scenarios"])

    with tab1:
        st.header("Agent Workflow Scanner")
        st.write("Describe the AI agent you want to evaluate.")

        col1, col2 = st.columns(2)
        with col1:
            agent_name = st.text_input(
                "Agent name",
                value=st.session_state.get("agent_name", ""),
                placeholder="Example: Customer Support Refund Agent",
            )
            agent_purpose = st.text_area(
                "Agent purpose",
                value=st.session_state.get("agent_purpose", ""),
                placeholder="Describe what this AI agent is supposed to do...",
                height=140,
            )
            autonomy_level = st.selectbox(
                "Autonomy level",
                ["Suggests only", "Drafts actions", "Executes after approval", "Executes automatically"],
                index=["Suggests only", "Drafts actions", "Executes after approval", "Executes automatically"].index(
                    st.session_state.get("autonomy_level", "Suggests only")
                )
                if st.session_state.get("autonomy_level", "Suggests only") in ["Suggests only", "Drafts actions", "Executes after approval", "Executes automatically"]
                else 0,
            )
            human_approval = st.selectbox(
                "Human approval",
                ["Always required", "Required for high-risk actions", "Not required"],
                index=["Always required", "Required for high-risk actions", "Not required"].index(
                    st.session_state.get("human_approval", "Always required")
                )
                if st.session_state.get("human_approval", "Always required") in ["Always required", "Required for high-risk actions", "Not required"]
                else 0,
            )

        with col2:
            tools = st.multiselect(
                "Tools the agent can access",
                [
                    "Email",
                    "Calendar",
                    "Files",
                    "Web browser",
                    "Database",
                    "Code execution",
                    "Payment system",
                    "CRM",
                    "Slack/Teams",
                    "Ticketing system",
                ],
                default=st.session_state.get("tools", []),
            )
            data_types = st.multiselect(
                "Types of data the agent handles",
                [
                    "Public data",
                    "Internal documents",
                    "Personally identifiable information",
                    "Financial data",
                    "Health data",
                    "Credentials or secrets",
                    "Customer records",
                    "Student records",
                ],
                default=st.session_state.get("data_types", []),
            )
            external_inputs = st.multiselect(
                "External inputs the agent receives",
                [
                    "User messages",
                    "Emails",
                    "Websites",
                    "Uploaded files",
                    "API responses",
                    "Chat logs",
                    "Support tickets",
                ],
                default=st.session_state.get("external_inputs", []),
            )

        st.divider()
        analyze_button = st.button("Analyze Agent Risk", type="primary")

        if analyze_button:
            missing_required_input = (
                not agent_name.strip()
                and not agent_purpose.strip()
                and not tools
                and not data_types
                and not external_inputs
            )

            if missing_required_input:
                st.error(
                    "Please enter at least some information about the AI agent before generating a risk report."
                )
                st.stop()

            if not agent_purpose.strip():
                st.warning(
                    "Agent purpose is empty. The analysis may be less useful without a clear description of what the agent does."
                )

            profile = {
                "agent_name": agent_name,
                "agent_purpose": agent_purpose,
                "tools": tools,
                "data_types": data_types,
                "external_inputs": external_inputs,
                "autonomy_level": autonomy_level,
                "human_approval": human_approval,
                "use_ollama": use_ollama,
                "ollama_model": ollama_model,
            }
            result = calculate_risk_score(profile)

            st.success("Risk analysis complete.")
            st.subheader("Risk Summary")

            if result["risk_level"] == "Critical":
                st.error("Critical risk detected. This agent should not be deployed without strong safeguards.")
            elif result["risk_level"] == "High":
                st.warning("High risk detected. Review permissions, autonomy, and sensitive data access before deployment.")
            elif result["risk_level"] == "Medium":
                st.info("Medium risk detected. Add safeguards before production use.")
            else:
                st.success("Low risk detected. Continue monitoring and validating the workflow.")

            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Risk Score", f"{result['score']}/100")
            with metric_col2:
                st.metric("Risk Level", result["risk_level"])

            st.subheader("Risk Category Breakdown")
            category_df = pd.DataFrame(list(result["category_scores"].items()), columns=["Risk Category", "Score"])
            category_df = category_df[category_df["Score"] > 0]
            if not category_df.empty:
                st.bar_chart(category_df, x="Risk Category", y="Score", use_container_width=True)
            else:
                st.info("No category-specific risk points were added.")

            st.divider()
            st.subheader("Detected Risks")
            if result["risks"]:
                st.dataframe(pd.DataFrame(result["risks"]), use_container_width=True)
            else:
                st.info("No major risks detected based on the current inputs.")

            st.subheader("Recommended Controls")
            for index, recommendation in enumerate(result["recommendations"], start=1):
                st.write(f"{index}. {recommendation}")

            st.divider()
            st.subheader("Local LLM Security Analysis")
            if use_ollama:
                from ollama_utils import generate_ollama_summary

                with st.spinner(f"Generating local security analysis with {ollama_model}..."):
                    ollama_summary = generate_ollama_summary(profile=profile, risk_result=result, model_name=ollama_model)
                st.markdown(ollama_summary)
            else:
                st.info("Ollama summary is turned off. Enable it in the sidebar to generate a local LLM analysis.")

            st.divider()
            st.subheader("Download Security Report")
            markdown_report = generate_markdown_report(profile=profile, result=result, ollama_summary=ollama_summary if use_ollama else None)
            safe_agent_name = agent_name.strip().lower().replace(" ", "-") if agent_name.strip() else "agentguardian-report"
            st.download_button(
                label="Download Markdown Report",
                data=markdown_report,
                file_name=f"{safe_agent_name}-security-report.md",
                mime="text/markdown",
            )
            with st.expander("View Captured Agent Profile"):
                st.json(profile)

    with tab2:
        st.header("Risk Knowledge Base")
        st.write(
            """
            Agentic AI systems introduce new security concerns because they can reason,
            use tools, access sensitive data, and take actions on behalf of users.
            """
        )
        risk_data = [
            {"Risk Category": "Prompt Injection", "Description": "Malicious input attempts to override system instructions or manipulate the agent."},
            {"Risk Category": "Tool Misuse", "Description": "The agent uses tools in unsafe, unintended, or unauthorized ways."},
            {"Risk Category": "Sensitive Data Exposure", "Description": "The agent reveals, stores, or processes private data insecurely."},
            {"Risk Category": "Excessive Autonomy", "Description": "The agent can take high-impact actions without enough human oversight."},
            {"Risk Category": "Privilege Abuse", "Description": "The agent has broader access than needed for its assigned task."},
            {"Risk Category": "Insecure Output Handling", "Description": "The agent generates unsafe outputs such as commands, links, or messages without validation."},
            {"Risk Category": "Logging Gap", "Description": "Agent actions are not logged clearly enough for auditing or incident response."},
        ]
        st.dataframe(pd.DataFrame(risk_data), use_container_width=True)

    with tab3:
        st.header("Sample Scenarios")
        st.write("Use these examples to test AgentGuardian with realistic agentic AI workflows.")
        scenario_names = ["Custom"] + list(SCENARIOS.keys())
        selected_scenario = st.selectbox("Load a sample scenario", scenario_names, index=0)
        if selected_scenario != "Custom":
            st.button("Apply scenario", on_click=_apply_scenario_to_session, args=(selected_scenario,))

        scenario_cards = [
            {
                "Scenario": name,
                "Summary": scenario["agent_purpose"],
            }
            for name, scenario in SCENARIOS.items()
        ]
        st.dataframe(pd.DataFrame(scenario_cards), use_container_width=True)
