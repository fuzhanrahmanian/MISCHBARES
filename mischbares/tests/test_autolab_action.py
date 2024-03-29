""" Test file for the autolab action """
import time
import shutil
from multiprocessing import Process

import json
import requests
import numpy as np

import pytest

from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.config.main_config import config


host_url = config['servers']['autolab']['host']
port_action = config['servers']['autolab']['port']
port_server = config['servers']['autolabDriver']['port']

def run_action():
    """Start the Autolab server."""
    autolab_action.main()


def run_server():
    """Start the Autolab server."""
    autolab_server.main()


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
    time.sleep(15)
    yield proc_server, proc_action
    proc_server.kill()
    proc_action.kill()
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_action_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port_action}/docs", timeout=None)
    assert response.status_code == 200


def test_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port_server}/docs", timeout=None)
    assert response.status_code == 200


def test_potential_action():
    """Test the potential action."""
    response = requests.get(f"http://{host_url}:{port_action}/autolab/potential", timeout=None)
    assert response.status_code == 200
    assert round(eval(response.content)["data"]["data"]["potential"], 2) == 0.0


def test_applied_potential_action():
    """Test the applied voltage action."""
    response = requests.get(f"http://{host_url}:{port_action}/autolab/appliedpotential",
                            timeout=None)
    assert response.status_code == 200
    assert round(eval(response.content)["data"]["data"]["applied_potential"], 2) == 0.0


def test_current_action():
    """Test the current action."""
    response = requests.get(f"http://{host_url}:{port_action}/autolab/current", timeout=None)
    assert response.status_code == 200
    assert round(eval(response.content)["data"]["data"]["current"], 2) == 0.0


def test_measure_status_action():
    """Test the measure status action."""
    response = requests.get(f"http://{host_url}:{port_action}/autolab/ismeasuring",
                            timeout=None)
    assert response.status_code == 200
    evaluate_status = eval(response.content.decode("utf-8").replace("false", "False"))
    assert evaluate_status["data"]["data"]["measure_status"] is False


def test_autolab_measure_ocp_action():
    """Test the autolab measure action with ocp procedure."""
    params =dict(procedure= 'ocp', plot_type= 'tCV',
                 parse_instruction= json.dumps(['recordsignal']),
                 save_dir= "mischbares/tests",
                 setpoints= json.dumps({'recordsignal': {'Duration (s)': 10}}),
                 current_range = "10mA",on_off_status= 'off',
                 optional_name = 'ocp', measure_at_ocp = False)

    response = requests.get(f"http://{host_url}:{port_action}/autolab/measure", params=params,
                            timeout=None)

    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                                .replace("false", "False"))
    evaluate_potential = evaluate_potential['data']['data']['recordsignal']['WE(1).Potential'][-5:]
    evaluate_potential = round(np.mean(evaluate_potential), 2)
    assert response.status_code == 200
    assert evaluate_potential == 0.0


def test_autolab_measure_cp_action():
    """Test the autolab measure action with cp procedure."""
    params =dict(procedure= 'cp', plot_type= 'tCV',
                 parse_instruction= json.dumps(['recordsignal']),
                 save_dir= "mischbares/tests",
                 setpoints= json.dumps({'applycurrent': {'Setpoint value': 0.00001},\
                        'recordsignal': {'Duration (s)': 10, 'Interval time (s)': 0.5}}),
                 current_range = "10mA",on_off_status= 'off',
                 optional_name = 'cp', measure_at_ocp = True)

    response = requests.get(f"http://{host_url}:{port_action}/autolab/measure", params=params,
                            timeout=None)

    evaluate_current = eval(response.content.decode("utf-8").replace("null", "None")\
                                .replace("false", "False").replace("true", "True"))
    evaluate_current = evaluate_current['data']['data']['recordsignal']['WE(1).Current'][-5:]
    evaluate_current = round(np.mean(evaluate_current), 2)
    assert response.status_code == 200
    assert evaluate_current == 0.0


def test_autolab_measure_ca_action():
    """Test the autolab measure action with ca procedure."""
    params =dict(procedure= 'ca', plot_type= 'tCV',
                 parse_instruction= json.dumps(['recordsignal']),
                 save_dir= "mischbares/tests",
                 setpoints=  json.dumps({'applypotential': {'Setpoint value': 0.7},\
                    'recordsignal': {'Duration (s)': 5, 'Interval time (s)': 0.5}}),
                 current_range = "10mA",on_off_status= 'off',
                 optional_name = 'ca', measure_at_ocp = True)

    response = requests.get(f"http://{host_url}:{port_action}/autolab/measure", params=params,
                            timeout=None)

    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                                .replace("false", "False").replace("true", "True"))
    evaluate_potential = evaluate_potential['data']['data']['recordsignal']['WE(1).Potential'][-5:]
    evaluate_potential = round(np.mean(evaluate_potential), 2)
    assert response.status_code == 200
    assert evaluate_potential == 0.7


def test_autolab_measure_eis_action():
    """Test the autolab measure action with eis procedure."""
    params =dict(procedure= 'eis', plot_type= 'impedance',
                 parse_instruction= json.dumps(['FIAMeasPotentiostatic', 'FIAMeasurement']),
                 save_dir= "mischbares/tests",
                 setpoints=  json.dumps({}),
                 current_range = "10mA",on_off_status= 'off',
                 optional_name = 'eis', measure_at_ocp = True)

    response = requests.get(f"http://{host_url}:{port_action}/autolab/measure", params=params,
                            timeout=None)

    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                                .replace("false", "False").replace("true", "True"))
    evaluate_potential = evaluate_potential['data']['data']['FIAMeasurement']['Potential (DC)'][0]
    evaluate_potential = round(np.mean(evaluate_potential), 1)
    assert response.status_code == 200
    assert evaluate_potential == 0.0
