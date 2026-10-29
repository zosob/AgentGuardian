from agentguardian.ui import render_app


if __name__ == "__main__":
    render_app()
    for name, description in scenarios.items():
        with st.expander(name):
            st.write(description)