""" Test file for the autolab server """
import shutil
from time import sleep
from multiprocessing import Process
import pytest
import json
import numpy as np

import requests
from mischbares.config.main_config import config
from mischbares.server import autolab_server

host_url = config['servers']['autolabDriver']['host']
port = config['servers']['autolabDriver']['port']

def run_server():
    """Start the Autolab server."""
    autolab_server.main()


@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server in a separate process."""
    proc = Process(target=run_server)
    try:
        proc.start()
        print("Waiting for server to start...")
    except RuntimeError as e:
        print("Error starting server: ", e)
    sleep(15)
    yield proc
    proc.kill()
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port}/docs", timeout=None)
    assert response.status_code == 200


def test_potential_server():
    """Test the potential server."""
    response = requests.get(f"http://{host_url}:{port}/autolabDriver/potential", timeout=None)
    assert response.status_code == 200
    assert round(eval(response.content)["data"]["potential"], 2) == 0.0


def test_applied_potential_server():
    """Test the applied voltage server."""
    response = requests.get(f"http://{host_url}:{port}/autolabDriver/appliedpotential",
                            timeout=None)
    assert response.status_code == 200
    assert round(eval(response.content)["data"]["applied_potential"], 2) == 0.0


def test_current_server():
    """Test the current server."""
    response = requests.get(f"http://{host_url}:{port}/autolabDriver/current", timeout=None)
    assert response.status_code == 200
    assert round(eval(response.content)["data"]["current"], 2) == 0.0


def test_measure_status_server():
    """Test the measure status server."""
    response = requests.get(f"http://{host_url}:{port}/autolabDriver/ismeasuring", timeout=None)
    assert response.status_code == 200
    evaluate_status = eval(response.content.decode("utf-8").replace("false", "False"))
    assert evaluate_status["data"]["measure_status"] is False


def test_perform_measurment_ocp_server():
    """Test the perform ocp measurment server."""
    params =dict(procedure= 'ocp', plot_type= 'tCV',
                parse_instruction=json.dumps(['recordsignal']),
                save_dir= "mischbares/tests",
                setpoints= json.dumps({'recordsignal': {'Duration (s)': 10}}),
                current_range = "10mA",on_off_status= 'off',
                measure_at_ocp = False)

    response = requests.get(f"http://{host_url}:{port}/autolabDriver/measure",
                            params=params, timeout=None)
    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                            .replace("false", "False"))
    evaluate_potential = evaluate_potential['data']['recordsignal']['WE(1).Potential'][-5:]
    evaluate_potential = round(np.mean(evaluate_potential), 2)
    assert response.status_code == 200
    assert evaluate_potential == 0.0


def test_perform_measurment_cp_server():
    """Test the perform cp measurment at ocp voltage server."""
    params =dict(procedure= 'cp', plot_type= 'tCV',
                parse_instruction=json.dumps(['recordsignal']),
                save_dir= "mischbares/tests",
                setpoints= json.dumps({'applycurrent': {'Setpoint value': 0.00001},\
                        'recordsignal': {'Duration (s)': 10, 'Interval time (s)': 0.5}}),
                current_range = "100uA",on_off_status= 'off',
                measure_at_ocp = True)

    response = requests.get(f"http://{host_url}:{port}/autolabDriver/measure",
                            params=params, timeout=None)
    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                            .replace("false", "False").replace("true", "True"))
    evaluate_potential = evaluate_potential['data']['recordsignal']['WE(1).Current'][-5:]
    evaluate_potential = round(np.mean(evaluate_potential), 2)
    assert response.status_code == 200
    assert evaluate_potential == 0.0


def test_perform_measurment_ca_server():
    """Test the perform ca measurment at ocp voltage server."""
    params =dict(procedure= 'ca', plot_type= 'tCV',
                parse_instruction=json.dumps(['recordsignal']),
                save_dir= "mischbares/tests",
                setpoints= json.dumps({'applypotential': {'Setpoint value': 0.7},\
                    'recordsignal': {'Duration (s)': 5, 'Interval time (s)': 0.5}}),
                current_range = "100uA",on_off_status= 'off',
                measure_at_ocp = True)

    response = requests.get(f"http://{host_url}:{port}/autolabDriver/measure",
                            params=params, timeout=None)
    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                            .replace("false", "False").replace("true", "True"))
    evaluate_potential = evaluate_potential['data']['recordsignal']['WE(1).Potential'][-5:]
    evaluate_potential = round(np.mean(evaluate_potential), 2)
    assert response.status_code == 200
    assert evaluate_potential == 0.7


def test_perform_measurment_eis_server():
    """Test the perform eis measurment at ocp voltage server."""
    params =dict(procedure= 'eis', plot_type= 'impedance',
                parse_instruction= json.dumps(['FIAMeasPotentiostatic', 'FIAMeasurement']),
                save_dir= "mischbares/tests",
                setpoints= json.dumps({}),
                current_range = "1mA",on_off_status= 'off',
                measure_at_ocp = True)

    response = requests.get(f"http://{host_url}:{port}/autolabDriver/measure",
                            params=params, timeout=None)
    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                            .replace("false", "False").replace("true", "True"))
    evaluate_potential = evaluate_potential['data']['FIAMeasurement']['Potential (DC)'][0]
    evaluate_potential = round(np.mean(evaluate_potential), 1)
    assert response.status_code == 200
    assert evaluate_potential == 0.0
