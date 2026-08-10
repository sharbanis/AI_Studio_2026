Understanding
This prompt is asking for a strict, code-only Selenium + Java + Maven + TestNG framework for a Salesforce login page, built to enterprise automation standards.

The key interpretation is:

It is not a generic script; it is a production-style framework.
The target is the Salesforce login page with valid and invalid authentication flows.
The implementation must use:
Page Object Model
PageFactory
@FindBy
XPath-only locators
TestNG lifecycle methods like @BeforeTest, @AfterTest, @Test
It must avoid prohibited patterns:
no CSS selectors
no ID, name, or similar locator types
no Thread.sleep
no comments
no extra explanation text
The final output must be runnable code only, with:
1 page object file
2 test scripts
Maven project structure
Plan
1. Project setup
Create a Maven Java project with Selenium, TestNG, and ChromeDriver management.
Configure the build so tests can be executed with Maven.
Keep the project structure modular: pages, tests, base utility layer.
2. Base framework layer
Create the browser setup and teardown logic.
Initialize WebDriver with a stable browser configuration.
Add wait utilities using WebDriverWait and implicit waits.
Centralize reusable configuration like base URL and credentials.
3. Page Object Model
Build a LoginPage class with:
constructor initialization
@FindBy XPath locators
reusable methods for entering username, password, clicking login, and checking validation states
Add structured exception handling around page actions and navigation.
Keep the methods reusable and readable.
4. Test scripts
Script 1: valid login scenario

navigate to Salesforce login page
enter valid credentials
click login
verify successful landing or post-login state
Script 2: invalid login scenario

navigate to Salesforce login page
enter invalid credentials
click login
verify error message or failed auth state
5. Enterprise-grade quality checks
Ensure all locators are XPath only.
Ensure no Thread.sleep is used anywhere.
Ensure assertions validate real behavior.
Ensure exceptions are handled in both page object and test classes.
Use consistent naming, modular methods, and clean structure.
6. Verification
Run the Maven test suite.
Confirm both valid and invalid login tests execute successfully.
Check that there are no forbidden locators or anti-patterns.
Final output should be code only, with zero explanatory text.
Final interpretation
This prompt is effectively a “generate only the production-ready code” challenge. The main focus is not just automation, but disciplined enterprise-level Selenium design under strict constraints. The plan should therefore prioritize:

stable Page Object structure,
XPath-only selectors,
robust exception handling,
clean TestNG organization,
and strict compliance with the no-extra-output requirement.