**Framework**
*RICE POT Framework (95%, Plan, 5% Execution)*
ROLE: [Expertise]
Instructions: [Purpose]
CONTEXT: [Background info]
EXPECTED: [Success criteria]
PARAMETERS: [Constraints]
OUTPUT: [Format]
TONE: [Specific instruction]

**Task** 
Create Test cases using RICEPOT Framework Prompting

**Prompt**

Role : 
you are a senior QA manager with almost 10 years of experience in functional testing, security testing, and performance testing. 
CONTEXT : 
- Application : E Commerice website 
- https://www.bstackdemo.com/ 
- Login Method : Email , Password and Submit 
- Features : Remember me check, Forgot password link, create a free account. 
- Validation : Email must be valid, if not valid error message shown Task : Generate the exactly 10 Testcases covering 
- 3 positive scenarios ( successful login) 
- 5 negative scenarios ( validation errors) 
- 1 security scenarios, (sql injection, brute force) 
- 1 performance related scenario 
CONSTRAINTS 
- Use Only the feature mentioned above. 
- [DON'T] Assume password complexity 
- [DON'T] invent error messages 
- Mark any assumptions as "[ASSUMPTION]" 
- If information is missing, state "Not specified" 
OUTPUT FORMAT: TABLE VIEW 
| TC_ID | Category | Description | Pre-condition | Steps | Expected Result | Priority 
| Use TC_001, TC_002, etc. for IDs. Priority: High / Medium / Low
 
 **output**
 TC_ID	Category	Description	Pre-condition	Steps	Expected Result	Priority
TC_001	Positive	Verify successful login with valid email and valid password	User has a valid registered account on the application; user is on the login page	1. Navigate to https://www.bstackdemo.com/ 2. Click on the login option 3. Enter a valid email 4. Enter the valid password 5. Click Submit	User is successfully logged in and redirected to the authenticated page or account dashboard	High
TC_002	Positive	Verify successful login with Remember me checked	User has a valid registered account; user is on the login page	1. Navigate to login page 2. Enter valid email 3. Enter valid password 4. Select Remember me checkbox 5. Click Submit	User logs in successfully and the session remains available after browser restart or revisit if the application supports persistent login behavior; otherwise the checkbox is accepted without error	High
TC_003	Positive	Verify successful login with valid credentials after leaving fields empty initially	User has valid account; user is on the login page	1. Open login page 2. Enter valid email 3. Enter valid password 4. Click Submit	Login succeeds and user is redirected to the authenticated area	High
TC_004	Negative	Validate email field with invalid format	User is on the login page	1. Navigate to login page 2. Enter invalid email format such as abc or test@ 3. Enter a valid or any password 4. Click Submit	System displays a validation error for invalid email format; no login attempt is performed	High
TC_005	Negative	Validate email field as empty	User is on the login page	1. Open login page 2. Leave email field blank 3. Enter a valid password 4. Click Submit	System prevents login and shows validation for required email field; no navigation occurs	High
TC_006	Negative	Validate password field as empty	User is on the login page	1. Open login page 2. Enter valid email 3. Leave password blank 4. Click Submit	System prevents login and shows validation for required password field; no navigation occurs	High
TC_007	Negative	Validate both email and password blank	User is on the login page	1. Open login page 2. Leave email blank 3. Leave password blank 4. Click Submit	System prevents login and shows required field validation for both fields; no navigation occurs	High
TC_008	Negative	Validate login with incorrect password for valid email	User has a valid registered email; user is on the login page	1. Open login page 2. Enter valid registered email 3. Enter incorrect password 4. Click Submit	Login is rejected and the system displays an authentication failure message; user remains on login page	High
TC_009	Security	Verify login form is protected against SQL injection attempt in email/password fields	User is on the login page; application is accessible	1. Open login page 2. Enter a payload such as ' OR '1'='1 in the email field 3. Enter a payload such as ' OR '1'='1 in the password field 4. Click Submit	Application does not allow injection input to bypass login; it either rejects the request or displays a standard validation/authentication error; no system compromise or abnormal response	High
TC_010	Performance	Verify login response time under normal valid login flow	User has valid credentials; application is accessible	1. Navigate to login page 2. Enter valid email and password 3. Click Submit 4. Measure page load/response time	Login completes within acceptable user response time; no delay causing usability issues; page responds without timeout or severe lag	Medium
Notes:

[ASSUMPTION] The application supports browser session persistence when Remember me is checked; if this functionality is not supported, the expected result should be adjusted to “checkbox is accepted without error.”
[ASSUMPTION] The exact validation error text for invalid email and required field errors is not specified in the requirement; therefore, the expected result focuses on validation behavior rather than specific wording.
Not specified: exact password complexity rules, exact error messages, and whether forgot password or create free account links are fully functional beyond the login flow.

*[chatgpt.com/share/697efcef-7c50-8009-b5e6-db0a4fab6f82](https://chatgpt.com/share/697efcef-7c50-8009-b5e6-db0a4fab6f82)*