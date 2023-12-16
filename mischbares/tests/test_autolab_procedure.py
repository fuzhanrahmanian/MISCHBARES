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

@pytest.fixture
def clean_data_directory():
    # Setup code can go here (if any)
    yield
    try:
        if os.path.exists('mischbares/tests/data'):
            shutil.rmtree('mischbares/tests/data', ignore_errors=True)
            print("2 Cleanup successful: mischbares/tests/data directory removed.")
        else:
            print("2 Cleanup skipped: mischbares/tests/data directory does not exist.")
    except Exception as e:
        print(f"Cleanup failed: {e}")

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


def test_ocp_measurement(clean_data_directory):
    """ Test if the ocp procedure works.
    """
    print("Starting OCP measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                       electrode_area=6.2, concentration_of_active_material=6.2,
                                       mass_of_active_material=6.2).ocp_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(30)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_ocp.json')]) == 1



def test_ca_measurement(clean_data_directory):
    """ Test if the ca procedure works.
    """
    print("Starting CA measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).ca_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(30)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_ca.json')]) == 1



def test_cp_measurement(clean_data_directory):
    """ Test if the cp procedure works.
    """
    print("Starting CP measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cp_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(50)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_cp.json')]) == 1



def test_cv_measurement(clean_data_directory):
    """ Test if the cv procedure works.
    """
    print("Starting CV measurement test")
    _,_, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cv_staircase_measurement(
                                        start_value=0, upper_vortex=0.1, lower_vortex=-0.1, stop_value=0.0)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(50)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_cv_staircase.json')]) == 1


def test_cv_measurement_with_ocp(clean_data_directory):
    """ Test if the cv procedure works.
    """
    print("Starting CV with OCP measurement test")
    _,_, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cv_staircase_measurement(
                                        start_value=0, upper_vortex=0.1, lower_vortex=-0.1, measure_at_ocp=True, stop_value=0.0)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(50)
    assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_cv_staircase.json')]) == 1



def test_eis_measurement_with_ocp(clean_data_directory):
    """ Test if the eis procedure works at the ocp potential.
    """
    print("Starting EIS measurement at OCP")
    autolab_procedure = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2)
    _, _, sequence = autolab_procedure.eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(120)
    data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith('Autolab_eis.json')]
    assert len(data_name) == 1
    # check if the data is properly recorded or not
    with open(os.path.join('mischbares/tests/data', data_name[0]), encoding="utf-8") as f:
        data = json.load(f)



def test_eis_measurement_without_ocp(clean_data_directory):
    """ Test if the eis procedure works at the defined potential.
    """
    print("Starting EIS measurement test with no OCP")
    autolab_procedure = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2)
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




def test_ca_eis_measurement(clean_data_directory): #9
    """ Test if the ca & eis procedure works.
    """
    print("Starting CA+EIS measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).ca_eis_measurement(eis_potential=0.1,
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


def test_eis_ca_measurement(clean_data_directory):
    """ Test if the eis & ca procedure works.
    """
    print("Starting EIS+CA measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_ca_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(150)
    for file_endings in ['Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1


def test_cp_eis_measurement(clean_data_directory): #11
    """ Test if the cp & eis procedure works.
    """
    print("Starting CP+EIS measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cp_eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(150)
    for file_endings in ['Autolab_cp.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1


def test_cv_eis(clean_data_directory):
    """ Test if the cv procedure works.
    """
    print("Starting CV+EIS measurement test")
    _,_, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cv_stairstep_eis_measurement(
                                        start_value=0, upper_vortex=0.1, lower_vortex=-0.1,
                                        eis_measure_at_ocp=True, stop_value=0.0)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(200)
    for file_endings in ['Autolab_eis.json', 'Autolab_cv_staircase.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]
        assert len(data_name) == 1


def test_eis_cv(clean_data_directory):
    """ Test if the cv procedure works.
    """
    print("Starting EIS+CV measurement test")
    _,_, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_cv_staircase_measurement(
                                        start_value=0, upper_vortex=0.1, lower_vortex=-0.1,
                                        measure_at_ocp=True, stop_value=0.0)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(200)
    for file_endings in ['Autolab_eis.json', 'Autolab_cv_staircase.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]
        assert len(data_name) == 1



def test_eis_cp_measurement(clean_data_directory):
    """ Test if the eis & cp procedure works.
    """
    print("Starting EIS+CP measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_cp_measurement(eis_potential=0.2,
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


def test_cp_ca_measurement(clean_data_directory): #13
    """ Test if the cp & ca procedure works.
    """
    print("Starting CP+CA measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cp_ca_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(90)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]) == 1



def test_ca_cp_measurement(clean_data_directory):
    """ Test if the ca & cp procedure works.
    """
    print("Starting CA+CP measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).ca_cp_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(90)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json']:
        assert len([f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]) == 1



def test_cp_ca_eis_measurement(clean_data_directory): #15
    """ Test if the cp & ca & eis procedure works.
    """
    print("Starting CP+CA+EIS measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cp_ca_eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(210)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1


def test_ca_cp_eis_measurement(clean_data_directory):
    """ Test if the ca & cp & eis procedure works.
    """
    print("Starting CA+CP+EIS measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).ca_cp_eis_measurement()
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(200)
    for file_endings in ['Autolab_cp.json', 'Autolab_ca.json', 'Autolab_eis.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                if f.endswith(file_endings)]
        assert len(data_name) == 1


def test_eis_cv_eis(clean_data_directory):
    """ Test if the cv procedure works.
    """
    print("Starting EIS+CV+EIS measurement test")
    _,_, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_cv_staircase_eis_measurement(
                                        start_value=0, upper_vortex=0.1, lower_vortex=-0.1,
                                        first_eis_measure_at_ocp=True, second_eis_measure_at_ocp=True, stop_value=0.0)
    parameters = dict(experiment=json.dumps(sequence),thread=0)

    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=parameters, timeout=None)
    assert response.status_code == 200
    time.sleep(200)
    for file_endings in ['Autolab_eis.json', 'Autolab_cv_staircase.json']:
        data_name = [f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]
        if file_endings == 'Autolab_eis.json':
            assert len(data_name) == 2
        else:
            assert len(data_name) == 1



def test_eis_ca_cp_measurement(clean_data_directory): #17
    """ Test if the eis & ca & cp procedure works.
    """
    print("Starting EIS+CA+CP measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_ca_cp_measurement(eis_potential=0.2,
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



def test_eis_cp_ca_measurement(clean_data_directory):
    """ Test if the eis & cp & ca procedure works.
    """
    print("Starting EIS+CP+CA measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_cp_ca_measurement(eis_potential=0.2,
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



def test_eis_ca_cp_eis_measurement(clean_data_directory): #19
    """ Test if the eis & ca & cp & eis procedure works.
    """
    print("Starting EIS+CA+CP+EIS measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_ca_cp_eis_measurement(
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

        else:
            assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1



def test_eis_cp_ca_eis_measurement(clean_data_directory):
    """ Test if the eis & cp & ca & eis procedure works.
    """
    print("Starting EIS+CP+CA+EIS measurement test")
    _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).eis_cp_ca_eis_measurement(
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
        else:
            assert len([f for f in os.listdir('mischbares/tests/data')
                    if f.endswith(file_endings)]) == 1



def test_finish_orchestrator(clean_data_directory):
    """ Test if the experiment is added to the orchestrator. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/finish'],
                  params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None)
    assert response.status_code == 200
