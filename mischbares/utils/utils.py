""" This module defines some utility functions for the MISCHBARES project. """
import time
import os
import json

from mischbares.logger import logger



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