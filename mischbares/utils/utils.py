""" This module defines some utility functions for the MISCHBARES project. """
import time
import os
import json
import requests
from dotenv import load_dotenv

from mischbares.logger import logger
from mischbares.config.main_config import config


log = logger.get_logger("utils")


def create_dir(directory):
    """Checks if a directory is present, if not creates one at the given location
    Args:
        directory (str): Location where the directory should be created
    """

    if not os.path.exists(directory):
        os.makedirs(directory)
        log.info(f"Created directory {directory}.")
    else:
        log.info(f"Directory {directory} already exists.")
    return directory


def assemble_file_name(*args):
    """Assemble a file name from the given arguments
    Returns:
        str: The assembled file name
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S_")
    return timestamp+"_".join(list(args))


def save_data_as_json(directory, data, name):
    """Save the given data as json
    Args:
        directory (str): The directory where the data should be saved
        data (dict): The data that should be saved
        name (str): The name of the file
    """

    log.info(f"Saving data in {directory} as json")
    with open(os.path.join(directory, f"{name}.json"), 'w', encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False)


def load_data_as_json(directory, name):
    """ Load the given data as json
    Args:
        directory (str): The directory where the data should be saved
        name (str): The name of the file
    """
    log.info(f"Loading data from {directory} as json")
    with open(os.path.join(directory, name), 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_nested_value(config, keys):
    """
    Recursively get the value from a nested dictionary using a list of keys.

    Args:
        config (dict): The dictionary to search in.
         keys (list): A list of keys to search for.

    Returns:
        The value corresponding to the given keys.

    Raises:
        KeyError: If the key is not found in the dictionary.
    """
    # Base case: if there's only one key, return the corresponding value
    if len(keys) == 1:
        if keys[0] in config:
            return config[keys[0]]
        else:
            raise KeyError(f"Key '{keys[0]}' not found")

    # Recursive case: navigate one level deeper in the dictionary
    if keys[0] in config:
        return get_nested_value(config[keys[0]], keys[1:])
    else:
        raise KeyError(f"Key '{keys[0]}' not found")


def send_to_telegram(message, message_type):
    """
    Sends a message to a Telegram bot.

    Args:
        message (str): The message to be sent.
        message_type (str): The type of the message ("error" or "info").

    """

    if message_type == "error":
        message = " ‼ ‼ MISCHBARES ALERT ‼ ‼ \n" + message
    if message_type == "info":
        message = " ℹ ℹ MISCHBARES INFO ℹ ℹ \n" + message

    token, chat_id = _check_token()

    if (token is None) or (chat_id is None):
        log.warning("Could not send message to telegram bot.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url).json()
    if res['ok']:
        log.info("Message sent to telegram bot.")
    else:
        log.warning("Could not send message to telegram bot: {}".format(res['description']))


def _check_token():
    """
    Checks if the Telegram API token and chat ID are set either in environment variables or in the config file.
    If not set, it logs a warning message.
    Returns:
        tuple: A tuple containing the Telegram API token and chat ID.
    """
    load_dotenv()
    token = os.getenv("TELEGRAM_API_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if token is None:
        # Check if the token is set in the config file
        if (config['QC']['telegram']['api_token'] is not None) or (config['QC']['telegram']['api_token'] != ""):
            token = config['QC']['telegram']['api_token']
        else:
            log.warning("Telegram API token not set in the config_file")
        log.warning("Telegram API token not set in environment variables. Create a .env file and set the token as TELEGRAM_API_TOKEN")
    if chat_id is None:
        if (config['QC']['telegram']['chat_id'] is not None) or (config['QC']['telegram']['chat_id'] != ""):
            chat_id = config['QC']['telegram']['chat_id']
        log.warning("Telegram chat id not set in environment variables. Create a .env file and set the chat id as TELEGRAM_CHAT_ID")

    return token, chat_id