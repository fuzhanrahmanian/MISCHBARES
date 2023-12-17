""" Test file for the autolab server """
import shutil
from time import sleep
from multiprocessing import Process
import json
import pytest
import numpy as np

import requests
from mischbares.config.main_config import config
from mischbares.server import hamilton_server

host_url = config['servers']['hamiltonDriver']['host']
port = config['servers']['hamiltonDriver']['port']

def run_server():
    """Start the Autolab server."""
    hamilton_server.main()


@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server in a separate process."""
    proc = Process(target=run_server)
    try:
        proc.start()
        print("Waiting for server to start...")
    except RuntimeError as e:
        print("Error starting server: ", e)
    sleep(30)
    yield proc
    proc.kill()


def test_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port}/docs", timeout=None)
    assert response.status_code == 200


def test_pump_server():
    """Test the potential server."""
    params=dict(leftVol=10,rightVol=10,
                leftPort=0,rightPort=0,
                delayLeft=0,delayRight=0)
    response = requests.get(f"http://{host_url}:{port}/hamiltonDriver/pump", timeout=None,
                            params=params)
    assert response.status_code == 200
    status = requests.get(f"http://{host_url}:{port}/hamiltonDriver/getStatus", timeout=None)
    assert status.status_code == 200
    assert eval(status.content.decode("utf-8"))["data"]["volume_nL_left"] == 10