""" Test file for the autolab procedures """
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
from mischbares.procedures.autolab_procedures import AutolabProcedures


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
    # shutil.rmtree('mischbares/tests/data', ignore_errors=True)
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


def test_ocp_measurement():
    """ Test if the ocp procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).ocp_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(20)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_ocp.json')]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_ca_measurement():
    """ Test if the ca procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).ca_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(30)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_ca.json')]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_cp_measurement():
    """ Test if the cp procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).cp_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(50)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_cp.json')]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_measurement_with_ocp():
    """ Test if the eis procedure works at the ocp potential.
    """
    autolab_procedure = AutolabProcedures(measurement_num=0)
    _, _, sequence = autolab_procedure.eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)
    print("Starting EIS measurement at OCP")
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(120)
    print("EIS measurement at OCP finished")
    data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_eis.json')]
    assert len(data_name) == 1
    # check if the data is properly recorded or not
    with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
        data = json.load(f)
    assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.0

    shutil.rmtree('mischbares/tests/data', ignore_errors=True)
    print("data removed")


def test_eis_measurement_without_ocp():
    """ Test if the eis procedure works at the defined potential.
    """

    autolab_procedure = AutolabProcedures(measurement_num=0)
    _, _, sequence = autolab_procedure.eis_measurement(apply_potential = 0.1, measure_at_ocp=False)
    parameters = dict(experiment=json.dumps(sequence),thread=0)
    print("Starting EIS measurement with no OCP")
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(120)
    print("EIS measurement with no OCP finished")
    data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_eis.json')]
    assert len(data_name) == 1
    # check if the data is properly recorded or not
    with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
        data = json.load(f)
    assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_ca_eis_measurement(): #9
    """ Test if the ca & eis procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).ca_eis_measurement(eis_potential=0.1,
                                                                        eis_measure_at_ocp=False)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(150)
    for file_endings in ['Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1
        # check if the data is properly recorded or not
        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_ca_measurement():
    """ Test if the eis & ca procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).eis_ca_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(150)
    for file_endings in ['Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.0
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_cp_eis_measurement(): #11
    """ Test if the cp & eis procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).cp_eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(150)
    for file_endings in ['Autolab_cp.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.0
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_cp_measurement():
    """ Test if the eis & cp procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).eis_cp_measurement(eis_potential=0.2,
                                                                        eis_measure_at_ocp=False)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(150)
    for file_endings in ['Autolab_cp.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.2
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_cp_ca_measurement(): #13
    """ Test if the cp & ca procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).cp_ca_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(90)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_ca_cp_measurement():
    """ Test if the ca & cp procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).ca_cp_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(90)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_cp_ca_eis_measurement(): #15
    """ Test if the cp & ca & eis procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).cp_ca_eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(210)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.0
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_ca_cp_eis_measurement():
    """ Test if the ca & cp & eis procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).ca_cp_eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(200)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.0
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_ca_cp_measurement(): #17
    """ Test if the eis & ca & cp procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).eis_ca_cp_measurement(eis_potential=0.2,
                                                                         eis_measure_at_ocp=False)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(200)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.2
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_cp_ca_measurement():
    """ Test if the eis & cp & ca procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).eis_cp_ca_measurement(eis_potential=0.2,
                                                                         eis_measure_at_ocp=False)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(180)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1

        if file_endings == "Autolab_eis.json":
            with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.2
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_ca_cp_eis_measurement(): #19
    """ Test if the eis & ca & cp & eis procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).eis_ca_cp_eis_measurement(
                                        first_eis_measure_at_ocp=False, first_eis_potential=0.2)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(250)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        if file_endings == 'Autolab_eis.json':
            data_name = [f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]
            assert len(data_name) == 2
            data_time = [os.path.getmtime(os.path.join('mischbares/tests/data', file))\
                        for file in data_name]
            # get the index of the file with the lowest time stamp
            index = data_time.index(min(data_time))

            with open(os.path.join('mischbares/tests/data', data_name[index]),
                    encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.2

        else:
            assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_eis_cp_ca_eis_measurement():
    """ Test if the eis & cp & ca & eis procedure works.
    """
    _, _, sequence = AutolabProcedures(measurement_num=0).eis_cp_ca_eis_measurement(
                                        first_eis_measure_at_ocp=False, first_eis_potential=0.2)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(250)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        if file_endings == 'Autolab_eis.json':
            data_name = [f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]
            assert len(data_name) == 2
            data_time = [os.path.getmtime(os.path.join('mischbares/tests/data', file))\
                        for file in data_name]
            # get the index of the file with the latest time stamp
            index = data_time.index(max(data_time))

            with open(os.path.join('mischbares/tests/data', data_name[index]),
                      encoding="utf-8") as f:
                data = json.load(f)
            assert round(data["FIAMeasurement"]["Potential (DC)"][0], 1) == 0.0

        else:
            assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)


def test_finish_orchestrator():
    """ Test if the experiment is added to the orchestrator. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/finish'],
                  params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
