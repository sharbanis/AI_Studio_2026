"""
Test Case Generator - Generate test cases using Groq LLM
Layer 3: Tools (Content Generation)

Purpose: Use Groq LLM to generate structured test cases by category
Status: Phase 3 Implementation
"""

import re
import json
from typing import Dict, List, Optional


class TestCaseGenerator:
    """Generate test cases from normalized issue data using Groq LLM."""
    
    def __init__(self, groq_client):
        """Initialize with Groq client."""
        self.groq_client = groq_client
    
    def generate_test_cases(self, issue_data: Dict, category: str) -> List[Dict]:
        """
        Generate test cases for a specific category.
        
        Args:
            issue_data: Normalized issue data
            category: Test category (happy_path, negative, edge_cases, regression)
            
        Returns:
            list: Generated test cases
        """
        # Build prompt for this category
        prompt = self._build_prompt(issue_data, category)
        
        # Call Groq LLM
        llm_response = self.groq_client.generate_test_cases(issue_data, category)
        
        if not llm_response:
            return []
        
        # Parse response
        test_cases = self._parse_test_cases(llm_response, category)
        
        # Validate each test case
        valid_cases = []
        for tc in test_cases:
            validation_errors = self._validate_test_case(tc)
            if not validation_errors:
                valid_cases.append(tc)
            else:
                print(f"⚠️  Skipping invalid test case: {tc.get('title', 'Unknown')}")
        
        return valid_cases
    
    def _build_prompt(self, issue_data: Dict, category: str) -> str:
        """Build category-specific prompt."""
        prompts = {
            "happy_path": self._prompt_happy_path,
            "negative": self._prompt_negative,
            "edge_cases": self._prompt_edge_cases,
            "regression": self._prompt_regression
        }
        
        prompt_func = prompts.get(category, self._prompt_happy_path)
        return prompt_func(issue_data)
    
    def _prompt_happy_path(self, issue: Dict) -> str:
        """Prompt for happy path test cases."""
        return f"""Generate 2-3 HAPPY PATH test cases for this requirement.

Title: {issue['title']}
Description: {issue['description'][:300]}
Acceptance Criteria: {', '.join(issue.get('acceptanceCriteria', [])[:3])}

Format EXACTLY as:
TC-001-HAPPY
Title: [Test title]
Steps:
1. [Step 1]
2. [Step 2]
Expected Result: [Result]
Priority: High

Do NOT include error handling or negative scenarios.
Focus on the happy path where requirements work correctly."""
    
    def _prompt_negative(self, issue: Dict) -> str:
        """Prompt for negative test cases."""
        return f"""Generate 2-3 NEGATIVE test cases for this requirement.

Title: {issue['title']}
Description: {issue['description'][:300]}

Format EXACTLY as:
TC-001-NEGATIVE
Title: [Test title]
Steps:
1. [Step 1]
Expected Result: [Error message or rejection]
Priority: High

Focus on invalid input handling and error messages."""
    
    def _prompt_edge_cases(self, issue: Dict) -> str:
        """Prompt for edge case test cases."""
        return f"""Generate 2-3 EDGE CASE test cases for this requirement.

Title: {issue['title']}
Description: {issue['description'][:300]}

Format EXACTLY as:
TC-001-EDGE
Title: [Test title]
Steps:
1. [Step 1]
Expected Result: [Result]
Priority: Medium

Focus on boundary conditions and corner cases."""
    
    def _prompt_regression(self, issue: Dict) -> str:
        """Prompt for regression test cases."""
        return f"""Generate 2-3 REGRESSION test cases for this requirement.

Title: {issue['title']}
Description: {issue['description'][:300]}

Format EXACTLY as:
TC-001-REGRESSION
Title: [Test title]
Steps:
1. [Step 1]
Expected Result: [Feature works]
Priority: High

Focus on verifying existing functionality still works."""
    
    def _parse_test_cases(self, llm_response: str, category: str) -> List[Dict]:
        """Parse LLM response into test case objects."""
        test_cases = []
        
        # Split by TC-XXX markers
        parts = re.split(r'^TC-(\d+)[-\s]', llm_response, flags=re.MULTILINE)
        
        for i in range(1, len(parts), 2):
            if i + 1 >= len(parts):
                break
            
            tc_num = parts[i].strip()
            tc_text = parts[i + 1]
            
            # Extract fields
            title_match = re.search(r'Title:\s*(.+?)(?:\n|$)', tc_text, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else f"Test Case {tc_num}"
            
            # Extract steps
            steps_match = re.search(r'Steps?:\s*(.*?)(?=Expected|Priority|$)', tc_text, re.IGNORECASE | re.DOTALL)
            steps = []
            if steps_match:
                steps_text = steps_match.group(1)
                # Split by numbered lines
                step_lines = re.findall(r'^\s*\d+[\.\)]\s+(.+?)$', steps_text, re.MULTILINE)
                steps = [step.strip() for step in step_lines if step.strip()]
            
            # Extract expected result
            expected_match = re.search(r'Expected Result:\s*(.+?)(?:\n|Priority|$)', tc_text, re.IGNORECASE)
            expected = expected_match.group(1).strip() if expected_match else "Test passes"
            
            # Extract priority
            priority_match = re.search(r'Priority:\s*(High|Medium|Low)', tc_text, re.IGNORECASE)
            priority = priority_match.group(1) if priority_match else 'Medium'
            
            test_case = {
                'id': f'TC-{tc_num.zfill(3)}-{category.upper()}',
                'category': category,
                'title': title,
                'steps': steps if steps else [title],  # Fallback if no steps
                'expectedResult': expected,
                'priority': priority
            }
            
            test_cases.append(test_case)
        
        return test_cases
    
    def _validate_test_case(self, tc: Dict) -> List[str]:
        """Validate test case quality."""
        errors = []
        
        # Check title
        if not tc.get('title') or len(tc['title']) < 5:
            errors.append("Title too short or missing")
        
        # Check steps
        if not tc.get('steps') or len(tc['steps']) == 0:
            errors.append("No steps provided")
        else:
            for step in tc['steps']:
                if len(step) < 3:
                    errors.append(f"Step too short: '{step}'")
        
        # Check expected result
        if not tc.get('expectedResult') or len(tc['expectedResult']) < 3:
            errors.append("Expected result missing or too short")
        
        # Check priority
        if tc.get('priority') not in ['High', 'Medium', 'Low']:
            errors.append(f"Invalid priority: {tc.get('priority')}")
        
        return errors
