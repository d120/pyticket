import unittest
from selenium import webdriver
from pyvirtualdisplay import Display
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class BasicSelenium(StaticLiveServerTestCase):
    fixtures = ["user-data.json"]

    def setUp(self):
        # make virtualdisplay invisible
        # display = Display(visible=0, size=(800, 600))
        # display.start()
        self.driver = webdriver.Firefox()
        super().setUp()

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    # login test
    def login(self):
        self.driver.get(self.live_server_url + "/accounts/login/")
        self.driver.find_element_by_id("id_username").send_keys("test_user2")
        self.driver.find_element_by_id("id_password").send_keys("Coollol888")
        self.driver.find_element_by_class_name("btn-primary").click()
        self.assertIn(self.live_server_url, self.driver.current_url)


# test create group
class TestUserGroup(BasicSelenium):

    def test_create_user_group(self):
        self.login()
        # create new group
        self.driver.get(self.live_server_url + "/group/new_group/")
        self.driver.find_element_by_id("id_name").send_keys("Test Group")
        # select group members
        select = self.driver.find_element_by_id("id_members")
        for opt in select.find_elements_by_tag_name("option"):
            if opt.text == "1":
                opt.click()
        self.driver.find_element_by_xpath('//form/button[@type="submit"]').click()
        success_alert = self.driver.find_element_by_xpath('//div[@role="alert"]')
        self.assertIn(
            "Gruppe Test Group wurde erfolgreich erstellt!", success_alert.text
        )
