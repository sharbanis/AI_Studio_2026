# 🏗️ Phase 3 & 4: Architect & Stylize - Implementation Plan

**Status:** Ready for Development (2026-09-02)  
**Phase 3 Time Estimate:** 2-3 hours  
**Phase 4 Time Estimate:** 1-2 hours  
**Total Remaining:** 3-5 hours

---

## Phase 3: Architect (The 3-Layer Build)

### Overview
Phase 3 implements the actual working system using the 3-layer architecture specified in BLAST protocol:
- **Layer 1:** Architecture SOPs (✅ COMPLETE - see `architecture/` folder)
- **Layer 2:** Navigation (Decision Making & Orchestration)
- **Layer 3:** Tools (Deterministic Python Scripts)

### Layer 1: Architecture SOPs (✅ COMPLETED)
All SOPs are documented and ready to guide implementation:
- ✅ `01_jira_fetch_sop.md` - How to fetch issue data
- ✅ `02_normalization_sop.md` - How to normalize data
- ✅ `03_test_generation_sop.md` - How to generate test cases
- ✅ `04_validation_output_sop.md` - How to validate and format output

### Layer 2: Navigation (Decision Making) - TO BUILD

**File:** `navigation.py`

**Purpose:** Orchestrate Layer 1 & Layer 3 operations, route data, make decisions.

**Main Function Signature:**
```python
def generate_test_plan(issue_key: str) -> Dict:
    """
    Main orchestration function.
    Input: Jira issue key (e.g., "PROJ-123")
    Output: Complete test plan (JSON structure)
    """
    # Step 1: Initialize
    issue = jira_client.fetch_issue(issue_key)
    if not issue:
        return {'error': 'Issue not found'}
    
    # Step 2: Normalize
    normalized = normalizer.normalize_issue(issue)
    
    # Step 3: Check data quality
    if normalized['dataQuality']['hasMissingAcceptanceCriteria']:
        log_warning(f"{issue_key}: No acceptance criteria found")
    
    # Step 4: Generate test cases for each category
    test_cases = {}
    for category in ['happy_path', 'negative', 'edge_cases', 'regression']:
        test_cases[category] = generator.generate_test_cases(normalized, category)
    
    # Step 5: Validate
    validation_results = validator.validate_all(normalized, test_cases)
    
    # Step 6: Format and return
    output = formatter.format_output(normalized, test_cases, validation_results)
    
    return output
```

**Key Components:**
1. Error handling and retry logic
2. Quality gates and decision points
3. Logging and audit trails
4. Fallback mechanisms

**Implementation Checklist:**
- [ ] Create `navigation.py`
- [ ] Import all Layer 3 tools
- [ ] Implement main `generate_test_plan()` function
- [ ] Implement error handling
- [ ] Implement logging
- [ ] Add quality gates
- [ ] Test orchestration flow

### Layer 3: Tools (Deterministic Scripts) - TO BUILD

#### Tool 1: Data Normalizer
**File:** `tools/normalizer.py`

**Purpose:** Convert raw Jira data to internal schema (per `02_normalization_sop.md`)

**Key Functions:**
```python
def normalize_issue(raw_issue: Dict) -> Dict
def extract_acceptance_criteria(description: str) -> List[str]
def normalize_dates(date_string: str) -> str
def detect_ambiguous_language(text: str) -> bool
```

**Deliverables:**
- [ ] Parse raw Jira JSON
- [ ] Extract all required fields
- [ ] Normalize data types
- [ ] Quality assessment
- [ ] Return normalized schema

#### Tool 2: Test Case Generator
**File:** `tools/test_generator.py`

**Purpose:** Use Groq LLM to generate test cases (per `03_test_generation_sop.md`)

**Key Functions:**
```python
def generate_test_cases(issue: Dict, category: str) -> List[Dict]
def build_prompt(issue: Dict, category: str) -> str
def parse_test_cases(llm_response: str, category: str) -> List[Dict]
def validate_test_case(tc: Dict) -> List[str]
```

**Deliverables:**
- [ ] Build category-specific prompts
- [ ] Call Groq API
- [ ] Parse LLM output
- [ ] Validate structure
- [ ] Return test cases

#### Tool 3: Validator
**File:** `tools/validator.py`

**Purpose:** Quality assurance & output formatting (per `04_validation_output_sop.md`)

**Key Functions:**
```python
def validate_all(issue: Dict, test_cases: Dict) -> Dict
def check_traceability(test_case: Dict, issue: Dict) -> List[str]
def check_coverage(test_cases: List, criteria: List) -> Dict
def remove_duplicates(test_cases: List) -> List
def generate_json_output(issue: Dict, test_cases: Dict, validation: Dict) -> Dict
def generate_markdown_output(issue: Dict, test_cases: Dict, validation: Dict) -> str
```

