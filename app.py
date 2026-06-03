import streamlit as st
import pandas as pd


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
        st.success("Workflow captured successfully. Risk analysis engine will be added in Hour 2.")

        st.subheader("Captured Agent Profile")

        profile = {
            "Agent Name": agent_name,
            "Purpose": agent_purpose,
            "Tools": ", ".join(tools) if tools else "None selected",
            "Data Types": ", ".join(data_types) if data_types else "None selected",
            "External Inputs": ", ".join(external_inputs) if external_inputs else "None selected",
            "Autonomy Level": autonomy_level,
            "Human Approval": human_approval,
            "Use Ollama": use_ollama,
            "Ollama Model": ollama_model
        }

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