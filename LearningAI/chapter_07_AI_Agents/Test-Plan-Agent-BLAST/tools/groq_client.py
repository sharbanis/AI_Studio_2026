"""
Groq LLM Client - Minimal Connectivity Test Tool
Phase 2: Link (Connectivity Verification)

Purpose: Test Groq API connection using provided credentials.
Status: Deterministic, test-only logic.
"""

import os
import json
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GroqClient:
    """Minimal Groq API client for connectivity testing and LLM calls."""
    
    def __init__(self):
        """Initialize Groq client with API key from .env"""
        self.api_key = os.getenv('GROQ_API_KEY')
        self.model = None  # Will be set after successful connection
        
        if not self.api_key:
            raise ValueError("Missing GROQ_API_KEY in .env file")
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            self.is_available = True
        except ImportError:
            print("⚠️  Groq library not installed. Install with: pip install groq")
            self.is_available = False
    
    def test_connection(self) -> bool:
        """
        Test connectivity to Groq API with a minimal prompt.
        Tries multiple models to find one that works.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        if not self.is_available:
            return False
        
        # Try models in order of preference (updated based on available models)
        available_models = [
            "qwen/qwen3.8-27b",
            "allam-2-7b",
            "openai/gpt-oss-120b",
            "groq/compound",
            "mixtral-8x7b-32768"
        ]
        
        for model in available_models:
            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": "Say 'Connected' exactly."
                        }
                    ],
                    model=model,
                    max_tokens=10
                )
                
                result = response.choices[0].message.content.strip()
                self.model = model  # Store working model
                print("✅ Groq API connection successful")
                print(f"   Model: {model}")
                print(f"   Response: {result}")
                return True
                
            except Exception as e:
                if "decommissioned" in str(e) or "not found" in str(e) or "does not exist" in str(e):
                    continue  # Try next model
                else:
                    print(f"⚠️  Model {model} error: {str(e)[:80]}")
                    continue
        
        print("❌ No suitable Groq models found. Check available models.")
        print("   Available models: qwen/qwen3.8-27b, allam-2-7b, openai/gpt-oss-120b, groq/compound")
        return False
    
    def generate_test_cases(self, issue_data: Dict, test_category: str = "happy_path") -> Optional[str]:
        """
        Generate test cases from issue data using Groq LLM.
        
        Args:
            issue_data: Normalized issue data
            test_category: Category (happy_path, negative, edge_cases, regression)
            
        Returns:
            str: Generated test cases or None if failed
        """
        if not self.is_available or not self.model:
            return None
        
        try:
            # Build prompt
            prompt = self._build_test_generation_prompt(issue_data, test_category)
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a QA test case generation expert. Generate clear, formal test cases based on requirements."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,  # Lower temperature for deterministic output
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Failed to generate test cases: {str(e)}")
            return None
    
    def _build_test_generation_prompt(self, issue_data: Dict, category: str) -> str:
        """
        Build the prompt for test case generation.
        
        Args:
            issue_data: Normalized issue data
            category: Test category
            
        Returns:
            str: Formatted prompt
        """
        prompt_templates = {
            "happy_path": """Generate 2-3 Happy Path test cases for this issue.
Happy path tests verify that the feature works correctly when all inputs are valid.

Issue: {title}
Description: {description}
Acceptance Criteria: {criteria}

Format each test case as:
TC-ID: [ID]
Title: [title]
Steps: [step 1, step 2, ...]
Expected Result: [result]
Priority: [High/Medium/Low]""",
            
            "negative": """Generate 2-3 Negative test cases for this issue.
Negative tests verify that the system handles invalid inputs and errors correctly.

Issue: {title}
Description: {description}

Format each test case as:
TC-ID: [ID]
Title: [title]
Steps: [step 1, step 2, ...]
Expected Result: [error handling/validation message]
Priority: [High/Medium/Low]""",
            
            "edge_cases": """Generate 2-3 Edge Case test cases for this issue.
Edge cases test boundary conditions and extreme values.

Issue: {title}
Description: {description}

Format each test case as:
TC-ID: [ID]
Title: [title]
Steps: [step 1, step 2, ...]
Expected Result: [result]
Priority: [High/Medium/Low]""",
            
            "regression": """Generate 2-3 Regression test cases for this issue.
Regression tests verify that existing functionality still works.

Issue: {title}
Description: {description}

Format each test case as:
TC-ID: [ID]
Title: [title]
Steps: [step 1, step 2, ...]
Expected Result: [result]
Priority: [High/Medium/Low]"""
        }
        
        template = prompt_templates.get(category, prompt_templates["happy_path"])
        
        description = issue_data.get('description', 'N/A')
        criteria = ", ".join(issue_data.get('acceptanceCriteria', ['N/A']))
        
        return template.format(
            title=issue_data.get('title', 'N/A'),
            description=description,
            criteria=criteria
        )


def main():
    """
    Main entry point for Groq connectivity testing.
    Phase 2: Link verification.
    """
    print("=" * 60)
    print("🔗 PHASE 2: LINK - Groq LLM Connectivity Test")
    print("=" * 60)
    
    try:
        # Initialize client
        client = GroqClient()
        print("\n1. Testing Groq API Connection...")
        
        # Check if library is available
        if not client.is_available:
            print("⚠️  Groq library not installed. Installation required.")
            print("    Run: pip install groq")
            return
        
        # Test connection
        if not client.test_connection():
            print("❌ Connection test failed. Check GROQ_API_KEY in .env file.")
            return
        
        print("\n2. Groq API is ready for test case generation.")
        print("   (Generation will be tested in Phase 3 with real Jira data)")
        
        print("\n" + "=" * 60)
        print("✅ Phase 2: Groq Link Test Complete")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during connectivity test: {str(e)}")


if __name__ == "__main__":
    main()
