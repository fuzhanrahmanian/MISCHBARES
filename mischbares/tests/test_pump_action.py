""" Test file for the pump action """
import time

from multiprocessing import Process

import requests


import pytest

from mischbares.action import hamilton_action
from mischbares.server import hamilton_server
from mischbares.config.main_config import config


host_url = config['servers']['hamilton']['host']
port_action = config['servers']['hamilton']['port']
port_server = config['servers']['hamiltonDriver']['port']


def run_action():
    """Start the Autolab server."""
    hamilton_action.main()


def run_server():
    """Start the Autolab server."""
    hamilton_server.main()


@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server and action in a separate processes."""
    proc_server = Process(target=run_server)
    proc_action = Process(target=run_action)
    try:
        proc_server.start()
        print("Waiting for server to start...")
        proc_action.start()
        print("Waiting for action to start...")
    except RuntimeError as e:
        print("Error starting server: ", e)
    time.sleep(40)
    yield proc_server, proc_action
    proc_server.kill()
    proc_action.kill()


def test_action_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port_action}/docs", timeout=None)
    assert response.status_code == 200


def test_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port_server}/docs", timeout=None)
    assert response.status_code == 200


def test_pumpSingleR_action():
    """Test the potential action."""
    params = dict(volume=int(500))
    response = requests.get(f"http://{host_url}:{port_action}/hamilton/pumpR", timeout=None,
                            params=params)
    assert response.status_code == 200