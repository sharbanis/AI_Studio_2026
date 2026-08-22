"""
app.py — Main Streamlit Chat Application
Two-screen app: Chat (main) + Settings (pages/settings.py)
"""

import re
import streamlit as st
from pathlib import Path
from config_store import get_store
from jira_client import get_jira_client
from llm_client import get_llm_client

# Page config
st.set_page_config(
    page_title="Jira Test Case Generator",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def extract_jira_key(text: str) -> str:
    """Extract Jira ticket key from text using regex."""
    match = re.search(r'\b([A-Z]+-\d+)\b', text)
    return match.group(1) if match else None

def load_template() -> str:
    """Load the test case generator template."""
    template_path = Path(__file__).parent / "templates" / "testcase_creator.md"
    if template_path.exists():
        return template_path.read_text()
    return "# Test Case Template\n{content}"

def format_prompt(ticket_data: dict, template: str) -> str:
    """Format the prompt by merging ticket data into template."""
    return template.format(
        ticket_key=ticket_data.get("key", "UNKNOWN"),
        summary=ticket_data.get("summary", "N/A"),
        description=ticket_data.get("description", "N/A"),
        acceptance_criteria=ticket_data.get("acceptance_criteria", "N/A"),
    )

def main():
    """Main chat application."""
    st.title("✅ Jira Test Case Generator")
    st.markdown("Chat-based tool to generate test cases from Jira tickets")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings")
        if st.button("⚙️ Go to Settings"):
            st.switch_page("pages/settings.py")
        
        # Quick status
        store = get_store()
        jira_configured = bool(
            store.get("jira_url") and 
            store.get("jira_email") and 
            store.get("jira_api_token")
        )
        
        if jira_configured:
            st.success("✓ Jira Configured")
        else:
            st.warning("⚠ Jira Not Configured")
        
        # LLM provider status
        llm_client = get_llm_client()
        ollama_available = llm_client.test_ollama()
        groq_available = llm_client.test_groq()
        
        st.markdown("**LLM Providers:**")
        if ollama_available:
            st.success("✓ Ollama Available")
        else:
            st.error("✗ Ollama Unavailable")
        
        if groq_available:
            st.success("✓ Groq Available")
        else:
            st.error("✗ Groq Unavailable")
        
        if not (ollama_available or groq_available):
            st.error("⚠ No LLM provider available. Configure Ollama or Groq to generate test cases.")
    
    # Main chat area
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Type your request (e.g., 'create test cases for JIRA-102')")
    
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process request
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                # Extract Jira key
                jira_key = extract_jira_key(user_input)
                
                if not jira_key:
                    response = "❌ No Jira key found. Please mention a ticket like JIRA-102 or QA-50."
                else:
                    # Fetch ticket from Jira
                    jira_client = get_jira_client()
                    ticket_data = jira_client.fetch_ticket(jira_key)
                    
                    if not ticket_data:
                        response = f"❌ Could not fetch ticket **{jira_key}**. Check if it exists and your Jira credentials are correct."
                    else:
                        # Load template and format prompt
                        template = load_template()
                        prompt = format_prompt(ticket_data, template)
                        
                        # Generate test cases
                        llm_client = get_llm_client()
                        test_cases = llm_client.generate(prompt)
                        
                        if not test_cases:
                            # Provide detailed error message
                            provider = store.get("llm_provider", "ollama").lower()
                            ollama_ok = llm_client.test_ollama()
                            groq_ok = llm_client.test_groq()
                            
                            error_details = []
                            error_details.append(f"❌ Failed to generate test cases.\n")
                            error_details.append(f"**Selected Provider:** {provider}\n")
                            error_details.append(f"**Ollama Status:** {'✓ Available' if ollama_ok else '✗ Unavailable'}\n")
                            error_details.append(f"**Groq Status:** {'✓ Available' if groq_ok else '✗ Unavailable (check API key)'}\n")
                            error_details.append(f"\n**Troubleshooting:**\n")
                            
                            if not ollama_ok:
                                error_details.append(f"- Ollama is not running or not at http://localhost:11434\n")
                                error_details.append(f"- Start Ollama or update URL in Settings\n")
                                error_details.append(f"- Ensure model gemma3:1b is pulled\n")
                            
                            if not groq_ok:
                                error_details.append(f"- Groq API key is missing or invalid\n")
                                error_details.append(f"- Add your Groq API key in Settings\n")
                            
                            error_details.append(f"\nThe app needs at least one provider (Ollama or Groq) to be available.\n")
                            
                            response = "".join(error_details)
                        else:
                            response = f"## Test Cases for {jira_key}\n\n{test_cases}"
            
            st.markdown(response)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

if __name__ == "__main__":
    main()
