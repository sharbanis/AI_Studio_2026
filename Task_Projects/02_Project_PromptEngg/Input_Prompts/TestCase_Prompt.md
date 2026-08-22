# VWO Login Module Test Case Prompt

**R - Role:**

Act as an expert Senior Test Engineer with extensive experience in structural test design, boundary value analysis, and strict specification-based testing for enterprise B2B applications.

**I - Intent (Task & Scope):**

Your task is to write industry-level standard, highly rigorous test cases for the 5 core requirements of the VWO Login module. For each requirement, you must thoroughly design:

- **Positive Scenarios:** Valid paths confirming the system works as explicitly intended.
- **Negative Scenarios:** Invalid inputs, boundary violations, and edge cases to ensure the application handles failures robustly according to the rules provided.

**C - Context & Constraints:**

Base these test cases strictly on the VWO Login page (https://app.vwo.com/#/login) requirements provided in the Parameters (P) section.

- **Constraint 1:** Do not invent features, field constraints, or UI behaviors not explicitly written below.
- **Constraint 2:** If details like exact password character length, specific cookie names, or exact error text are missing from the parameters, do not guess or assume "typical" values. Mark those field inputs or expectations as "Information not provided in requirement".

**E - Expectations:**

The test cases must be immediately actionable and testable for execution teams. They must verify all functional bounds, security protocols, and session parameters accurately. Every single requirement must map directly to its corresponding test case(s).

**P - Parameters (Core Inputs):**

Design your test cases exclusively around these 5 explicit requirements as given in the VWO requirement doc.

**O - Output Format:**

Present the final test cases cleanly inside a Markdown table using exactly this industry-standard column layout:

| Test ID | Description | Pre-conditions | Steps | Expected Result | Priority |

Formatting of test cases to appear neatly in tabular format.

**T - Tolerance (Anti-Hallucination Guardrails):**

- **STRICT POLICY:** Zero tolerance for hallucinating system traits, default configurations, or typical frameworks.
- Do not assume default error messages (e.g., do not write "Invalid email or password text appears" unless it's explicitly in the parameter; write "Generic secure error message appears").
- If any technical detail necessary to execute a step is omitted from the specification, explicitly state "Information not provided" in that specific cell.
