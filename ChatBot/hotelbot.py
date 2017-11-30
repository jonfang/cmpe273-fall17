import os
import time
from slackclient import SlackClient

#Set up environment parameters
SLACK_BOT_TOKEN='xoxb-267332245988-szpTYxky9pHRhi74NnhQtDsi'
BOT_ID = 'U7V9S77V2'

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = ["hotel", "book", "date","room","checkout","review"]

#Receipt parameters
hotel_receipt = {
"start_date":"00-00-0000",
"end_date":"00-00-0000", 
"room_size":0,
"price": 0
}

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)

class HotelBot:
    """
        Hotel Bot class that handles commands at the high level
    """
    def __init__(self):
        pass

    def handle_command(self, command, channel):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """
        response = "Not sure what you mean. Use the *" + ",".join(EXAMPLE_COMMAND) + \
               "* command with numbers, delimited by spaces."
        if any(command.startswith(s) for s in EXAMPLE_COMMAND):
            if command.startswith('hotel'):
                response = "Hotel bot is ready. Below are the list of commands:\n" + "\n".join(EXAMPLE_COMMAND)
            elif command.startswith('date'):
                response = "Book a date"
            elif command.startswith('room'):
                response = "Book a room"
            elif command.startswith('checkout'):
                response = "Checkout booking"
            elif command.startswith('review'):
                response = self.format_receipt(hotel_receipt)
            else:
                response = "Sure...write some more code then I can do that!"
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

    def format_receipt(self, receipt):
        response = ""
        for key, val in receipt.items():
            pair = str(key) + " : " + str(val) + "\n"
            response+=pair
        return response

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        hotelBot = HotelBot()
        print("HotelBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                hotelBot.handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
