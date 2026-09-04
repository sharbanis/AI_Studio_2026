# Layer 1: Test Case Generation SOP (Standard Operating Procedure)

**Layer:** 1 (Architecture/Technical SOPs)  
**Purpose:** Generate structured test cases from normalized Jira requirements using Groq LLM  
**Owner:** test_generator.py (to be built in Phase 3)  
**Status:** Ready for Phase 3 implementation

---

## Objective
Transform normalized issue requirements into structured, actionable test cases using Groq LLM, organized by test category (Happy Path, Negative, Edge Cases, Regression).

## Key Principle
**LLM is used for CONTENT GENERATION only**, not for business logic decisions. All test structure, categorization, and validation remains deterministic.

## Inputs
```json
{
  "issueKey": "PROJ-123",
  "title": "User login should validate credentials",
  "type": "Story",
  "description": "The login form validates user input...",
  "acceptanceCriteria": [
    "Invalid email format is rejected",
    "Incorrect password shows error message",
    "No session is created"
  ],
  "labels": ["auth", "login"],
  "components": ["Authentication"],
  "priority": "High",
  "testCaseCategories": ["happy_path", "negative", "edge_cases", "regression"]
}
```

## Process Flow

### Step 1: Validate Input Readiness
Before generating test cases, verify:
- [ ] acceptanceCriteria array has items (warn if empty, but don't stop)
- [ ] description is not empty
- [ ] testCaseCategories is specified
- [ ] LLM model is available

**Decision:** If critical data missing → Flag in output, provide best-effort output

### Step 2: Build Category-Specific Prompts
For each test category, create a tailored prompt to guide Groq LLM.

#### **Category 1: Happy Path (Positive Scenarios)**
Test that the feature works correctly when all inputs are valid.

**Prompt Template:**
```
You are a QA test case generation expert. Generate ONLY valid, professional test cases.

Issue: {title}
Description: {description}
Acceptance Criteria:
{criteria_list}

Generate 2-3 HAPPY PATH test cases (feature works correctly).

Output format (EXACTLY):
TC-001-HAPPY
Title: [test title]
Steps:
1. [step 1]
2. [step 2]
3. [step 3]
Expected Result: [result]
Priority: High

TC-002-HAPPY
...

Do NOT include negative scenarios, edge cases, or error handling here.
Do NOT make up requirements not in the description.
Keep test cases simple and actionable.
```

#### **Category 2: Negative Scenarios (Error Handling)**
Test that invalid inputs are rejected gracefully.

**Prompt Template:**
```
You are a QA test case generation expert. Generate ONLY valid, professional test cases.

Issue: {title}
Description: {description}

Generate 2-3 NEGATIVE test cases (invalid input, error handling).

Examples of negative scenarios:
- Invalid input format
- Missing required fields
- Boundary violations
- Rejected access

Output format (EXACTLY):
TC-001-NEGATIVE
Title: [test title]
Steps:
1. [step 1]
2. [step 2]
Expected Result: [error message or rejection shown]
Priority: High

TC-002-NEGATIVE
...

Focus on error handling, validation, and user feedback.
Do NOT test happy paths here.
Keep test cases simple and actionable.
```

#### **Category 3: Edge Cases (Boundary Conditions)**
Test boundary values and corner cases.

**Prompt Template:**
```
You are a QA test case generation expert. Generate ONLY valid, professional test cases.

Issue: {title}
Description: {description}

Generate 2-3 EDGE CASE test cases (boundary conditions, extreme values).

Examples of edge cases:
- Empty fields
- Very long input (max length)
- Special characters
- Boundary values
- Concurrent operations

Output format (EXACTLY):
TC-001-EDGE
Title: [test title]
Steps:
1. [step 1]
Expected Result: [result]
Priority: Medium

TC-002-EDGE
...

Focus on boundaries and corner cases.
Keep test cases simple and actionable.
```

#### **Category 4: Regression (Existing Functionality)**
Test that existing functionality still works.

**Prompt Template:**
```
You are a QA test case generation expert. Generate ONLY valid, professional test cases.

Issue: {title}
Description: {description}

Generate 2-3 REGRESSION test cases (verify existing functionality still works).

Regression tests verify that:
- Basic functionality works
- UI elements load correctly
- No errors are thrown
- Previous functionality is not broken

Output format (EXACTLY):
TC-001-REGRESSION
Title: [test title]
Steps:
1. [step 1]
2. [step 2]
Expected Result: [feature works as expected]
Priority: High

TC-002-REGRESSION
...

Focus on core functionality and UI health checks.
Keep test cases simple and actionable.
```

### Step 3: Call Groq LLM for Each Category
For each category in testCaseCategories:

1. **Build the prompt** using template above
2. **Call Groq API:**
   ```python
   response = groq_client.generate_test_cases(
       issue_data=normalized_issue,
       test_category=category_name
   )
   ```
3. **Capture output** with model name and timestamp
4. **Parse response** (see Step 4)
5. **Handle errors** (see Step 7)

**LLM Parameters:**
- Model: qwen/qwen3.8-27b (or current available)
- Temperature: 0.3 (low for deterministic output)
- Max tokens: 1000
- Top-p: 0.95
- Stop sequences: ["TC-00", "---"]

### Step 4: Parse LLM Output into Structured Format
Extract test cases from LLM response using regex patterns.

**Pattern to match:**
```regex
^TC-(\d+)-(\w+)\s*$
^Title:\s*(.+)$
^Steps:\s*$
^\d+\.\s*(.+)$
^Expected Result:\s*(.+)$
^Priority:\s*(High|Medium|Low)$
```

**Parsing logic:**
```python
def parse_test_cases(llm_response, category):
    """Parse LLM response into structured test cases"""
    test_cases = []
    
    # Split by TC-XXX markers
    parts = re.split(r'^TC-(\d+)', llm_response, flags=re.MULTILINE)
    
    for i in range(1, len(parts), 2):
        tc_num = parts[i]
        tc_text = parts[i+1]
        
        # Extract fields using regex
        title = extract_field(tc_text, r'Title:\s*(.+)')
        steps = extract_steps(tc_text)
        expected = extract_field(tc_text, r'Expected Result:\s*(.+)')
        priority = extract_field(tc_text, r'Priority:\s*(High|Medium|Low)')
        
        test_cases.append({
            'id': f'TC-{tc_num:03d}-{category.upper()}',
            'category': category,
            'title': title,
            'steps': steps,
            'expectedResult': expected,
            'priority': priority or 'Medium'
        })
    
    return test_cases
```

### Step 5: Validate Generated Test Cases
Quality checks on generated output:

```python
def validate_test_case(tc):
    """Verify test case meets quality standards"""
    issues = []
    
    # Check 1: All required fields present
    if not tc.get('title') or len(tc['title']) < 5:
        issues.append("Title is missing or too short")
    
    # Check 2: Steps are specific and actionable
    if not tc.get('steps') or len(tc['steps']) < 2:
        issues.append("Steps are missing or incomplete")
    
    for step in tc['steps']:
        if len(step) < 5:
            issues.append(f"Step is too vague: '{step}'")
    
    # Check 3: Expected result is clear
    if not tc.get('expectedResult') or len(tc['expectedResult']) < 5:
        issues.append("Expected result is missing or unclear")
    
    # Check 4: Priority is valid
    if tc.get('priority') not in ['High', 'Medium', 'Low']:
        issues.append(f"Invalid priority: {tc['priority']}")
    
    # Check 5: No hallucinated requirements
    if detect_hallucination(tc['title'], original_requirements):
        issues.append("Test case appears to reference unknown requirements")
    
    return issues
```

### Step 6: Organize Test Cases
Structure all generated test cases by category:

```json
{
  "happy_path": [
    {"id": "TC-001-HAPPY", "category": "happy_path", ...},
    {"id": "TC-002-HAPPY", "category": "happy_path", ...}
  ],
  "negative": [
    {"id": "TC-001-NEGATIVE", "category": "negative", ...},
    {"id": "TC-002-NEGATIVE", "category": "negative", ...}
  ],
  "edge_cases": [...],
  "regression": [...]
}
```

### Step 7: Error Handling & Fallback

| Error | Handling |
|-------|----------|
| Groq API unavailable | Use Ollama fallback (if configured) |
| LLM returns invalid format | Re-parse with lenient regex, flag issues |
| LLM returns hallucinated test | Validate against original data, remove if mismatch |
| LLM returns incomplete output | Use partial data, flag missing test cases |
| Model rate-limited | Implement exponential backoff, retry up to 3 times |

**Graceful Degradation:**
- If Groq fails → Try Ollama fallback
- If both fail → Return template test cases with warnings
- Always provide SOME output, never return None

### Step 8: Add Metadata & Delivery
```json
{
  "metadata": {
    "project": "PROJ",
    "issueKey": "PROJ-123",
    "generatedAt": "2026-09-02T15:30:00Z",
    "llmProvider": "groq",
    "llmModel": "qwen/qwen3.8-27b",
    "llmTemperature": 0.3,
    "dataQualityWarnings": [],
    "generationNotes": []
  },
  "testCases": {
    "happy_path": [...],
    "negative": [...],
    "edge_cases": [...],
    "regression": [...]
  },
  "statistics": {
    "totalTestCases": 8,
    "byCategory": {
      "happy_path": 2,
      "negative": 2,
      "edge_cases": 2,
      "regression": 2
    }
  }
}
```

## Quality Standards
All generated test cases must meet:
- ✓ Clear, formal English
- ✓ Actionable steps (not vague)
- ✓ Measurable expected results
- ✓ Traceable to Jira requirements
- ✓ Free of hallucinated features
- ✓ Appropriate priority level
- ✓ No ambiguous language

## Determinism & Reproducibility
- **Rule 1:** Same issue + same model always produces similar (not identical, LLM varies) test cases
- **Rule 2:** Test structure and categorization is deterministic
- **Rule 3:** All test cases are validated against source requirements
- **Rule 4:** Validation failures are logged and flagged

## Implementation Notes
- Use Groq SDK for API calls
- Implement regex-based parsing for reliability
- Cache test case templates for consistency
- Log all LLM calls (input/output) for audit
- Store intermediate outputs in `.tmp/` for debugging

## Testing Checklist (Phase 3)
- [ ] Generate Happy Path test cases correctly
- [ ] Generate Negative test cases correctly
- [ ] Generate Edge Case test cases correctly
- [ ] Generate Regression test cases correctly
- [ ] Parse LLM output into structured format
- [ ] Validate test cases for quality
- [ ] Handle missing or ambiguous requirements
- [ ] Handle LLM rate limiting
- [ ] Fall back to Ollama if Groq unavailable
- [ ] Verify test cases are not hallucinated

---

**SOP Status:** Ready for Phase 3 Implementation  
**Tool:** tools/test_generator.py (new)  
**Next SOP:** Validation & Output SOP
