import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.urls import reverse

class TestAccountManagement:

    def setup(self, live_server):
        self.driver = webdriver.Chrome()
        self.driver.get(live_server.url + reverse("login"))
        yield
        self.driver.quit()
    def tearDown(self):
        self.driver.close()

    def test_add_admin(self, live_server):
        self.driver.get(live_server.url + reverse("add_account"))
        self.driver.find_element(By.NAME, "admin_ident").send_keys("new_admin")
        self.driver.find_element(By.NAME, "submit").click()


        self.driver.get(live_server.url + reverse("account"))
        accounts = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'new_admin')]")
        assert len(accounts) > 0

    def test_remove_admin(self, live_server):
        self.driver.get(live_server.url + reverse("delete_account"))
        self.driver.find_element(By.NAME, "admin_ident").send_keys("new_admin")
        self.driver.find_element(By.NAME, "submit").click()


        self.driver.get(live_server.url + reverse("account"))
        accounts = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'new_admin')]")
        assert len(accounts) == 0
