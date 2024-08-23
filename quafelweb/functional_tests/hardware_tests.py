import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse


class TestHardwareManagement:

    def setup(self, live_server):
        self.driver = webdriver.Chrome()

        self.driver.get(live_server.url + reverse("login"))


        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("password")
        self.driver.find_element(By.NAME, "login").click()

        yield
        self.driver.quit()

    def test_add_hardware_profile(self, live_server):
        self.driver.get(live_server.url + reverse("add_account"))


        self.driver.find_element(By.NAME, "name").send_keys("New Hardware")
        self.driver.find_element(By.NAME, "description").send_keys("Test Description")
        self.driver.find_element(By.NAME, "connection").send_keys("http://127.0.0.1:8000")
        self.driver.find_element(By.NAME, "submit").click()


        self.driver.get(live_server.url + reverse("hardware"))
        profiles = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'New Hardware')]")
        assert len(profiles) > 0

    def test_configure_hardware_profile(self, live_server):
        self.driver.get(live_server.url + reverse("hardware"))

        self.driver.find_element(By.LINK_TEXT, "New Hardware").click()

        self.driver.find_element(By.NAME, "name").clear()
        self.driver.find_element(By.NAME, "name").send_keys("Updated Hardware")
        self.driver.find_element(By.NAME, "description").clear()
        self.driver.find_element(By.NAME, "description").send_keys("Updated Description")
        self.driver.find_element(By.NAME, "submit").click()

        self.driver.get(live_server.url + reverse("hardware"))
        profiles = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Updated Hardware')]")
        assert len(profiles) > 0

    def test_delete_hardware_profile(self, live_server):
        self.driver.get(live_server.url + reverse("hardware"))

        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Updated Hardware')]").click()
        self.driver.find_element(By.NAME, "delete").click()

        self.driver.get(live_server.url + reverse("hardware"))
        profiles = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Updated Hardware')]")
        assert len(profiles) == 0

    def test_invalid_connection_format(self, live_server):
        self.driver.get(live_server.url + reverse("add_account"))

        self.driver.find_element(By.NAME, "name").send_keys("Invalid Hardware")
        self.driver.find_element(By.NAME, "description").send_keys("Invalid Connection")
        self.driver.find_element(By.NAME, "connection").send_keys("invalid-connection-string")
        self.driver.find_element(By.NAME, "submit").click()

        error_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Invalid Request')]")
        assert error_message is not None