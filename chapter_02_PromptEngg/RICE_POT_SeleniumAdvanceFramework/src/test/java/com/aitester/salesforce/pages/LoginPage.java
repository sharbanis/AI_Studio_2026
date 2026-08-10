package com.aitester.salesforce.pages;

import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class LoginPage {
    private final WebDriver driver;
    private final WebDriverWait wait;

    @FindBy(xpath = "//input[@type='email']")
    private WebElement username;

    @FindBy(xpath = "//input[@type='password']")
    private WebElement password;

    @FindBy(xpath = "//input[@type='submit']")
    private WebElement loginButton;

    @FindBy(xpath = "//input[@type='checkbox']")
    private WebElement rememberMe;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        PageFactory.initElements(driver, this);
    }

    public void open(String url) {
        try {
            driver.get(url);
            wait.until(ExpectedConditions.visibilityOf(username));
        } catch (TimeoutException | RuntimeException e) {
            throw new RuntimeException("The Salesforce login page did not load correctly.", e);
        }
    }

    public void login(String user, String pass) {
        try {
            wait.until(ExpectedConditions.visibilityOf(username));
            username.clear();
            username.sendKeys(user);

            wait.until(ExpectedConditions.visibilityOf(password));
            password.clear();
            password.sendKeys(pass);

            wait.until(ExpectedConditions.elementToBeClickable(loginButton));
            loginButton.click();
        } catch (TimeoutException | RuntimeException e) {
            throw new RuntimeException("Failed to perform login action.", e);
        }
    }

    public void toggleRememberMe() {
        try {
            wait.until(ExpectedConditions.visibilityOf(rememberMe));
            if (!rememberMe.isSelected()) {
                rememberMe.click();
            }
        } catch (TimeoutException | RuntimeException e) {
            throw new RuntimeException("The Remember Me checkbox could not be interacted with.", e);
        }
    }

    public boolean isErrorDisplayed() {
        try {
            WebElement error = wait.until(ExpectedConditions.visibilityOfElementLocated(
                    By.xpath("//div[contains(.,'Please check your username and password.') or contains(.,'username and password') or contains(.,'error') or contains(.,'invalid')]")));
            return error.isDisplayed();
        } catch (TimeoutException | RuntimeException e) {
            return false;
        }
    }

    public boolean isLoginSuccessful() {
        try {
            return !driver.getCurrentUrl().contains("login.salesforce.com") && !driver.getCurrentUrl().contains("/login");
        } catch (RuntimeException e) {
            return false;
        }
    }
}
