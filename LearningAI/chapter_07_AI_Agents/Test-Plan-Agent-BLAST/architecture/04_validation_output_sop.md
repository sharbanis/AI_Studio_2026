# Layer 1: Validation & Output SOP (Standard Operating Procedure)

**Layer:** 1 (Architecture/Technical SOPs)  
**Purpose:** Validate generated test plan against source requirements and format for output  
**Owner:** validator.py (to be built in Phase 3)  
**Status:** Ready for Phase 3 implementation

---

## Objective
Ensure all generated test cases are valid, traceable to requirements, and properly formatted for delivery in JSON and Markdown formats.

## Inputs
```json
{
  "issueKey": "PROJ-123",
  "issueTitle": "User login should validate credentials",
  "acceptanceCriteria": ["Invalid email rejected", "Wrong password shows error"],
  "testCasesByCategory": {
    "happy_path": [...],
    "negative": [...],
    "edge_cases": [...],
    "regression": [...]
  },
  "dataQualityFlags": []
}
```

## Process Flow

### Step 1: Validate Test Cases Against Requirements
For each generated test case, verify traceability:

```python
def validate_traceability(test_case, issue_data):
    """Ensure test case relates to Jira requirements"""
    
    issues = []
    
    # Rule 1: Test title must be relevant to issue
    if not is_relevant(test_case['title'], issue_data['acceptanceCriteria']):
        issues.append(f"Title '{test_case['title']}' may not relate to requirement")
    
    # Rule 2: Steps must be specific (not generic)
    for step in test_case['steps']:
        if is_too_generic(step):
            issues.append(f"Step is too generic: '{step}'")
    
    # Rule 3: Expected result must be measurable
    if not is_measurable(test_case['expectedResult']):
        issues.append(f"Expected result not measurable: '{test_case['expectedResult']}'")
    
    # Rule 4: Test should not reference unknown features
    unknown_terms = find_unknown_terms(test_case, issue_data)
    if unknown_terms:
        issues.append(f"Test references unknown features: {unknown_terms}")
    
    return issues

def is_relevant(title, acceptance_criteria):
    """Check if test title relates to acceptance criteria"""
    title_words = set(title.lower().split())
    criteria_words = set(' '.join(acceptance_criteria).lower().split())
    overlap = len(title_words & criteria_words) / len(title_words)
    return overlap > 0.3  # At least 30% overlap

def is_too_generic(step):
    """Detect overly generic steps"""
    generic_phrases = ['do something', 'check', 'verify', 'test', 'etc']
    return any(phrase in step.lower() for phrase in generic_phrases)

def is_measurable(expected_result):
    """Verify expected result is specific, not vague"""
    vague_words = ['should work', 'looks ok', 'seems fine', 'as expected']
    has_vague = any(word in expected_result.lower() for word in vague_words)
    return len(expected_result) > 10 and not has_vague

def find_unknown_terms(test_case, issue_data):
    """Find terms in test that don't appear in Jira data"""
    test_text = f"{test_case['title']} {' '.join(test_case['steps'])} {test_case['expectedResult']}"
    issue_text = f"{issue_data['title']} {issue_data['description']} {' '.join(issue_data.get('acceptanceCriteria', []))}"
    
    test_terms = set(test_text.lower().split())
    issue_terms = set(issue_text.lower().split())
    
    unknown = test_terms - issue_terms
    # Filter out common words
    common_words = {'a', 'an', 'the', 'is', 'are', 'should', 'will', 'can', 'and', 'or', 'to', 'from'}
    unknown = unknown - common_words
    
    return unknown if len(unknown) > 2 else []
```

### Step 2: Check Coverage
Verify that test cases cover all acceptance criteria:

