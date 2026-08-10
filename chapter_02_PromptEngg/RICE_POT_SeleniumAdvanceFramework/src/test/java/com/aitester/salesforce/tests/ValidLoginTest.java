package com.aitester.salesforce.tests;

import org.openqa.selenium.WebDriverException;
import org.testng.Assert;
import org.testng.annotations.Test;

import com.aitester.salesforce.base.BaseTest;
import com.aitester.salesforce.utils.ConfigReader;

public class ValidLoginTest extends BaseTest {
    @Test
    public void validLogin() {
        try {
            String username = ConfigReader.getValidUsername();
            String password = ConfigReader.getValidPassword();

            Assert.assertNotNull(username, "Salesforce username is missing.");
            Assert.assertNotNull(password, "Salesforce password is missing.");

            loginPage.login(username, password);
            Assert.assertTrue(loginPage.isLoginSuccessful(), "Valid login should succeed.");
        } catch (AssertionError | WebDriverException e) {
            throw new RuntimeException("Valid login test failed.", e);
        }
    }
}
