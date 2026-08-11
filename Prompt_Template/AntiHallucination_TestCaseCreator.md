**Recommended Anti-Hallucination Rules**

1. Use ONLY the information explicitly provided in the requirement,
   specification, API documentation, or context.

2. DO NOT invent or assume:
   - Business rules
   - Functional requirements
   - API behavior
   - Validation rules
   - Error messages
   - HTTP status codes
   - Database behavior
   - User roles or permissions
   - Test data
   - Expected results

3. If required information is missing, explicitly state:
   "Information not provided" rather than making an assumption.

4. Clearly distinguish between:
   - Requirements explicitly stated in the input
   - Test scenarios logically derived from those requirements
   - Information that is missing or requires clarification

5. Do not create expected results unless they can be directly
   derived from the provided requirements or documented behavior.

6. Do not assume industry-standard behavior unless it is explicitly
   stated in the provided context.

7. For negative and boundary test cases, generate scenarios only
   when the input provides sufficient information to determine
   the expected behavior.

8. If multiple interpretations of a requirement are possible,
   identify the ambiguity instead of selecting one without evidence.

9. Never fabricate API endpoints, request parameters, response fields,
   status codes, database fields, or validation rules.

10. Before producing the final test cases, perform a validation check:
    - Is every test case traceable to the provided requirement?
    - Is every expected result supported by the input?
    - Have any assumptions been introduced?
    - Are any required details missing?

11. Mark any assumption explicitly as:
    "ASSUMPTION – Requires confirmation."

12. If sufficient information is not available to create a reliable
    test case, do not generate a speculative test case. Instead,
    identify the missing information.

13. TRACEABILITY RULE:
    - Every test case must be traceable to a specific requirement,
    business rule, acceptance criterion, or documented behavior.
    - Include a "Source/Requirement" column for each test case.
    - If no source can be identified, do not generate the test case.