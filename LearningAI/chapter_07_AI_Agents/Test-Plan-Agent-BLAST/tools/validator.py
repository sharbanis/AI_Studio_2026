"""
Validator - Validate test cases and generate outputs
Layer 3: Tools (Quality Assurance)

Purpose: Validate test case quality, check coverage, and format output
Status: Phase 3 Implementation
"""

import json
from typing import Dict, List, Any
from datetime import datetime


class TestValidator:
    """Validate and format test plan output."""
    
    def validate_and_format(self, issue_data: Dict, test_cases_by_category: Dict) -> Dict:
        """
        Validate all test cases and generate final output.
        
        Args:
            issue_data: Normalized issue data
            test_cases_by_category: Dict of test cases organized by category
            
        Returns:
            dict: Complete formatted test plan
        """
        # Flatten test cases
        all_test_cases = []
        for category, cases in test_cases_by_category.items():
            all_test_cases.extend(cases)
        
        # Validation checks
        coverage = self._check_coverage(all_test_cases, issue_data.get('acceptanceCriteria', []))
        priority_dist = self._check_priority_distribution(all_test_cases)
        validation_issues = self._validate_all_test_cases(all_test_cases, issue_data)
        
        # Remove duplicates
        unique_cases = self._remove_duplicates(all_test_cases)
        
        # Generate output
        output = {
            'metadata': {
                'project': issue_data['issueKey'].split('-')[0],
                'issueKey': issue_data['issueKey'],
                'issueTitle': issue_data['title'],
                'issueType': issue_data['type'],
                'priority': issue_data.get('priority', 'Medium'),
                'status': issue_data.get('status', 'Unknown'),
                'generatedAt': datetime.now().isoformat() + 'Z',
                'llmProvider': 'groq',
                'llmModel': 'qwen/qwen3.8-27b',
                'validationStatus': 'PASSED' if not validation_issues else 'WARNINGS'
            },
            'testPlan': {
                'objective': self._generate_objective(issue_data),
                'scope': self._generate_scope(issue_data),
                'preconditions': self._generate_preconditions(issue_data),
                'testCases': unique_cases
            },
            'coverage': coverage,
            'priorityDistribution': priority_dist,
            'dataQualityFlags': issue_data.get('dataQuality', {}).get('flags', []),
            'validationWarnings': validation_issues
        }
        
        return output
    
    def _check_coverage(self, test_cases: List[Dict], acceptance_criteria: List[str]) -> Dict:
        """Check if test cases cover acceptance criteria."""
        if not acceptance_criteria:
            return {
                'totalCriteria': 0,
                'coveredCriteria': 0,
                'coveragePercent': 0,
                'missingCoverage': []
            }
        
        covered_criteria = set()
        
        for tc in test_cases:
            tc_text = f"{tc.get('title', '')} {' '.join(tc.get('steps', []))} {tc.get('expectedResult', '')}".lower()
            
            for i, criterion in enumerate(acceptance_criteria):
                criterion_lower = criterion.lower()
                # Check if criterion words appear in test case
                criterion_words = [w for w in criterion_lower.split() if len(w) > 3]
                if criterion_words and all(word in tc_text for word in criterion_words[:2]):
                    covered_criteria.add(i)
        
        total = len(acceptance_criteria)
        covered = len(covered_criteria)
        
        missing = [acceptance_criteria[i] for i in range(total) if i not in covered_criteria]
        
        return {
            'totalCriteria': total,
            'coveredCriteria': covered,
            'coveragePercent': (covered / total * 100) if total > 0 else 0,
            'missingCoverage': missing
        }
    
    def _check_priority_distribution(self, test_cases: List[Dict]) -> Dict:
        """Check priority distribution."""
        by_priority = {
            'High': len([tc for tc in test_cases if tc.get('priority') == 'High']),
            'Medium': len([tc for tc in test_cases if tc.get('priority') == 'Medium']),
            'Low': len([tc for tc in test_cases if tc.get('priority') == 'Low'])
        }
        
        total = sum(by_priority.values())
        
        if total == 0:
            return {
                'distribution': by_priority,
                'percentageByPriority': {},
                'warnings': ['No test cases generated']
            }
        
        percent = {k: v / total * 100 for k, v in by_priority.items()}
        
        warnings = []
        critical_pct = (by_priority['High'] + by_priority['Medium']) / total * 100
        if critical_pct < 50:
            warnings.append(f"Warning: Only {critical_pct:.1f}% of tests are High/Medium priority")
        
        return {
            'distribution': by_priority,
            'percentageByPriority': percent,
            'warnings': warnings
        }
    
    def _validate_all_test_cases(self, test_cases: List[Dict], issue_data: Dict) -> List[str]:
        """Validate all test cases."""
        warnings = []
        
        for tc in test_cases:
            # Check traceability
            if not self._is_traceable(tc, issue_data):
                warnings.append(f"Test '{tc.get('title', '')}' may not relate to requirements")
        
        return warnings
    
    def _is_traceable(self, test_case: Dict, issue_data: Dict) -> bool:
        """Check if test case is traceable to requirements."""
        tc_text = f"{test_case.get('title', '')} {' '.join(test_case.get('steps', []))}".lower()
        issue_text = f"{issue_data.get('title', '')} {issue_data.get('description', '')}".lower()
        
        # Check for some overlap in keywords
        tc_words = set(tc_text.split())
        issue_words = set(issue_text.split())
        
        overlap = len(tc_words & issue_words)
        return overlap > 3
    
    def _remove_duplicates(self, test_cases: List[Dict]) -> List[Dict]:
        """Remove duplicate test cases."""
        unique = []
        seen_titles = set()
        
        for tc in test_cases:
            title_lower = tc.get('title', '').lower().strip()
            
            if title_lower in seen_titles:
                continue
            
            # Check for similarity
            is_similar = False
            for existing in unique:
                existing_title = existing.get('title', '').lower()
                if self._string_similarity(title_lower, existing_title) > 0.85:
                    is_similar = True
                    break
            
            if not is_similar:
                unique.append(tc)
                seen_titles.add(title_lower)
        
        return unique
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity."""
        if not str1 or not str2:
            return 0.0
        
        # Simple similarity check
        longer = str1 if len(str1) > len(str2) else str2
        shorter = str2 if len(str1) > len(str2) else str1
        
        if len(longer) == 0:
            return 1.0
        
        edit_distance = self._levenshtein(shorter, longer)
        return (len(longer) - edit_distance) / float(len(longer))
    
    def _levenshtein(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance."""
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _generate_objective(self, issue: Dict) -> str:
        """Generate test plan objective."""
        title = issue.get('title', 'Verify requirement')
        return f"Verify {title.lower()}"
    
    def _generate_scope(self, issue: Dict) -> List[str]:
        """Generate test scope."""
        scope = []
        
        if issue.get('components'):
            scope.extend(issue['components'])
        
        if issue.get('labels'):
            scope.extend(issue['labels'])
        
        if not scope:
            scope = ['Core functionality', 'User interface', 'Integration']
        
        return scope[:3]  # Limit to 3 items
    
    def _generate_preconditions(self, issue: Dict) -> List[str]:
        """Generate test preconditions."""
        preconditions = []
        
        issue_type = issue.get('type', '').lower()
        
        if 'login' in issue.get('title', '').lower():
            preconditions.append('User account exists')
        
        if issue.get('components'):
            preconditions.append(f"{issue['components'][0]} module is accessible")
        
        if not preconditions:
            preconditions = [
                'Test environment is available',
                'User has necessary permissions',
                'System is in a clean state'
            ]
        
        return preconditions
    
    def generate_markdown(self, output: Dict) -> str:
        """Generate Markdown output."""
        metadata = output['metadata']
        test_plan = output['testPlan']
        
        markdown = f"""# Test Plan: {metadata['issueTitle']}

**Issue:** {metadata['issueKey']}  
**Type:** {metadata['issueType']}  
**Priority:** {metadata['priority']}  
**Status:** {metadata['status']}  
**Generated:** {metadata['generatedAt']}  
**LLM Model:** {metadata['llmModel']}  

## Objective
{test_plan['objective']}

## Scope
{chr(10).join(f"- {item}" for item in test_plan['scope'])}

## Preconditions
{chr(10).join(f"- {item}" for item in test_plan['preconditions'])}

## Test Cases

"""
        
        # Organize by category
        by_category = {}
        for tc in test_plan.get('testCases', []):
            category = tc.get('category', 'other')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(tc)
        
        # Format each category
        category_names = {
            'happy_path': 'Happy Path (Positive Scenarios)',
            'negative': 'Negative Scenarios (Error Handling)',
            'edge_cases': 'Edge Cases (Boundary Conditions)',
            'regression': 'Regression Tests'
        }
        
        for category in ['happy_path', 'negative', 'edge_cases', 'regression']:
            if category not in by_category:
                continue
            
            markdown += f"### {category_names.get(category, category)}\n\n"
            
            for tc in by_category[category]:
                markdown += f"**{tc['id']}: {tc['title']}** (Priority: {tc['priority']})\n"
                markdown += "- Steps:\n"
                for i, step in enumerate(tc.get('steps', []), 1):
                    markdown += f"  {i}. {step}\n"
                markdown += f"- Expected Result: {tc.get('expectedResult', 'N/A')}\n\n"
        
        # Add coverage info
        coverage = output.get('coverage', {})
        if coverage:
            markdown += f"""## Coverage
- Total Acceptance Criteria: {coverage['totalCriteria']}
- Covered: {coverage['coveredCriteria']}
- Coverage: {coverage['coveragePercent']:.1f}%

"""
        
        # Add quality notes
        if output.get('dataQualityFlags'):
            markdown += "## Quality Flags\n"
            for flag in output['dataQualityFlags']:
                markdown += f"- {flag}\n"
        
        return markdown
