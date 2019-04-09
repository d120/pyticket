# import unittest
# from user_group.tests.test_views_selenium import BasicSelenium
#
#
#Testclass for create Ticket
# class TestTicket(BasicSelenium):
#
#    def test_create_ticket(self):
#
#        self.login()
#
#        self.driver.get("http://127.0.0.1:8000/new")
#        self.driver.find_element_by_id('id_name').send_keys("Test ticket")
#        self.driver.find_element_by_id('id_text').send_keys("Test ticket text")
#
#        self.driver.find_element_by_xpath('//*[@id="content_body"]/div/form/button').click()
#        self.assertIn("http://127.0.0.1:8000", self.driver.current_url)
#
#
# if __name__ == '__main__':
#    unittest.main()
