""" Test file for the autolab orchestrator """
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


def test_send_measurment_ocp():
    """ Test if the ocp experiment is added to the orchestrator. """
    sequence = dict(soe=['autolab/measure_0'],
                    params={'measure_0': {'procedure':'ocp',
                                'plot_type':'tCV',
                                'parse_instruction': json.dumps(['recordsignal']),
                                'save_dir':'mischbares/tests',
                                'setpoints': json.dumps({'recordsignal': {'Duration (s)': 10}}),
                                'current_range': '10mA',
                                'on_off_status':'off',
                                'optional_name': 'ocp',
                                'measure_at_ocp': False}},
                    meta={})

    parameters = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    # wait for the measurement to finish
    time.sleep(20)
    # Check if there is a file that ends with autolab.nox
    for file_endings in ['Autolab_ocp.nox', 'Autolab_ocp.json', 'Autolab_ocp_configuration.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1


def test_send_measurment_cp():
    """ Test if the cp experiment is added to the orchestrator. """
    sequence = dict(soe=['autolab/measure_0'],
                    params={'measure_0': {'procedure':'cp',
                                'plot_type':'tCV',
                                'parse_instruction': json.dumps(['recordsignal']),
                                'save_dir':'mischbares/tests',
                                'setpoints': json.dumps({'applycurrent':\
                                            {'Setpoint value': 0.00001},
                                            'recordsignal': {'Duration (s)': 5,\
                                            'Interval time (s)': 0.5}}),
                                'current_range': '10mA',
                                'on_off_status':'off',
                                'optional_name': 'cp',
                                'measure_at_ocp': True}},
                    meta={})

    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    # wait for the measurement to finish
    time.sleep(30)
    # Check if there is a file that ends with autolab.nox
    for file_endings in ['Autolab_cp.nox', 'Autolab_cp.json', 'Autolab_cp_configuration.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_send_measurment_ca():
    """ Test if the ca experiment is added to the orchestrator. """
    sequence = dict(soe=['autolab/measure_0'],
                    params={'measure_0': {'procedure':'ca',
                                'plot_type':'tCV',
                                'parse_instruction': json.dumps(['recordsignal']),
                                'save_dir':'mischbares/tests',
                                'setpoints': json.dumps({'applypotential': {'Setpoint value': 0.7},\
                                            'recordsignal': {'Duration (s)': 5,\
                                            'Interval time (s)': 0.5}}),
                                'current_range': '10mA',
                                'on_off_status':'off',
                                'optional_name': 'ca',
                                'measure_at_ocp': True}},
                    meta={})

    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    # wait for the measurement to finish
    time.sleep(50)
    # Check if there is a file that ends with autolab.nox
    for file_endings in ['Autolab_ca.nox', 'Autolab_ca.json', 'Autolab_ca_configuration.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_send_measurment_eis():
    """ Test if the eis experiment is added to the orchestrator. """
    sequence = dict(soe=['autolab/measure_0'],
                    params={'measure_0': {'procedure':'eis',
                                'plot_type':'impedance',
                                'parse_instruction':
                                    json.dumps(['FIAMeasPotentiostatic', 'FIAMeasurement']),
                                'save_dir':'mischbares/tests',
                                'setpoints': json.dumps({}),
                                'current_range': '10mA',
                                'on_off_status':'off',
                                'optional_name': 'eis',
                                'measure_at_ocp': True}},
                    meta={})
    #json.dumps({'Set potential': {'Setpoint value': 0.1}}),
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    # wait for the measurement to finish
    time.sleep(120)
    # Check if there is a file that ends with autolab.nox
    for file_endings in ['Autolab_eis.nox', 'Autolab_eis.json', 'Autolab_eis_configuration.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1


def test_send_measurment_cvcc():
    """ Test a seqeunce of two experiments to the orchestrator. """
    sequence = dict(soe=['autolab/measure_0', 'autolab/measure_1'],
                    params={'measure_0': {'procedure':'ca','plot_type':'tCV',
                                'parse_instruction': json.dumps(['recordsignal']),
                                'save_dir':'mischbares/tests',
                                'setpoints': json.dumps({'applypotential': {'Setpoint value': 0.7},
                                            'recordsignal': {'Duration (s)': 5,
                                            'Interval time (s)': 0.5}}),
                                            'current_range': '10mA','on_off_status':'off',
                                            'optional_name': 'ca', 'measure_at_ocp': True},
                            'measure_1': {'procedure':'cp','plot_type':'tCV',
                                            'parse_instruction': json.dumps(['recordsignal']),
                                            'save_dir':'mischbares/tests',
                                            'setpoints': json.dumps({'applycurrent':
                                                {'Setpoint value': 0.00001},'recordsignal':
                                                {'Duration (s)': 5,'Interval time (s)': 0.5}}),
                                'current_range': '10mA','on_off_status':'off',
                                'optional_name': 'cp','measure_at_ocp': True}},
                    meta={})

    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
    # wait for the measurement to finish
    time.sleep(100)
    # Check if there is a file that ends with autolab.nox
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1


def test_finish_orchestrator():
    """ Test if the experiment is added to the orchestrator. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/finish'],
                  params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
