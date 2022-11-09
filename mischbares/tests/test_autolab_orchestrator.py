""" Test file for the autolab action """
import time
import os
import shutil
import json
from multiprocessing import Process

import requests

import pytest

from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.orchestrator import orchestrator
from mischbares.config.main_config import config


host_url = config['servers']['autolab']['host']
port_action = config['servers']['autolab']['port']
port_server = config['servers']['autolabDriver']['port']
port_orchestrator = config['servers']['orchestrator']['port']

def run_action():
    """Start the Autolab server."""
    autolab_action.main()


def run_server():
    """Start the Autolab server."""
    autolab_server.main()


def run_orchestrator():
    """Start the Autolab server."""
    orchestrator.main()


@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server and action in a separate processes."""
    processes = [Process(target=run_server),
                 Process(target=run_action),
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

def test_server_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port_server}/docs", timeout=None)
    assert response.status_code == 200


def test_action_connection():
    """Test if the server is running."""
    response = requests.get(f"http://{host_url}:{port_action}/docs", timeout=None)
    assert response.status_code == 200


def test_start_orchestrator():
    """ Test if the experiment is added to the orchestrator """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/start'],
                  params={'start': {'collectionkey': "test"}}, meta=dict())
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    time.sleep(5)
    assert os.path.exists("data/test/SDC_test_session_0.h5") is True


def test_send_measurment():
    """ Test if the experiment is added to the orchestrator """
    sequence = dict(soe=['autolab/measure_0'],
                    params={'measure_0': {'procedure':'ocp',
                                          'setpoints': "{'FHLevel':{'Duration':10}}",
                                          "plot_type":'tCV',
                                          "on_off_status":'off',
                                          "save_dir":'mischbares/tests',
                                          "parse_instruction":'recordsignal'}}, meta=dict())
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    # wait for the measurement to finish
    time.sleep(15)
    # Check if there is a file that ends with autolab.nox
    for file_endings in ['Autolab.nox', 'Autolab.json', 'Autolab_configuration.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1



def test_finish_orchestrator():
    """ Test if the experiment is added to the orchestrator """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/finish'],
                  params={'finish': None}, meta=dict())
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
