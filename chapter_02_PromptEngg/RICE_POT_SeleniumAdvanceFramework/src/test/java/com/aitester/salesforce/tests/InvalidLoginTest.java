package com.aitester.salesforce.tests;

import org.openqa.selenium.WebDriverException;
import org.testng.Assert;
import org.testng.annotations.Test;

import com.aitester.salesforce.base.BaseTest;
import com.aitester.salesforce.utils.ConfigReader;

public class InvalidLoginTest extends BaseTest {
    @Test
    public void invalidLogin() {
        try {
            String username = ConfigReader.getInvalidUsername();
            String password = ConfigReader.getInvalidPassword();

            if (username == null) {
                username = "invalid.user@example.com";
            }
            if (password == null) {
                password = "WrongPassword123!";
            }

            loginPage.login(username, password);
            Assert.assertTrue(loginPage.isErrorDisplayed(), "Invalid login error message should be displayed.");
        } catch (AssertionError | WebDriverException e) {
            throw new RuntimeException("Invalid login test failed.", e);
        }
    }
}
