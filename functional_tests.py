# functional_tests.py
# by Sam Heyman
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from slackclient import SlackClient
from qabify_bot.qabify_bot import parse_bot_commands, handle_command


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# user commands to test
HELLO = [{
                'type': 'message', 
                'text': '<@UCPF17NBX> hello', 
                'channel': 'CCP3YDEDS', 
}]
ALL_TAXIS = [{
                'type': 'message', 
                'text': '<@UCPF17NBX> all taxis', 
                'channel': 'CCP3YDEDS', 
}]
ALL_TAXIS_IN_MADRID = [{
                'type': 'message', 
                'text': '<@UCPF17NBX> all taxis in Madrid', 
                'channel': 'CCP3YDEDS', 
}]
BOOK_TAXI = [{
                'type': 'message', 
                'text': '<@UCPF17NBX> all taxis', 
                'channel': 'CCP3YDEDS', 
}]
BOOK_TAXI_TO_ADDRESS = [{
                'type': 'message', 
                'text': '<@UCPF17NBX> all taxis', 
                'channel': 'CCP3YDEDS', 
}]


class SlackBotUserTest(unittest.TestCase):

    # user opens Slack in the browser
    slack_client.rtm_connect(with_team_state=False)
    print("QAbify Bot connected and running!")
    # Read bot's user ID by calling Web API method `auth.test`
    starterbot_id = slack_client.api_call("auth.test")["user_id"]
    print("ok!")
    command, channel = parse_bot_commands(ALL_TAXIS)
    answer = handle_command(command, channel)
    if answer == "There are currently 3 taxis in the system.":
        print("Success!")
    else:
        print("Fail: {}".format(answer))

# Run the tests
if __name__ == "__main__":
    unittest.main()