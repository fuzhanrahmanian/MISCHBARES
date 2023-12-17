""" Test file for the autolab procedures """
import time
import os
import json
import shutil
from multiprocessing import Process
import requests
import pytest

from mischbares.action import hamilton_action
from mischbares.server import hamilton_server
from mischbares.orchestrator import orchestrator
from mischbares.config.main_config import config



port_orchestrator = config['servers']['orchestrator']['port']

host_url = config['servers']['hamilton']['host']
port_action = config['servers']['hamilton']['port']
port_server = config['servers']['hamiltonDriver']['port']

def run_action_hamilton():
    """Start the Autolab server."""
    hamilton_action.main()


def run_server_hamilton():
    """Start the Autolab server."""
    hamilton_server.main()


def run_orchestrator():
    """Start the Autolab server."""
    orchestrator.main()


@pytest.fixture(scope="session", autouse=True)
def server_instance():
    """Start the server and action in a separate processes."""
    processes = [Process(target=run_server_hamilton),
                 Process(target=run_action_hamilton),
                 Process(target=run_orchestrator)]

    for proc in processes:
        try:
            proc.start()
            print("Waiting for processess to start...")
        except RuntimeError as e:
            print("Error starting server: ", e)
    time.sleep(40)
    yield processes
    for proc in processes:
        proc.kill()


def test_server_connection():
    """Test if the hamilton server is running."""
    response = requests.get(f"http://{host_url}:{port_server}/docs", timeout=None)
    assert response.status_code == 200


def test_action_connection():
    """Test if the hamilton server is running."""
    response = requests.get(f"http://{host_url}:{port_action}/docs", timeout=None)
    assert response.status_code == 200


def test_start_orchestrator():
    """ Test if the experiment is added to the orchestrator. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/start'],
                  params={'start': {'collectionkey': "test"}}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    time.sleep(5)
    assert os.path.exists("data/test/SDC_test_session_0.h5") is True
    #shutil.rmtree("data/test")


def test_hamilton_pumpSingleR():
    soe =[f'hamilton/pumpR_0']
    params = {'pumpR_0':{'volume': 600}}
    sequence = dict(soe=soe,params=params,meta={})

    parameters = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200


def test_finish_orchestrator():
    """ Test if the experiment is added to the orchestrator. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/finish'],
                  params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    shutil.rmtree("data/test")
