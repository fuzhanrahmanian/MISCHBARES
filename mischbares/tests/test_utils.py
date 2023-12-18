import os
import pytest
from mischbares.utils.utils import get_nested_value
from mischbares.config.main_config import config
from unittest.mock import patch
from mischbares.utils.utils import _check_token
import requests
from unittest.mock import patch
from mischbares.utils.utils import send_to_telegram


def test_get_nested_value_single_key():
    """
    Test case for get_nested_value function with a single key.
    """
    config = {'a': 1, 'b': 2, 'c': 3}
    keys = ['b']
    assert get_nested_value(config, keys) == 2


def test_get_nested_value_multiple_keys():
    """
    Test case for get_nested_value function with multiple keys.
    """
    config = {'a': {'b': {'c': 3}}}
    keys = ['a', 'b', 'c']
    assert get_nested_value(config, keys) == 3


def test_get_nested_value_key_not_found():
    """
    Test case for get_nested_value function when a key is not found.
    """
    config = {'a': {'b': {'c': 3}}}
    keys = ['a', 'd']
    with pytest.raises(KeyError, match="Key 'd' not found"):
        get_nested_value(config, keys)


def test_with_actual_config():
    """
    Test case for get_nested_value function using actual config values.
    """
    keys = config['servers']['hamiltonDriver']['qc_motor_safe_pos']
    values = config['lang']['langAction']['safe_waste_pos']
    assert get_nested_value(config, keys) == values


def test__check_token():
    """
    Test case for _check_token function.
    """
    from dotenv import load_dotenv
    load_dotenv()
    token, chat_id = _check_token()
    assert token == os.getenv('TELEGRAM_API_TOKEN')
    assert chat_id == os.getenv('TELEGRAM_CHAT_ID')


@patch('mischbares.utils.utils.log')
def test_send_to_telegram_success_info(mock_log):
    """
    Test case for send_to_telegram function when the message is successfully sent.
    """
    message = "Test message"
    message_type = "info"
    send_to_telegram(message, message_type)
    mock_log.info.assert_called_once_with("Message sent to telegram bot.")
    mock_log.warning.assert_not_called()

@patch('mischbares.utils.utils.log')
@patch('mischbares.utils.utils._check_token', return_value=(None, None))
def test_send_to_telegram_token_or_chat_id_not_set(mock_check_token, mock_log):
    """
    Test case for send_to_telegram function when the token or chat id is not set.
    """
    message = "Test message"
    message_type = "info"
    send_to_telegram(message, message_type)
    mock_check_token.assert_called_once()
    mock_log.warning.assert_called_once_with("Could not send message to telegram bot.")
    mock_log.info.assert_not_called()

@patch('mischbares.utils.utils.log')
@patch('mischbares.utils.utils._check_token', return_value=('test_token', 'test_chat_id'))
@patch('requests.get')
def test_send_to_telegram_failure(mock_requests_get, mock_check_token, mock_log):
    """
    Test case for send_to_telegram function when the message sending fails.
    """
    mock_requests_get.return_value.json.return_value = {'ok': False, 'description': 'Error'}
    message = "Test message"
    message_type = "info"
    send_to_telegram(message, message_type)
    mock_check_token.assert_called_once()
    mock_requests_get.assert_called_once_with("https://api.telegram.org/bottest_token/sendMessage?chat_id=test_chat_id&text= ℹ ℹ MISCHBARES INFO ℹ ℹ \nTest message")
    mock_log.warning.assert_called_once_with("Could not send message to telegram bot: Error")
    mock_log.info.assert_not_called()

@patch('mischbares.utils.utils.log')
def test_send_to_telegram_success_error(mock_log):
    """
    Test case for send_to_telegram function when the message is successfully sent.
    """
    message = "Error message"
    message_type = "error"
    send_to_telegram(message, message_type)
    mock_log.info.assert_called_once_with("Message sent to telegram bot.")
    mock_log.warning.assert_not_called()