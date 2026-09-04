"""
Data Normalizer - Convert raw Jira data to internal schema
Layer 3: Tools (Deterministic processing)

Purpose: Normalize heterogeneous Jira data into consistent internal schema
Status: Phase 3 Implementation
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime


class DataNormalizer:
    """Normalize raw Jira issue data to internal schema."""
    
    def normalize_issue(self, raw_issue: Dict) -> Dict:
        """
        Convert raw Jira API response to normalized internal schema.
        
        Args:
            raw_issue: Raw Jira REST API response
            
        Returns:
            dict: Normalized issue data following internal schema
        """
        if not raw_issue or not raw_issue.get('fields'):
            return self._empty_normalized_schema()
        
        fields = raw_issue['fields']
        
        # Extract core fields
        normalized = {
            'issueKey': raw_issue.get('key', 'UNKNOWN'),
            'title': fields.get('summary', 'Untitled'),
            'type': fields.get('issuetype', {}).get('name', 'Unknown'),
            'status': fields.get('status', {}).get('name', 'Unknown'),
            'priority': fields.get('priority', {}).get('name', 'Medium'),
            'summary': self._coerce_to_text(fields.get('summary', '')),
            'description': self._coerce_to_text(fields.get('description', '')) or '',
            'acceptanceCriteria': [],
            'labels': self._normalize_labels(fields.get('labels', [])),
            'components': self._normalize_components(fields.get('components', [])),
            'assignee': self._normalize_assignee(fields.get('assignee')),
            'createdAt': self._normalize_date(fields.get('created')),
            'updatedAt': self._normalize_date(fields.get('updated')),
            'linkedIssues': self._extract_linked_issues(fields.get('issuelinks', [])),
            'linkedSubtasks': self._extract_subtasks(fields.get('subtasks', [])),
            'dataQuality': {
                'hasMissingAcceptanceCriteria': True,
                'hasAmbiguousRequirements': False,
                'missingFields': [],
                'flags': []
            }
        }
        
        # Extract acceptance criteria
        acceptance_criteria = self._extract_acceptance_criteria(
            fields.get('customfield_10001'),
            normalized['description']
        )
        normalized['acceptanceCriteria'] = acceptance_criteria
        
        # Quality assessment
        if normalized['acceptanceCriteria']:
            normalized['dataQuality']['hasMissingAcceptanceCriteria'] = False
        else:
            normalized['dataQuality']['flags'].append(
                "WARNING: No acceptance criteria found in Jira issue"
            )
        
        if not normalized['description']:
            normalized['dataQuality']['flags'].append(
                "WARNING: Issue description is empty"
            )
        
        # Detect ambiguous language
        if self._has_ambiguous_language(normalized['description']):
            normalized['dataQuality']['hasAmbiguousRequirements'] = True
            normalized['dataQuality']['flags'].append(
                "WARNING: Description contains vague language (should/may/might)"
            )
        
        return normalized
    
    def _normalize_labels(self, labels: List) -> List[str]:
        """Normalize labels to lowercase strings."""
        if not labels:
            return []
        return [label.lower().strip() for label in labels if label]
    
    def _normalize_components(self, components: List) -> List[str]:
        """Extract component names."""
        if not components:
            return []
        return [comp.get('name', '') for comp in components if comp.get('name')]
    
    def _normalize_assignee(self, assignee: Optional[Dict]) -> Dict:
        """Extract assignee information."""
        if not assignee:
            return {'name': 'Unassigned', 'email': None}
        return {
            'name': assignee.get('displayName', 'Unknown'),
            'email': assignee.get('emailAddress')
        }
    
    def _normalize_date(self, date_string: Optional[str]) -> str:
        """Convert Jira date to ISO 8601 format."""
        if not date_string:
            return datetime.now().isoformat() + 'Z'
        
        try:
            # Parse Jira date format: "2026-09-01T10:00:00.000-0400"
            # Remove timezone info and convert to UTC Z notation
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        except:
            return datetime.now().isoformat() + 'Z'
    
    def _coerce_to_text(self, value: Any) -> str:
        """Convert Jira field values (string, list, dict) to a plain text string."""
        if value is None:
            return ''
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            parts = []
            for item in value:
                text = self._coerce_to_text(item)
                if text:
                    parts.append(text)
            return '\n'.join(parts)
        if isinstance(value, dict):
            # Handle Atlassian document format: {"type":"doc","content":[...]}
            if 'text' in value and isinstance(value['text'], str):
                return value['text']
            text_parts = []
            for key in ('text', 'value', 'content'):
                if key in value:
                    text_parts.append(self._coerce_to_text(value[key]))
            if text_parts:
                return '\n'.join(part for part in text_parts if part)
            return str(value)
        return str(value)

    def _extract_acceptance_criteria(self, custom_field: Optional[str], description: str) -> List[str]:
        """Extract acceptance criteria from custom field or description."""
        criteria = []

        custom_text = self._coerce_to_text(custom_field)
        if custom_text and custom_text.strip():
            criteria = self._parse_criteria_text(custom_text)
            if criteria:
                return criteria

        description_text = self._coerce_to_text(description)
        if description_text:
            # Look for "Given/When/Then" pattern (Gherkin style)
            gherkin_criteria = self._extract_gherkin_criteria(description_text)
            if gherkin_criteria:
                return gherkin_criteria

            # Look for bullet points
            bullet_criteria = self._extract_bullet_criteria(description_text)
            if bullet_criteria:
                return bullet_criteria

            # Look for "Acceptance Criteria:" section
            ac_criteria = self._extract_ac_section(description_text)
            if ac_criteria:
                return ac_criteria

        return []

    def _parse_criteria_text(self, text: str) -> List[str]:
        """Parse criteria text into list of strings."""
        text = self._coerce_to_text(text)
        if not text:
            return []

        lines = text.split('\n')
        return [line.strip() for line in lines if line.strip() and len(line.strip()) > 3]

    def _extract_gherkin_criteria(self, description: str) -> List[str]:
        """Extract Gherkin-style criteria (Given/When/Then)."""
        description = self._coerce_to_text(description)
        if not description:
            return []

        criteria = []
        lines = description.split('\n')

        for i, line in enumerate(lines):
            lower_line = line.lower().strip()
            if lower_line.startswith(('given', 'when', 'then', 'and')):
                # Found Gherkin line
                scenario = line.strip()
                # Group consecutive Gherkin lines
                if i > 0 and criteria and criteria[-1].startswith(('Given', 'When', 'Then', 'And')):
                    criteria[-1] = f"{criteria[-1]}\n{scenario}"
                else:
                    criteria.append(scenario)

        return criteria if criteria else []

    def _extract_bullet_criteria(self, description: str) -> List[str]:
        """Extract bullet-point criteria (✓, •, -, *)."""
        description = self._coerce_to_text(description)
        if not description:
            return []

        criteria = []
        lines = description.split('\n')

        for line in lines:
            stripped = line.strip()
            if stripped and stripped[0] in ['✓', '•', '-', '*']:
                criteria.append(stripped[1:].strip())

        return criteria if criteria else []

    def _extract_ac_section(self, description: str) -> List[str]:
        """Extract 'Acceptance Criteria:' section."""
        description = self._coerce_to_text(description)
        if not description or 'acceptance criteria' not in description.lower():
            return []

        lines = description.split('\n')
        in_ac_section = False
        criteria = []

        for line in lines:
            if 'acceptance criteria' in line.lower():
                in_ac_section = True
                continue

            if in_ac_section:
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped[0] in ['✓', '•', '-', '*', '1', '2', '3']:
                    # Remove bullet marker
                    content = re.sub(r'^[✓•\-*\d]+[\.\)]*\s*', '', stripped)
                    if content:
                        criteria.append(content)
                elif criteria:  # Stop if we hit non-criteria line after starting
                    break

        return criteria
    
    def _extract_linked_issues(self, issuelinks: List) -> List[str]:
        """Extract linked issue keys."""
        linked = []
        for link in issuelinks:
            if 'outwardIssue' in link:
                issue_key = link['outwardIssue'].get('key')
                if issue_key:
                    linked.append(issue_key)
            elif 'inwardIssue' in link:
                issue_key = link['inwardIssue'].get('key')
                if issue_key:
                    linked.append(issue_key)
        
        return linked
    
    def _extract_subtasks(self, subtasks: List) -> List[str]:
        """Extract subtask keys."""
        return [st.get('key') for st in subtasks if st.get('key')]
    
    def _has_ambiguous_language(self, text: str) -> bool:
        """Detect vague language in requirements."""
        text = self._coerce_to_text(text)
        if not text:
            return False

        vague_patterns = [
            r'\bshould\b',  # "should" instead of "must"
            r'\bmay\b',
            r'\bmight\b',
            r'\bcould\b',
            r'\betc\b',
            r'\band so on\b',
            r'\bas needed\b',
            r'\bif applicable\b',
            r'\bsimilar to\b',
            r'\blike\b.*\btesting',
            r'\bsomewhat\b'
        ]

        text_lower = text.lower()
        vague_count = sum(1 for pattern in vague_patterns if re.search(pattern, text_lower))

        return vague_count > 2
    
    def _empty_normalized_schema(self) -> Dict:
        """Return empty normalized schema."""
        return {
            'issueKey': 'UNKNOWN',
            'title': 'Unknown Issue',
            'type': 'Unknown',
            'status': 'Unknown',
            'priority': 'Medium',
            'summary': '',
            'description': '',
            'acceptanceCriteria': [],
            'labels': [],
            'components': [],
            'assignee': {'name': 'Unassigned', 'email': None},
            'createdAt': datetime.now().isoformat() + 'Z',
            'updatedAt': datetime.now().isoformat() + 'Z',
            'linkedIssues': [],
            'linkedSubtasks': [],
            'dataQuality': {
                'hasMissingAcceptanceCriteria': True,
                'hasAmbiguousRequirements': False,
                'missingFields': ['all'],
                'flags': ['ERROR: Could not parse Jira issue']
            }
        }