**Deliverables:**
- [ ] Validate test case traceability
- [ ] Check acceptance criteria coverage
- [ ] Remove duplicates
- [ ] Format JSON output
- [ ] Format Markdown output
- [ ] Return validation results

#### Tool 4: Output Formatter
**File:** `tools/formatter.py`

**Purpose:** Package test plan for delivery

**Key Functions:**
```python
def format_output(issue: Dict, test_cases: Dict, validation: Dict) -> Dict
def format_markdown(issue: Dict, test_cases: Dict) -> str
def save_outputs(issue_key: str, json_data: Dict, markdown_data: str)
```

**Deliverables:**
- [ ] Combine all data
- [ ] Add metadata
- [ ] Generate JSON
- [ ] Generate Markdown
- [ ] Save to files

### Phase 3 Deliverables

**After Phase 3 completion, you will have:**

```
Test-Plan-Agent-BLAST/
├── tools/
│   ├── jira_client.py              ✅ Phase 2
│   ├── groq_client.py              ✅ Phase 2
│   ├── normalizer.py               ← Phase 3
│   ├── test_generator.py           ← Phase 3
│   ├── validator.py                ← Phase 3
│   └── formatter.py                ← Phase 3
├── navigation.py                   ← Phase 3 (orchestration)
├── architecture/
│   ├── 01_jira_fetch_sop.md        ✅ Phase 3
│   ├── 02_normalization_sop.md     ✅ Phase 3
│   ├── 03_test_generation_sop.md   ✅ Phase 3
│   └── 04_validation_output_sop.md ✅ Phase 3
└── ...
```

**Phase 3 Success Criteria:**
- [x] Layer 1 SOPs documented
- [ ] Layer 2 Navigation (orchestration.py) complete
- [ ] Layer 3 Tools (normalizer, generator, validator, formatter) complete
- [ ] All components integrated
- [ ] Full workflow tested

---

## Phase 4: Stylize (Refinement & UI)

### Overview
Phase 4 creates the web interface and refines output for professional delivery.

### Deliverable 1: Web UI (Flask Application)
**File:** `app.py`

**Features:**
```python
@app.route('/', methods=['GET'])
def home():
    """Landing page with form to enter Jira issue ID"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Endpoint to generate test plan.
    Input: JSON with issueKey
    Output: Test plan JSON + link to download Markdown
    """
    issue_key = request.json.get('issueKey')
    result = navigation.generate_test_plan(issue_key)
    return jsonify(result)

@app.route('/download/<issue_key>', methods=['GET'])
def download(issue_key):
    """Download generated Markdown file"""
    return send_file(f'.tmp/{issue_key}_test_plan.md')
```

**Deliverables:**
- [ ] Create Flask app structure
- [ ] Implement input form
- [ ] Implement generation endpoint
- [ ] Add download functionality
- [ ] Error handling

### Deliverable 2: HTML/CSS Frontend
**File:** `templates/index.html` and `static/style.css`

**Features:**
- Clean, professional UI
- Input form for Jira issue ID
- Display results (JSON + preview)
- Download buttons
- Error messages
- Loading indicator

**Design:**
```html
<div class="container">
  <h1>Jira Test Plan Generator</h1>
  
  <form id="generatorForm">
    <input type="text" placeholder="Enter Jira Issue ID (e.g., PROJ-123)" />
    <button type="submit">Generate Test Plan</button>
  </form>
  
  <div id="results" style="display:none;">
    <div id="jsonOutput"></div>
    <button id="downloadMarkdown">Download as Markdown</button>
    <button id="copyJson">Copy JSON</button>
  </div>
  
  <div id="errors" style="display:none;"></div>
</div>
```

**Deliverables:**
- [ ] Create form template
- [ ] Add result display
- [ ] Add download/copy buttons
- [ ] Add loading state
- [ ] Professional styling

### Deliverable 3: Output Formatting
**Markdown Example:**
```markdown
# Test Plan: User Login Validation

**Issue:** PROJ-123
**Generated:** 2026-09-02 15:30 UTC
**Model:** qwen/qwen3.8-27b

## Objective
Verify that the login form correctly validates user credentials and rejects invalid input.

## Test Cases

### Happy Path
**TC-001:** Valid credentials grant access
- Steps:
  1. Navigate to login page
  2. Enter valid email
  3. Enter correct password
  4. Click login
- Expected: User is logged in

### Negative Scenarios
**TC-002:** Invalid password shows error
- Steps:
  1. Navigate to login page
  2. Enter valid email
  3. Enter wrong password
  4. Click login
- Expected: Error message displayed
```

