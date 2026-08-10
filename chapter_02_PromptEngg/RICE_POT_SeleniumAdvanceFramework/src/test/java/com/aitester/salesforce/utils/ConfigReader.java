package com.aitester.salesforce.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigReader {
    private static final Properties PROPERTIES = loadProperties();

    private ConfigReader() {
    }

    public static String getBaseUrl() {
        return getProperty("base.url", "https://login.salesforce.com/?locale=in");
    }

    public static String getBrowser() {
        return getProperty("browser", "chrome");
    }

    public static String getValidUsername() {
        return getProperty("valid.username", System.getProperty("salesforce.username", System.getenv("SALESFORCE_USERNAME")));
    }

    public static String getValidPassword() {
        return getProperty("valid.password", System.getProperty("salesforce.password", System.getenv("SALESFORCE_PASSWORD")));
    }

    public static String getInvalidUsername() {
        return getProperty("invalid.username", System.getProperty("salesforce.invalidUsername", System.getenv("SALESFORCE_INVALID_USERNAME")));
    }

    public static String getInvalidPassword() {
        return getProperty("invalid.password", System.getProperty("salesforce.invalidPassword", System.getenv("SALESFORCE_INVALID_PASSWORD")));
    }

    private static Properties loadProperties() {
        Properties properties = new Properties();
        try (InputStream inputStream = ConfigReader.class.getClassLoader().getResourceAsStream("config.properties")) {
            if (inputStream != null) {
                properties.load(inputStream);
            }
        } catch (IOException e) {
            throw new RuntimeException("Unable to load config properties.", e);
        }
        return properties;
    }

    private static String getProperty(String key, String defaultValue) {
        String value = PROPERTIES.getProperty(key);
        if (value == null || value.trim().isEmpty()) {
            return defaultValue;
        }
        return value.trim();
    }
}