```python
def check_coverage(test_cases, acceptance_criteria):
    """Ensure test cases cover all acceptance criteria"""
    
    coverage = {}
    for criterion in acceptance_criteria:
        covered = False
        for tc in test_cases:
            if is_criterion_covered(tc, criterion):
                covered = True
                coverage[criterion] = True
                break
        
        if not covered:
            coverage[criterion] = False
    
    missing = [c for c, covered in coverage.items() if not covered]
    return {
        'totalCriteria': len(acceptance_criteria),
        'coveredCriteria': sum(1 for c in coverage.values() if c),
        'coveragePercent': sum(1 for c in coverage.values() if c) / len(acceptance_criteria) * 100,
        'missingCoverage': missing
    }

def is_criterion_covered(test_case, criterion):
    """Check if test case covers acceptance criterion"""
    test_text = f"{test_case['title']} {' '.join(test_case['steps'])} {test_case['expectedResult']}"
    criterion_words = criterion.lower().split()
    
    test_lower = test_text.lower()
    return all(word in test_lower for word in criterion_words if len(word) > 3)
```

### Step 3: Check for Duplicates
Remove duplicate test cases:

```python
def remove_duplicates(test_cases):
    """Remove duplicate or nearly-identical test cases"""
    
    unique = []
    seen_titles = set()
    
    for tc in test_cases:
        normalized_title = tc['title'].lower().strip()
        
        # Check for exact duplicate
        if normalized_title in seen_titles:
            continue
        
        # Check for semantic similarity
        similar_found = False
        for existing in unique:
            similarity = calculate_similarity(tc['title'], existing['title'])
            if similarity > 0.85:  # >85% similar
                similar_found = True
                break
        
        if not similar_found:
            unique.append(tc)
            seen_titles.add(normalized_title)
    
    return unique

def calculate_similarity(str1, str2):
    """Calculate string similarity using Levenshtein distance"""
    # Implementation: use difflib.SequenceMatcher
    from difflib import SequenceMatcher
    return SequenceMatcher(None, str1, str2).ratio()
```

### Step 4: Validate Priority Distribution
Ensure appropriate priority levels:

```python
def validate_priority_distribution(test_cases):
    """Check that priority distribution is reasonable"""
    
    by_priority = {
        'High': len([tc for tc in test_cases if tc.get('priority') == 'High']),
        'Medium': len([tc for tc in test_cases if tc.get('priority') == 'Medium']),
        'Low': len([tc for tc in test_cases if tc.get('priority') == 'Low'])
    }
    
    total = sum(by_priority.values())
    
    # Rule: At least 50% should be High or Medium
    critical = by_priority['High'] + by_priority['Medium']
    if critical / total < 0.5:
        warnings = ["Distribution skewed: too many Low priority tests"]
    else:
        warnings = []
    
    return {
        'distribution': by_priority,
        'percentageByPriority': {
            k: v / total * 100 for k, v in by_priority.items()
        },
        'warnings': warnings
    }
```

### Step 5: Generate JSON Output
Create properly formatted JSON output:

```python
def generate_json_output(issue_data, test_cases_by_category, validation_results):
    """Generate final JSON output"""
    
    output = {
        'metadata': {
            'project': issue_data['issueKey'].split('-')[0],
            'issueKey': issue_data['issueKey'],
            'issueTitle': issue_data['title'],
            'issueType': issue_data['type'],
            'priority': issue_data.get('priority'),
            'generatedAt': datetime.now().isoformat() + 'Z',
            'llmProvider': 'groq',
            'llmModel': 'qwen/qwen3.8-27b',
            'validationStatus': 'PASSED' if not validation_results['errors'] else 'WARNINGS'
        },
        'testPlan': {
            'objective': generate_objective(issue_data),
            'scope': generate_scope(issue_data),
            'preconditions': generate_preconditions(issue_data),
            'assumptions': generate_assumptions(issue_data),
            'environment': 'QA/Staging',
            'testCases': flatten_test_cases(test_cases_by_category)
        },
        'coverage': validation_results['coverage'],
        'priorityDistribution': validation_results['priorityDistribution'],
        'validationWarnings': validation_results['warnings'],
        'dataQualityFlags': issue_data.get('dataQualityFlags', [])
    }
    
    return output
```

### Step 6: Generate Markdown Output
Create human-readable Markdown format:

