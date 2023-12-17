""" Test file for the autolab server """
import shutil
from time import sleep
from multiprocessing import Process
import json
import pytest
import numpy as np

import requests
from mischbares.config.main_config import config
from mischbares.server import lang_server

host_url = config['servers']['langDriver']['host']
port = config['servers']['langDriver']['port']

def run_server():
    """Start the Autolab server."""
    lang_server.main()


@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server in a separate process."""
    proc = Process(target=run_server)
    try:
        proc.start()
        print("Waiting for server to start...")
    except RuntimeError as e:
        print("Error starting server: ", e)
    sleep(20)
    yield proc
    proc.kill()


def test_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port}/docs", timeout=None)
    assert response.status_code == 200


def test_lang_server_connect():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port}/langDriver/connect", timeout=None)
    assert response.status_code == 200


def test_lang_server_goHome():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port}/langDriver/goHome", timeout=None)
    assert response.status_code == 200


def test_lang_server_moveRelFar():
    """Test if the server is running."""
    params = dict(dx=1, dy=0, dz=0)
    response = requests.get(f"http://{host_url}:{port}/langDriver/moveRelFar",
                            params=params,
                            timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port}/langDriver/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['pos'][0], 1) == 1
    # go back to home
    requests.get(f"http://{host_url}:{port}/langDriver/goHome", timeout=None)
    position = requests.get(f"http://{host_url}:{port}/langDriver/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['pos'][0], 1) == 0
    assert round(eval(position.content)['data']['pos'][1], 1) == 0

