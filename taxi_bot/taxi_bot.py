import os
import time
import re
from slackclient import SlackClient
from math import radians, cos, sin, asin, sqrt
import json
from urllib import request, parse
from urllib.error import URLError, HTTPError
try:
    from . import utilities
except:
        import utilities

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None
google_api_key = os.environ.get('GOOGLE_API_KEY')

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = ("all taxis", "all taxis in Madrid", "book taxi to Calle Mayor 12, Madrid")
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
#TAXI_ENDPOINT = "http://130.211.103.134:4000/taxis"
# TAXI_ENDPOINT = "http://localhost:8080/taxis"
TAXI_ENDPOINT = "https://mock-travel-apis.herokuapp.com/taxis"
CITY = ""
ADDRESS = ""
COORDINATES = (0,0)
DESTINATION_ADDRESS = ""

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        print("Event: {}".format(event["type"]))
        if event["type"] == "message" and not "subtype" in event:
            print("Message: {}".format(event["text"]))
            user_id, message = parse_direct_mention(event["text"])
            print("User ID: {}".format(user_id))
            if user_id == starterbot_id or user_id == 'UCPF17NBX':
                print("Message: {}".format(message))
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Sorry I did not understand you command. Try: "
    for example in EXAMPLE_COMMAND:
        default_response+= "\n - " + example
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    global CITY
    global ADDRESS
    global COORDINATES
    global DESTINATION_ADDRESS
    
    if command.startswith("all taxis in"):
        city = command.replace('all taxis in ','')
        city = city.split(' ')[0]
        CITY = city
        taxis = get_taxis(city)
        print(taxis)
        if taxis:
            taxiOrTaxis = 'taxis' if len(taxis) > 1 else 'taxi'
            response = "Found {} {} in {}:".format(len(taxis), taxiOrTaxis, city)
            for taxi in taxis:
                response += "\n - {}".format(taxi["name"])
        else:
            response = "Sorry, there are currently no taxis in {}".format(city)

    elif command.startswith("address is "):
        address = command.replace('address is ','')
        ADDRESS = address
        coordinates = utilities.get_geocoordinates(address)
        COORDINATES = coordinates
        response = "Your address is: {}\nYour coordinates are: {}".format(address, coordinates)

    elif command.startswith("all taxis"):
        taxis = get_taxis()
        if taxis:
            response = "There are currently {} taxis in the system.".format(len(taxis))
            response += "\nPlease specify your city. For e.g. you can ask me \"all taxis in Madrid\" "
        else:
            response = "Sorry, there are currently no taxis in the system."

    elif command.startswith("taxi"):
        taxi_id = command.replace('taxi ','')
        if CITY == '':
            response = "Please specify your city, for e.g. 'all taxis in Madrid'"
        else:
            taxi_info = get_taxi_info(CITY, taxi_id)
            if taxi_info:
                lat = taxi_info["location"]["lat"]
                lon = - taxi_info["location"]["lon"]
                dist = utilities.get_distance((40.415970, -3.712050), (lat, lon))
                map_url = "https://www.google.com/maps/search/?query={},{}&api={}".format(
                    lat, lon, google_api_key)
                response = "Taxi {} is {}, distance: {}km (see <{}|map>)".format(
                    taxi_id, taxi_info["state"], dist, map_url)
            else:
                response = "Could not get information for taxi {}".format(taxi_id)

    elif command.startswith("book taxi to"):
        destination_address = command.replace('book taxi to ','')
        if ADDRESS == "":
            response = "Please specify your address, for e.g. 'address is Calle Mayor 12, Madrid'"
        elif destination_address == "":
            response = "Please book a taxi to a concrete address, for e.g. 'book taxi to Calle Mayor 12, Madrid'"
        else:
            destination_coordinates = utilities.get_geocoordinates(destination_address)
            DESTINATION_ADDRESS = destination_address
            taxi_info = request_taxi()
            print(taxi_info)
            if taxi_info:
                response = "Successfully requested taxi {}. Taxi status is now '{}'.".format(taxi_info["name"], 
                           taxi_info["state"])
            else:
                response = "Failed to reserve taxi."
                
    else:
        pass

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        # attachments= [
        #     {
        #         "image_url": "https://www.sciencemag.org/sites/default/files/styles/article_main_image_-_1280w__no_aspect_/public/cc_E2B865_hires_16x9.jpg?itok=cRrAYAq9",
        #         "text": "And here’s an attachment!"
        #     }
        # ]
    )

    return response or default_response

def get_taxis(city=''):
    if city:
        url = TAXI_ENDPOINT + '/' + city.lower()
    else:
        url = TAXI_ENDPOINT
    taxis = utilities.api_call(url)
    return taxis["data"]

def get_taxi_info(city, taxi_id):
    url = TAXI_ENDPOINT + '/' + city + "/" + taxi_id
    taxi_info = utilities.api_call(url)
    return taxi_info["data"]

def get_nearest_taxi(city=None):
    all_taxis = get_taxis(city)
    distance = 1000
    start_address = (40.415970, -3.712050)
    for taxi in all_taxis:
        taxi_location = (taxi["location"]["lat"], -taxi["location"]["lon"])
        new_distance = utilities.get_distance(start_address, taxi_location)
        if new_distance < distance:
            distance = new_distance
            taxiId = taxi["name"]
            taxiCity = taxi["city"]
    if distance < 1000:
        return (taxiId, taxiCity)
    else:
        return None

def request_taxi(city='', taxi_id=''):
    if taxi_id == '':
        taxi = get_nearest_taxi()
        taxi_id = taxi[0]
        city = taxi[1]
    url = "{}/{}/{}".format(TAXI_ENDPOINT, city, taxi_id)
    body = parse.urlencode({"state": "hired"}).encode()
    requested_taxi = utilities.api_call(url, body) 
    return requested_taxi["data"]

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Taxi Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            #print("Slack read is: {}".format(slack_client.rtm_read()))
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")