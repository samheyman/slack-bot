# functional_tests.py
# by Sam Heyman

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import QAbifyConsierge

class SlackBotTest(unittest.TestCase):

    # open Slack in the browser
    def setUp(self):
        self.browser  = webdriver.Firefox()
        # logIn()

    # user can log in
    # def logIn(self):
    #     self.assertTrue(userNameBox = self.browser.find_element_by_id("email"))
    #     self.assertTrue(userPasswordBox = self.browser.find_element_by_id("email"))
    #     self.assertTrue(signIn = self.browser.find_element_by_id("signin_btn"))

    # user invites the bot to channel 

    # user asks for a taxi now

    # user orders a taxi


    # user cancels taxi


    def tearDown(self):
        self.browser.quit()

    def test_first_call(self):
        self.browser.get('https://sam-heyman.slack.com/messages/CCP3YDEDS/')
        self.assertIn('Slack', self.browser.title)
        self.assertTrue(self.browser.find_element_by_xpath('//*[@id="email"]'))
        self.assertTrue(self.browser.find_element_by_xpath('//*[@id="password"]'))
        self.assertTrue(self.browser.find_element_by_xpath('//*[@id="signin_btn"]'))
        # self.assertIn('Sam\'s space Slack', self.browser.title)

# Run the tests
if __name__ == "__main__":
    unittest.main()