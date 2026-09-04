"""
Jira Client - Minimal Connectivity Test Tool
Phase 2: Link (Connectivity Verification)

Purpose: Test Jira API connection using provided credentials.
Status: Deterministic, no LLM logic here.
"""

import os
import requests
import json
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JiraClient:
    """Minimal Jira REST API client for connectivity testing and issue fetching."""
    
    def __init__(self):
        """Initialize Jira client with credentials from .env"""
        self.jira_url = os.getenv('JIRA_URL', '').rstrip('/')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        
        # Validate credentials
        if not all([self.jira_url, self.jira_email, self.jira_token]):
            raise ValueError("Missing Jira credentials in .env file")
        
        self.session = requests.Session()
        self.session.auth = (self.jira_email, self.jira_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def test_connection(self) -> bool:
        """
        Test connectivity to Jira API.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            response = self.session.get(f"{self.jira_url}/rest/api/3/myself")
            response.raise_for_status()
            print("✅ Jira API connection successful")
            print(f"   Connected as: {response.json().get('displayName')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Jira API connection failed: {str(e)}")
            return False
    
    def fetch_issue(self, issue_key: str) -> Optional[Dict]:
        """
        Fetch a Jira issue by key.
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            
        Returns:
            dict: Issue data or None if fetch failed
        """
        try:
            url = f"{self.jira_url}/rest/api/3/issue/{issue_key}"
            params = {
                'expand': 'renderedFields,changelog',
                'fields': [
                    'summary',
                    'description',
                    'status',
                    'priority',
                    'labels',
                    'components',
                    'assignee',
                    'created',
                    'updated',
                    'customfield_10001'
                ]
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            issue_data = response.json()
            print(f"✅ Issue {issue_key} fetched successfully")
            return issue_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch issue {issue_key}: {str(e)}")
            return None
    
    def normalize_issue(self, issue_data: Dict) -> Dict:
        """
        Normalize raw Jira issue data to internal schema.
        
        Args:
            issue_data: Raw Jira API response
            
        Returns:
            dict: Normalized issue data
        """
        fields = issue_data.get('fields', {})
        
        normalized = {
            'issueKey': issue_data.get('key'),
            'title': fields.get('summary', 'N/A'),
            'type': issue_data.get('type', {}).get('name', 'Unknown'),
            'status': fields.get('status', {}).get('name', 'Unknown'),
            'priority': fields.get('priority', {}).get('name', 'N/A'),
            'summary': fields.get('summary', ''),
            'description': fields.get('description', ''),
            'acceptanceCriteria': [],  # To be extracted from description
            'labels': fields.get('labels', []),
            'components': [c.get('name') for c in fields.get('components', [])],
            'linkedIssues': [],
            'linkedSubtasks': [],
            'dataQuality': {
                'hasMissingAcceptanceCriteria': not fields.get('description', '').strip(),
                'hasAmbiguousRequirements': False,
                'flags': []
            }
        }
        
        # Flag missing acceptance criteria
        if not normalized['description']:
            normalized['dataQuality']['flags'].append(
                "WARNING: Issue description is empty - acceptance criteria may be missing"
            )
        
        return normalized


def main():
    """
    Main entry point for connectivity testing.
    Phase 2: Link verification.
    """
    print("=" * 60)
    print("🔗 PHASE 2: LINK - Jira Connectivity Test")
    print("=" * 60)
    
    try:
        # Initialize client
        client = JiraClient()
        print("\n1. Testing Jira API Connection...")
        
        # Test connection
        if not client.test_connection():
            print("❌ Connection test failed. Check credentials in .env file.")
            return
        
        # Prompt for issue key (for demonstration)
        print("\n2. Ready to fetch issues. Provide an issue key to test.")
        issue_key = input("   Enter Jira issue key (or press Enter to skip): ").strip()
        
        if issue_key:
            print(f"\n3. Fetching issue {issue_key}...")
            issue_data = client.fetch_issue(issue_key)
            
            if issue_data:
                print("\n4. Normalizing issue data...")
                normalized = client.normalize_issue(issue_data)
                
                print("\n✅ Normalized Issue Data:")
                print(json.dumps(normalized, indent=2))
                
                # Save to temporary file
                tmp_file = f".tmp/{issue_key}_normalized.json"
                os.makedirs('.tmp', exist_ok=True)
                with open(tmp_file, 'w') as f:
                    json.dump(normalized, f, indent=2)
                print(f"\n📁 Saved to: {tmp_file}")
                
        print("\n" + "=" * 60)
        print("✅ Phase 2: Link Test Complete")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during connectivity test: {str(e)}")


if __name__ == "__main__":
    main()
