# functional_tests.py
# by Sam Heyman
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from slackclient import SlackClient
from context import taxi_bot


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# user commands to test
BOT_COMMAND = [{
                'type': 'message', 
                'text': '', 
                'channel': 'CCP3YDEDS', 
}]

class SlackBotUserTest(unittest.TestCase):

    # user opens Slack in the browser
    slack_client.rtm_connect(with_team_state=False)
    print("QAbify Bot connected and running!")
    # Read bot's user ID by calling Web API method `auth.test`
    starterbot_id = slack_client.api_call("auth.test")["user_id"]

    def test_user_can_see_all_taxis(self):
        BOT_COMMAND[0]['text']='<@UCPF17NBX> all taxis'
        command, channel = taxi_bot.parse_bot_commands(BOT_COMMAND)
        answer = taxi_bot.handle_command(command, channel)
        self.assertIn("There are currently 4 taxis in the system.", answer)

    def test_user_can_see_all_taxis_in_city(self):
        BOT_COMMAND[0]['text']='<@UCPF17NBX> all taxis in Madrid'
        command, channel = taxi_bot.parse_bot_commands(BOT_COMMAND)
        answer = taxi_bot.handle_command(command, channel)
        self.assertIn("Found 1 taxi in Madrid:", answer)
    
    # def test_user_can_see_taxi_information(self):
    #     BOT_COMMAND[0]['text']='<@UCPF17NBX> taxi Opel'
    #     command, channel = taxi_bot.parse_bot_commands(BOT_COMMAND)
    #     answer = taxi_bot.handle_command(command, channel)
    #     self.assertIn("distance: ", answer)
    #     self.assertIn("https://www.google.com/maps/", answer)

    # def test_user_cant_see_book_no_address(self):
    #     BOT_COMMAND[0]['text']='<@UCPF17NBX> book taxi'
    #     command, channel = taxi_bot.parse_bot_commands(BOT_COMMAND)
    #     answer = taxi_bot.handle_command(command, channel)
    #     self.assertIn("distance: ", answer)
    #     self.assertIn("https://www.google.com/maps/", answer)

# Run the tests
if __name__ == "__main__":
    unittest.main()