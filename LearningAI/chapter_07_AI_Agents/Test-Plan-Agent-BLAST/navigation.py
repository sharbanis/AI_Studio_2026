"""
Navigation Layer - Orchestrate the complete test plan generation pipeline
Layer 2: Navigation/Orchestration

Purpose: Coordinate Fetch -> Normalize -> Generate -> Validate -> Format
Status: Phase 3 Implementation
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

from tools.jira_client import JiraClient
from tools.groq_client import GroqClient
from tools.normalizer import DataNormalizer
from tools.test_generator import TestCaseGenerator
from tools.validator import TestValidator


class TestPlanOrchestrator:
    """Orchestrate the complete test plan generation pipeline."""
    
    def __init__(self):
        """Initialize all components."""
        self.jira = JiraClient()
        self.groq = GroqClient()
        self.normalizer = DataNormalizer()
        self.generator = TestCaseGenerator(self.groq)
        self.validator = TestValidator()
        
        # Create tmp directory if needed
        os.makedirs('.tmp', exist_ok=True)
    
    def generate_test_plan(self, issue_key: str) -> Dict:
        """
        Generate complete test plan from Jira issue ID.
        
        Args:
            issue_key: Jira issue key (e.g., "PROJ-123")
            
        Returns:
            dict: Complete test plan with metadata, test cases, and coverage
        """
        try:
            print(f"\n📋 Generating test plan for: {issue_key}")
            
            # Step 1: Fetch issue
            print("   1/5 Fetching issue from Jira...")
            raw_issue = self.jira.fetch_issue(issue_key)
            if not raw_issue:
                return {
                    'error': f'Issue {issue_key} not found',
                    'issueKey': issue_key
                }
            
            # Step 2: Normalize
            print("   2/5 Normalizing data...")
            normalized_issue = self.normalizer.normalize_issue(raw_issue)
            
            # Step 3: Generate test cases for each category
            print("   3/5 Generating test cases (Groq LLM)...")
            test_cases_by_category = {}
            for category in ['happy_path', 'negative', 'edge_cases', 'regression']:
                test_cases = self.generator.generate_test_cases(normalized_issue, category)
                test_cases_by_category[category] = test_cases
                print(f"      - {category}: {len(test_cases)} test cases")
            
            # Step 4: Validate
            print("   4/5 Validating and formatting...")
            output = self.validator.validate_and_format(normalized_issue, test_cases_by_category)
            
            # Step 5: Generate Markdown
            print("   5/5 Generating Markdown output...")
            markdown = self.validator.generate_markdown(output)
            
            # Save outputs
            self._save_outputs(issue_key, output, markdown)
            
            print(f"✅ Test plan generated successfully!\n")
            
            return output
            
        except Exception as e:
            return {
                'error': f'Error generating test plan: {str(e)}',
                'issueKey': issue_key
            }
    
    def _save_outputs(self, issue_key: str, json_output: Dict, markdown: str):
        """Save JSON and Markdown outputs to files."""
        try:
            # Save JSON
            json_file = f'.tmp/{issue_key}_test_plan.json'
            with open(json_file, 'w') as f:
                json.dump(json_output, f, indent=2)
            
            # Save Markdown
            md_file = f'.tmp/{issue_key}_test_plan.md'
            with open(md_file, 'w') as f:
                f.write(markdown)
            
        except Exception as e:
            print(f"⚠️  Could not save output files: {str(e)}")
