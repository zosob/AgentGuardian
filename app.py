import streamlit as st
import pandas as pd
from risk_engine import calculate_risk_score


st.set_page_config(
    page_title="AgentGuardian",
    page_icon="🛡️",
    layout="wide"
)


st.title("AgentGuardian")
st.subheader("Local-first AI Agent Security Risk Scanner")

st.write(
    """
    AgentGuardian helps developers and security teams evaluate risks in agentic AI workflows.
    Describe an AI agent, select its tools and data access, and generate a practical security risk review.
    """
)

st.divider()


# Sidebar
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


# Main tabs
tab1, tab2, tab3 = st.tabs(
    ["🔍 Agent Workflow Scanner", "📚 Risk Knowledge Base", "🧪 Sample Scenarios"]
)


with tab1:
    st.header("Agent Workflow Scanner")

    st.write("Describe the AI agent you want to evaluate.")

    col1, col2 = st.columns(2)

    with col1:
        agent_name = st.text_input(
            "Agent name",
            placeholder="Example: Customer Support Refund Agent"
        )

        agent_purpose = st.text_area(
            "Agent purpose",
            placeholder="Describe what this AI agent is supposed to do...",
            height=140
        )

        autonomy_level = st.selectbox(
            "Autonomy level",
            [
                "Suggests only",
                "Drafts actions",
                "Executes after approval",
                "Executes automatically"
            ]
        )

        human_approval = st.selectbox(
            "Human approval",
            [
                "Always required",
                "Required for high-risk actions",
                "Not required"
            ]
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
                "Ticketing system"
            ]
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
                "Student records"
            ]
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
                "Support tickets"
            ]
        )

    st.divider()

    analyze_button = st.button("Analyze Agent Risk", type="primary")

    if analyze_button:
        profile = {
            "agent_name": agent_name,
            "agent_purpose": agent_purpose,
            "tools": tools,
            "data_types": data_types,
            "external_inputs": external_inputs,
            "autonomy_level": autonomy_level,
            "human_approval": human_approval,
            "use_ollama": use_ollama,
            "ollama_model": ollama_model
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

        st.divider()

        st.subheader("Detected Risks")

        if result["risks"]:
            risk_df = pd.DataFrame(result["risks"])
            st.dataframe(risk_df, use_container_width=True)
        else:
            st.info("No major risks detected based on the current inputs.")

        st.subheader("Recommended Controls")

        for index, recommendation in enumerate(result["recommendations"], start=1):
            st.write(f"{index}. {recommendation}")

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
        {
            "Risk Category": "Prompt Injection",
            "Description": "Malicious input attempts to override system instructions or manipulate the agent."
        },
        {
            "Risk Category": "Tool Misuse",
            "Description": "The agent uses tools in unsafe, unintended, or unauthorized ways."
        },
        {
            "Risk Category": "Sensitive Data Exposure",
            "Description": "The agent reveals, stores, or processes private data insecurely."
        },
        {
            "Risk Category": "Excessive Autonomy",
            "Description": "The agent can take high-impact actions without enough human oversight."
        },
        {
            "Risk Category": "Privilege Abuse",
            "Description": "The agent has broader access than needed for its assigned task."
        },
        {
            "Risk Category": "Insecure Output Handling",
            "Description": "The agent generates unsafe outputs such as commands, links, or messages without validation."
        },
        {
            "Risk Category": "Logging Gap",
            "Description": "Agent actions are not logged clearly enough for auditing or incident response."
        },
    ]

    risk_df = pd.DataFrame(risk_data)
    st.dataframe(risk_df, use_container_width=True)


with tab3:
    st.header("Sample Scenarios")

    st.write("These scenarios will become clickable templates in a later step.")

    scenarios = {
        "Customer Support Agent": "Reads customer support tickets, checks order history, drafts refund responses, and sends emails.",
        "HR Screening Agent": "Reviews resumes, ranks candidates, and drafts interview recommendations.",
        "Invoice Approval Agent": "Reads invoices, checks vendor records, and approves payments under a threshold.",
        "University Advising Agent": "Answers student questions using academic records and course catalog data.",
        "Senior Scam Awareness Agent": "Reviews suspicious messages and explains possible scam indicators."
    }

    for name, description in scenarios.items():
        with st.expander(name):
            st.write(description)