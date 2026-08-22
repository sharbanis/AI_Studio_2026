"""
jira_client.py — Fetch ticket details from Jira Cloud REST API
"""

import requests
from typing import Optional, Dict
from config_store import get_store

class JiraClient:
    def __init__(self):
        """Initialize Jira client with credentials from config."""
        self.store = get_store()
    
    def fetch_ticket(self, ticket_key: str) -> Optional[Dict]:
        """
        Fetch ticket details from Jira.
        
        Returns dict with keys: summary, description, acceptance_criteria
        Returns None if fetch fails.
        """
        jira_url = self.store.get("jira_url", "").strip()
        jira_email = self.store.get("jira_email", "").strip()
        jira_token = self.store.get("jira_api_token", "").strip()
        
        if not all([jira_url, jira_email, jira_token]):
            return None
        
        # Construct REST API URL
        if not jira_url.endswith("/"):
            jira_url += "/"
        api_url = f"{jira_url}rest/api/2/issue/{ticket_key}"
        
        # Prepare auth
        auth = (jira_email, jira_token)
        
        try:
            response = requests.get(api_url, auth=auth, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            
            data = response.json()
            fields = data.get("fields", {})
            
            # Extract relevant fields
            result = {
                "key": data.get("key", ticket_key),
                "summary": fields.get("summary", "No summary"),
                "description": fields.get("description", "No description"),
                "acceptance_criteria": self._extract_acceptance_criteria(fields),
            }
            return result
        except requests.exceptions.RequestException as e:
            print(f"Error fetching ticket {ticket_key}: {e}")
            return None
    
    def _extract_acceptance_criteria(self, fields: Dict) -> str:
        """
        Extract acceptance criteria from various possible Jira fields.
        Jira sometimes stores custom fields with different names.
        """
        # Try common custom field names
        candidates = [
            "customfield_10051",  # Often "Acceptance Criteria"
            "customfield_10052",
            fields.get("Acceptance Criteria"),
            fields.get("acceptance_criteria"),
        ]
        
        for candidate in candidates:
            if candidate and isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
        
        return "No acceptance criteria provided"
    
    def test_connection(self) -> bool:
        """
        Test the connection to Jira by fetching a non-existent issue.
        Returns True if authentication works, False otherwise.
        """
        jira_url = self.store.get("jira_url", "").strip()
        jira_email = self.store.get("jira_email", "").strip()
        jira_token = self.store.get("jira_api_token", "").strip()
        
        if not all([jira_url, jira_email, jira_token]):
            return False
        
        if not jira_url.endswith("/"):
            jira_url += "/"
        api_url = f"{jira_url}rest/api/2/myself"
        
        auth = (jira_email, jira_token)
        
        try:
            response = requests.get(api_url, auth=auth, timeout=10)
            return response.status_code == 200
        except:
            return False

# Global instance
_jira_client = None

def get_jira_client():
    """Get or create the global JiraClient."""
    global _jira_client
    if _jira_client is None:
        _jira_client = JiraClient()
    return _jira_client
