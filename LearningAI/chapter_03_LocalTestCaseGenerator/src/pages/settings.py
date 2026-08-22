"""
pages/settings.py — Settings screen for configuration persistence
Accessible from the main chat app via the sidebar
"""

import streamlit as st
from config_store import get_store
from jira_client import get_jira_client
from llm_client import get_llm_client

st.set_page_config(
    page_title="Settings - Test Case Generator",
    page_icon="⚙️",
    layout="wide",
)

st.title("⚙️ Settings")
st.markdown("Configure Jira credentials, LLM provider, and API keys")

# Initialize store and clients
store = get_store()
jira_client = get_jira_client()
llm_client = get_llm_client()

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["Jira", "Ollama", "Groq"])

# === JIRA TAB ===
with tab1:
    st.header("Jira Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        jira_url = st.text_input(
            "Jira URL",
            value=store.get("jira_url", ""),
            placeholder="https://your-workspace.atlassian.net/",
            help="Your Jira Cloud instance URL"
        )
        jira_email = st.text_input(
            "Jira Email",
            value=store.get("jira_email", ""),
            placeholder="your-email@company.com",
            help="Email address for Jira authentication"
        )
    
    with col2:
        jira_token = st.text_input(
            "Jira API Token",
            value=store.get("jira_api_token", ""),
            type="password",
            placeholder="Paste your API token here",
            help="Generate from https://id.atlassian.com/manage-profile/security/api-tokens"
        )
    
    # Test connection button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔗 Test Connection"):
            store.update({
                "jira_url": jira_url,
                "jira_email": jira_email,
                "jira_api_token": jira_token,
            })
            
            if jira_client.test_connection():
                st.success("✓ Connection successful!")
            else:
                st.error("✗ Connection failed. Check credentials.")
    
    # Save button
    if st.button("💾 Save Jira Settings", key="save_jira"):
        store.update({
            "jira_url": jira_url,
            "jira_email": jira_email,
            "jira_api_token": jira_token,
        })
        st.success("✓ Jira settings saved!")

# === OLLAMA TAB ===
with tab2:
    st.header("Ollama Configuration (Local)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ollama_url = st.text_input(
            "Ollama URL",
            value=store.get("ollama_url", "http://localhost:11434"),
            placeholder="http://localhost:11434",
            help="URL where Ollama server is running"
        )
    
    with col2:
        ollama_model = st.text_input(
            "Model Name",
            value=store.get("ollama_model", "gemma3:1b"),
            placeholder="gemma3:1b",
            help="Ollama model name (must be already pulled)"
        )
    
    # Test button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔗 Test Ollama"):
            store.update({
                "ollama_url": ollama_url,
                "ollama_model": ollama_model,
            })
            
            if llm_client.test_ollama():
                st.success("✓ Ollama is running!")
            else:
                st.error("✗ Ollama is not available. Make sure it's running.")
    
    # Save button
    if st.button("💾 Save Ollama Settings", key="save_ollama"):
        store.update({
            "ollama_url": ollama_url,
            "ollama_model": ollama_model,
        })
        st.success("✓ Ollama settings saved!")
    
    st.info("💡 Ensure Ollama is running locally. No credentials needed for local Ollama.")

# === GROQ TAB ===
with tab3:
    st.header("Groq Configuration (Cloud Fallback)")
    
    groq_api_key = st.text_input(
        "Groq API Key",
        value=store.get("groq_api_key", ""),
        type="password",
        placeholder="Paste your Groq API key here",
        help="Get your key from https://console.groq.com"
    )
    
    # Test button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🔗 Test Groq"):
            store.update({"groq_api_key": groq_api_key})
            
            if llm_client.test_groq():
                st.success("✓ Groq connection successful!")
            else:
                st.error("✗ Groq connection failed. Check API key.")
    
    # Save button
    if st.button("💾 Save Groq Settings", key="save_groq"):
        store.update({"groq_api_key": groq_api_key})
        st.success("✓ Groq settings saved!")
    
    st.info("💡 Groq is used as a fallback when Ollama is unavailable, and vice-versa. The app works as long as at least one provider is available.")

# === LLM PROVIDER SELECTION ===
st.markdown("---")
st.header("Primary LLM Provider")

provider = st.radio(
    "Choose your primary LLM provider:",
    options=["ollama", "groq"],
    index=0 if store.get("llm_provider", "ollama") == "ollama" else 1,
    horizontal=True,
    help="Preferred provider. If it is unavailable, the app automatically falls back to the other one."
)

if st.button("💾 Save Provider Choice"):
    store.update({"llm_provider": provider})
    st.success(f"✓ Primary provider set to **{provider}**")

# === BACK BUTTON ===
st.markdown("---")
if st.button("← Back to Chat"):
    st.switch_page("app.py")
