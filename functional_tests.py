# functional_tests.py
# by Sam Heyman

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SlackBotUserTest(unittest.TestCase):

    # user opens Slack in the browser
    def setUp(self):
        self.browser  = webdriver.Firefox()
        self.browser.get('https://sam-heyman.slack.com/messages/CCP3YDEDS/')
        self.assertIn('Slack', self.browser.title)


    # user logs in
    def test_can_login_and_use_slack(self):
        emailBox = self.browser.find_element_by_id('email')  
        passwordBox = self.browser.find_element_by_id('password')

        emailBox.send_keys('sam.heyman@gmail.com')
        emailBox.send_keys(Keys.ENTER)  
        passwordBox.send_keys('552>NR2018s')
        passwordBox.send_keys(Keys.ENTER)  

        time.sleep(10)  

        inputBox = self.browser.find_element_by_class_name('ql-editor')
        inputBox.click
        #textBox = inputBox.find_element_by_tag_name('p')
        inputBox.send_keys("Hello")
        inputBox.send_keys(Keys.ENTER)  

        time.sleep(2)  

        inputBox = self.browser.find_element_by_class_name('c-message_list__day_divider__label__pill')

    #     self.assertTrue(userNameBox = self.browser.find_element_by_id("email"))
    #     self.assertTrue(userPasswordBox = self.browser.find_element_by_id("email"))
    #     self.assertTrue(signIn = self.browser.find_element_by_id("signin_btn"))


    # def test_first_call(self):
    #     self.assertTrue(self.browser.find_element_by_xpath('//*[@id="email"]'))
    #     self.assertTrue(self.browser.find_element_by_xpath('//*[@id="password"]'))
    #     self.assertTrue(self.browser.find_element_by_xpath('//*[@id="signin_btn"]'))
    #     # self.assertIn('Sam\'s space Slack', self.browser.title)

    # user invites the bot to channel 

    # user orders a taxi now

    # user orders a taxi later

    # user cancels taxi

    # user asks for taxi status


    def tearDown(self):
        self.browser.quit()


# Run the tests
if __name__ == "__main__":
    unittest.main()