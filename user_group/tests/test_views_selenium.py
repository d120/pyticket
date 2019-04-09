# """
# Selenium install tutorial:
# https://christopher.su/2015/selenium-chromedriver-ubuntu/
# """
#
# import unittest
# from selenium import webdriver
# from pyvirtualdisplay import Display
#
#
# class BasicSelenium(unittest.TestCase):
#     def setUp(self):
#
#make virtualdisplay invisible
#         display = Display(visible=0, size=(800, 600))
#         display.start()
#         self.driver = webdriver.Chrome()
#
#login test
#     def login(self):
#         self.driver.get('http://127.0.0.1:8000/accounts/login/')
#         self.driver.find_element_by_id('id_username').send_keys("test_user2")
#         self.driver.find_element_by_id('id_password').send_keys("Coollol888")
#         self.driver.find_element_by_class_name("btn-primary").click()
#         self.assertIn("http://127.0.0.1:8080/", self.driver.current_url)
#
#     def tearDown(self):
#         self.driver.quit
#
#test create group
# class TestUserGroup(BasicSelenium):
#
#     def test_create_user_group(self):
#
#         self.login()
#
#create new group
#         self.driver.get("http://127.0.0.1:8000/group/new/")
#         self.driver.find_element_by_id('id_name').send_keys("Test Group")
#
#select group members
#         select = self.driver.find_element_by_id('id_members')
#         for opt in select.find_elements_by_tag_name('option'):
#             if opt.text == '1':
#                 opt.click()
#
#         self.driver.find_element_by_xpath('//*[@id="content_body"]/div/form/button').click()
#         self.assertIn("http://127.0.0.1:8000/group/", self.driver.current_url)
#
#
# if __name__ == '__main__':
#     unittest.main()
