import slack
import os
import flask
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
app = Flask(__name__)

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# handles events from the slack api
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']


class WelcomeMessage:
    START_TEXT = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': 'Welcome to the Hybrid Ambassaders workspace!'
        }
    }

    DIVIDER = {'type': 'divider'}

    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.icon_emoji = ':robot_face:'
        self.timestamp = ''
        self.completed = False

    def get_message(self):
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            'username': 'Welcome Slackbot',
            'icon_emoji': self.icon_emoji,
            'blocks': [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }

    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_large_square:'

        text = f'{checkmark} *React with a :sunglasses: to let me know you got it!*'

        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text}}


message_counts = {} # maps to Members.message_counts
welcome_messages = {} #maps to Message Class


def send_welcome_message(channel, user):
    welcome = WelcomeMessage(channel, user)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestamp = response['ts']

    if channel not in welcome_messages:
        welcome_messages[channel] = {}
    welcome_messages[channel][user] = welcome
    return welcome_messages

# events
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    text = event.get('text')
    user_id = event.get('user')

    if user_id != None and BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1
        if text.lower() == 'start':
            send_welcome_message(f'@{user_id}', user_id)


@slack_event_adapter.on('reaction_added')
def reaction(payload):
    event = payload.get('event',{})
    channel_id = event.get('item',{}).get('channel')
    user_id = event.get('user')

    if f'@{user_id}' not in welcome_messages:
        return 
    
    welcome = welcome_messages[f'@{user_id}'][user_id] #channel_id/user_id
    welcome.completed = True # switches for update
    welcome.channel = channel_id
    message = welcome.get_message()
    updated_message = client.chat_update(**message) #stars unpack dict into kwargs
    welcome.timestamp = updated_message['ts']



#! update slash command url and route for this to work in dev
@app.route('/messages', methods=['POST'])
def message_count():
    data = request.form
    print(data)
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(
        channel=channel_id, text=f'Message: {message_count}')
    return flask.Response(), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)


# TODO
