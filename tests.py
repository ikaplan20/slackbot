from slack.web import client
import hybridbot
import slack 
import pytest
import os
from pathlib import Path 
from unittest import mock

@pytest.fixture
def slack_client():
    from dotenv import load_dotenv
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)
    return slack.WebClient(token=os.environ['SLACK_TOKEN'])


def test_webclient(slack_client):
    assert slack_client

@mock.patch('hybridbot.client.chat_postMessage', return_value={'ts':'1'}, autospec=True)
def test_send_welcome_message(mock_chat):
    channel, user = 'test', '1'
    actual = hybridbot.send_welcome_message(channel, user)
    mock_chat.assert_called_once()
    assert isinstance(actual, dict)
    assert channel in actual 
    

# testing notes
# test contracts (uncoupled inputs, expected output boundaries, and invariants)
# design with tests in mind
# test document code