```markdown
# Test Plan: {issueTitle}

**Issue:** {issueKey}  
**Type:** {issueType}  
**Priority:** {priority}  
**Generated:** {timestamp}  
**LLM Model:** qwen/qwen3.8-27b  

## Objective
{generated_objective}

## Scope
{generated_scope}

## Preconditions
- {precondition_1}
- {precondition_2}

## Test Cases

### Happy Path (Positive Scenarios)
{happy_path_test_cases}

### Negative Scenarios (Error Handling)
{negative_test_cases}

### Edge Cases
{edge_case_test_cases}

### Regression Tests
{regression_test_cases}

## Test Case Coverage
- Total Acceptance Criteria: {total_criteria}
- Covered: {covered_criteria} ({coverage_percent}%)
- Missing Coverage: {missing_criteria}

## Priority Distribution
- High: {high_count} ({high_percent}%)
- Medium: {medium_count} ({medium_percent}%)
- Low: {low_count} ({low_percent}%)

## Quality Notes
{validation_warnings}
{data_quality_flags}
```

### Step 7: Save Outputs
Store in appropriate formats:

```python
def save_outputs(issue_key, json_output, markdown_output):
    """Save outputs to files"""
    
    os.makedirs('.tmp', exist_ok=True)
    
    # Save JSON
    json_file = f'.tmp/{issue_key}_test_plan.json'
    with open(json_file, 'w') as f:
        json.dump(json_output, f, indent=2)
    
    # Save Markdown
    md_file = f'.tmp/{issue_key}_test_plan.md'
    with open(md_file, 'w') as f:
        f.write(markdown_output)
    
    print(f"✓ Test plan saved to:")
    print(f"  - JSON: {json_file}")
    print(f"  - Markdown: {md_file}")
```

### Step 8: Log & Report Results
Generate a validation report:

```python
def generate_validation_report(issue_key, validation_results):
    """Create detailed validation report"""
    
    report = f"""
VALIDATION REPORT: {issue_key}
{'='*60}

Test Case Validation:
  Total Test Cases: {validation_results['totalTestCases']}
  Valid: {validation_results['validTestCases']}
  Issues Found: {len(validation_results['errors'])}

Coverage Analysis:
  Total Criteria: {validation_results['coverage']['totalCriteria']}
  Covered: {validation_results['coverage']['coveredCriteria']}
  Coverage: {validation_results['coverage']['coveragePercent']:.1f}%
  Missing: {validation_results['coverage']['missingCoverage']}

Priority Distribution:
  High: {validation_results['priorityDistribution']['distribution']['High']}
  Medium: {validation_results['priorityDistribution']['distribution']['Medium']}
  Low: {validation_results['priorityDistribution']['distribution']['Low']}

Warnings:
  {validation_results['warnings']}

{'='*60}
Status: {'PASS' if not validation_results['errors'] else 'FAIL WITH WARNINGS'}
"""
    
    return report
```

## Validation Checklist
- [ ] All test cases are traceable to requirements
- [ ] No duplicate or near-duplicate test cases
- [ ] Coverage is adequate (>75% of criteria)
- [ ] Priority distribution is reasonable (>50% High/Medium)
- [ ] All required fields present in each test case
- [ ] Steps are specific and actionable
- [ ] Expected results are measurable
- [ ] No hallucinated requirements
- [ ] Formal, professional tone
- [ ] Ready for QA team consumption

## Error Handling
| Error | Handling |
|-------|----------|
| Low coverage (<50%) | Log warning but proceed (QA may add manual tests) |
| Duplicate test cases | Automatically remove duplicates |
| Invalid priority | Default to 'Medium' |
| Missing expected result | Log error, flag for manual review |
| Hallucinated features | Flag for manual verification |

## Implementation Notes
- Use Python's `json` module for output
- Use string templates for Markdown generation
- Implement regex-based validation
- Log all validation results for audit trail
- Return BOTH JSON and Markdown

## Testing Checklist (Phase 3)
- [ ] Validate traceable test cases
- [ ] Detect non-relevant test cases
- [ ] Check acceptance criteria coverage
- [ ] Identify duplicates
- [ ] Validate priority distribution
- [ ] Generate valid JSON output
- [ ] Generate readable Markdown output
- [ ] Save files correctly
- [ ] Generate validation report
- [ ] Handle all error cases

---

**SOP Status:** Ready for Phase 3 Implementation  
**Tool:** tools/validator.py (new)  
**Next:** Phase 3 - Architect (Layer 2 Navigation & Layer 3 Implementation)
