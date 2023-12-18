""" Test file for the autolab procedures """
import time
import os
import json
import shutil
from multiprocessing import Process
import requests
import pytest

from mischbares.server import lang_server
from mischbares.action import lang_action
from mischbares.action import hamilton_action
from mischbares.server import hamilton_server
from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.orchestrator import orchestrator
from mischbares.config.main_config import config


port_orchestrator = config['servers']['orchestrator']['port']

host = config['servers']['autolab']['host']

autolab_port_server = config['servers']['autolabDriver']['port']
autolab_port_action = config['servers']['autolab']['port']

hamilton_port_action = config['servers']['hamilton']['port']
hamilton_port_server = config['servers']['hamiltonDriver']['port']

lang_port_server = config['servers']['langDriver']['port']
lang_port_action = config['servers']['lang']['port']

port_orchestrator = config['servers']['orchestrator']['port']

def run_lang_action():
    """Start the Autolab server."""
    lang_action.main()

def run_lang_server():
    """Start the Autolab server."""
    lang_server.main()

def run_action_hamilton():
    """Start the Autolab server."""
    hamilton_action.main()

def run_server_hamilton():
    """Start the Autolab server."""
    hamilton_server.main()

def run_action_autolab():
    """Start the Autolab server."""
    autolab_action.main()

def run_server_autolab():
    """Start the Autolab server."""
    autolab_server.main()

def run_orchestrator():
    """Start the Autolab server."""
    orchestrator.main()

@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server and action in a separate processes."""
    processes = [Process(target=run_server_hamilton),
                Process(target=run_action_hamilton),
                Process(target=run_lang_server),
                Process(target=run_lang_action),
                Process(target=run_server_autolab),
                Process(target=run_action_autolab),
                Process(target=run_orchestrator)]

    for proc in processes:
        try:
            proc.start()
            print("Waiting for processess to start...")
        except RuntimeError as e:
            print("Error starting server: ", e)
    time.sleep(15)
    yield processes
    for proc in processes:
        proc.kill()
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)
    shutil.rmtree('data/test', ignore_errors=True)

def test_autolab_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host}:{autolab_port_server}/docs", timeout=None)
    assert response.status_code == 200

def test_autolab_action_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host}:{autolab_port_action}/docs", timeout=None)
    assert response.status_code == 200

def test_hamilton_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host}:{hamilton_port_server}/docs", timeout=None)
    assert response.status_code == 200

def test_hamilton_action_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host}:{hamilton_port_action}/docs", timeout=None)
    assert response.status_code == 200

def test_lang_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host}:{lang_port_server}/docs", timeout=None)
    assert response.status_code == 200

def test_lang_action_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host}:{lang_port_action}/docs", timeout=None)
    assert response.status_code == 200