**Deliverables:**
- [ ] Template for Markdown generation
- [ ] Professional formatting
- [ ] Clear organization
- [ ] Printable layout

### Deliverable 4: End-to-End Flow
**Complete Workflow:**
1. User enters Jira issue ID in web form
2. Frontend sends POST to `/generate` endpoint
3. Navigation orchestrates: Fetch → Normalize → Generate → Validate → Format
4. Return test plan (JSON + Markdown)
5. Display in UI + offer download

**Deliverables:**
- [ ] Test complete flow
- [ ] Verify all components work together
- [ ] Error handling
- [ ] Performance optimization

### Phase 4 Deliverables

**After Phase 4 completion, you will have:**

```
Test-Plan-Agent-BLAST/
├── app.py                          ← Phase 4 (Flask app)
├── templates/
│   └── index.html                  ← Phase 4 (UI template)
├── static/
│   ├── style.css                   ← Phase 4 (styling)
│   └── script.js                   ← Phase 4 (frontend logic)
└── requirements.txt (updated)
```

**Running the Web App:**
```bash
pip install -r requirements.txt
python app.py
# Open browser: http://localhost:5000
```

**Phase 4 Success Criteria:**
- [ ] Web interface loads
- [ ] Form accepts Jira issue ID
- [ ] Generation works end-to-end
- [ ] Results display correctly
- [ ] Download works
- [ ] Error messages are clear
- [ ] Ready for user acceptance testing

---

## Complete Implementation Roadmap

```
Phase 1: Blueprint ✅ COMPLETE
├─ Discovery questions answered
├─ Data schemas defined
├─ Technology stack confirmed
└─ Project constitution documented

Phase 2: Link ✅ COMPLETE
├─ Jira API connection verified
├─ Groq LLM connection verified
├─ Credentials configured
└─ Tools ready for integration

Phase 3: Architect (2-3 hours)
├─ Layer 1: SOPs documented ✅
├─ Layer 2: Navigation built ← NEXT
├─ Layer 3: Tools implemented
└─ Full pipeline tested

Phase 4: Stylize (1-2 hours)
├─ Web UI created
├─ Output formatting
├─ End-to-end testing
└─ Ready for deployment

Total Time: ~5-7 hours from start
Remaining Time: ~3-5 hours to completion
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 4: Web UI (Stylize)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Flask App (app.py) + HTML/CSS/JS + Result Display   │  │
│  └────────────────────────┬─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│          Phase 3: Layer 2 (Navigation / Orchestration)      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ navigation.py: generate_test_plan() orchestration   │  │
│  │ - Coordinates Fetch → Normalize → Generate → Validate│  │
│  │ - Error handling & quality gates                    │  │
│  └────────────────────────┬─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────────┐  ┌─────▼──────────┐
│  Layer 3:    │  │  Layer 3:       │  │  Layer 3:      │
│ jira_client  │  │ normalizer.py   │  │ test_generator │
│     ✅       │  │   (new)         │  │     (new)      │
└──────────────┘  └─────────────────┘  └────────────────┘
       │                  │                   │
       │                  └───────────────────┘
       │                         │
       └─────────────────────────┼──────────────┐
                                │              │
                        ┌───────▼────────┐  ┌─▼──────────┐
                        │  validator.py  │  │formatter.py│
                        │    (new)       │  │  (new)     │
                        └────────────────┘  └────────────┘
                                │              │
                                └──────────────┘
                                        │
                                ┌───────▼────────┐
                                │ JSON + Markdown│
                                │    Output      │
                                └────────────────┘
```

---

## Success Criteria for All Phases

### Phase 1: Blueprint ✅
- [x] All discovery questions answered
- [x] Technology stack confirmed
- [x] Data schemas defined
- [x] Architecture documented

### Phase 2: Link ✅
- [x] Jira API working
- [x] Groq LLM working
- [x] Credentials secured
- [x] No connection issues

### Phase 3: Architect
- [ ] Layer 2 Navigation complete
- [ ] Layer 3 Tools complete
- [ ] All components integrated
- [ ] Full pipeline tested

### Phase 4: Stylize
- [ ] Web UI functional
- [ ] Output professionally formatted
- [ ] End-to-end working
- [ ] Ready for production use

---

## Next Steps

1. **Implement Layer 2 Navigation** (navigation.py)
2. **Implement Layer 3 Tools** (normalizer, generator, validator, formatter)
3. **Test integration** with real Jira issue
4. **Build web UI** (Flask + HTML/CSS/JS)
5. **End-to-end testing**
6. **Production deployment**

---

**Document Created:** 2026-09-02  
**Next Phase:** Phase 3 - Layer 2 & 3 Implementation
