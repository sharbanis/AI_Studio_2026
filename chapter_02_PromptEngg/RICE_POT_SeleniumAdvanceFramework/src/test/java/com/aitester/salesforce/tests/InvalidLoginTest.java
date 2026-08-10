package com.aitester.salesforce.tests;

import java.time.Duration;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

import com.aitester.salesforce.pages.LoginPage;

import io.github.bonigarcia.wdm.WebDriverManager;

public class InvalidLoginTest {
    private WebDriver driver;
    private LoginPage loginPage;

    @BeforeTest
    public void setUp() {
        try {
            WebDriverManager.chromedriver().setup();
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--headless=new");
            options.addArguments("--window-size=1920,1080");
            this.driver = new ChromeDriver(options);
            this.driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
            this.loginPage = new LoginPage(driver);
            this.loginPage.open(getBaseUrl());
        } catch (RuntimeException e) {
            throw new RuntimeException("Invalid login setup failed.", e);
        }
    }

    @Test
    public void invalidLogin() {
        try {
            String username = System.getProperty("salesforce.invalidUsername", System.getenv("SALESFORCE_INVALID_USERNAME"));
            String password = System.getProperty("salesforce.invalidPassword", System.getenv("SALESFORCE_INVALID_PASSWORD"));

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

    @AfterTest
    public void tearDown() {
        try {
            if (driver != null) {
                driver.quit();
            }
        } catch (RuntimeException e) {
            throw new RuntimeException("Invalid login teardown failed.", e);
        }
    }

    private String getBaseUrl() {
        return System.getProperty("salesforce.url", "https://login.salesforce.com/?locale=in");
    }
}
