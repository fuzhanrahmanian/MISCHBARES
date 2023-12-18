""" Test file for the lang action """
import time

from multiprocessing import Process

import requests


import pytest

from mischbares.action import lang_action
from mischbares.server import lang_server
from mischbares.config.main_config import config


host_url = config['servers']['lang']['host']
port_action = config['servers']['lang']['port']
port_server = config['servers']['langDriver']['port']

def run_action():
    """Start the Autolab server."""
    lang_action.main()

def run_server():
    """Start the Autolab server."""
    lang_server.main()


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
    time.sleep(20)
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


def test_getPos():
    """Test function getPos."""
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 0
    assert round(eval(position.content)['data']['data']['pos'][1], 1) == 0
    assert round(eval(position.content)['data']['data']['pos'][2], 1) == 0


def test_moveRelFar():
    """Test function moveRelFar."""
    params = dict(dx=1, dy=0, dz=0)
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveRel",
                            params=params,
                            timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 1
    # Return to home position
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveHome", timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 0


def test_moveAbsFar():
    """Test function moveAbsFar."""
    params = dict(dx=2, dy=2, dz=2)
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveAbs",
                            params=params,
                            timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 2
    assert round(eval(position.content)['data']['data']['pos'][1], 1) == 2
    assert round(eval(position.content)['data']['data']['pos'][2], 1) == 2
    # Return to home position
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveHome", timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 0


def test_moveWaste():
    """Test function moveWaste."""
    waste_pos = config["lang"]["langAction"]["safe_waste_pos"]
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveWaste",timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == waste_pos[0]
    assert round(eval(position.content)['data']['data']['pos'][1], 1) == waste_pos[1]
    assert round(eval(position.content)['data']['data']['pos'][2], 1) == waste_pos[2]
    # Return to home position
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveHome", timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 0
    assert round(eval(position.content)['data']['data']['pos'][1], 1) == 0
    assert round(eval(position.content)['data']['data']['pos'][2], 1) == 0


def test_removeDrop():
    """Test function removeDrop."""
    last_point = config["lang"]["langAction"]["safe_clean_pos_2"]
    response = requests.get(f"http://{host_url}:{port_action}/lang/RemoveDroplet",timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == last_point[0]
    assert round(eval(position.content)['data']['data']['pos'][1], 1) == last_point[1]
    assert round(eval(position.content)['data']['data']['pos'][2], 1) == last_point[2]
    # Return to home position
    response = requests.get(f"http://{host_url}:{port_action}/lang/moveHome", timeout=None)
    assert response.status_code == 200
    position = requests.get(f"http://{host_url}:{port_action}/lang/getPos", timeout=None)
    assert position.status_code == 200
    assert round(eval(position.content)['data']['data']['pos'][0], 1) == 0
    assert round(eval(position.content)['data']['data']['pos'][1], 1) == 0
    assert round(eval(position.content)['data']['data']['pos'][2], 1) == 0