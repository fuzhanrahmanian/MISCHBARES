"""Main module."""
import subprocess
import os
from datetime import datetime
import requests
import time
import shutil
import json
import argparse
from multiprocessing import Process

# postgres
import psycopg2
from mischbares.logger import logger
from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.orchestrator import orchestrator
from mischbares.config.main_config import config
from mischbares.procedures.autolab_procedures import AutolabProcedures

from mischbares.db.database import Database
from mischbares.db.user import Users
from mischbares.db.experiment import Experiments
from mischbares.db.measurement import Measurements
from mischbares.db.procedure import Procedure

log = logger.setup_applevel_logger(file_name="mischbares.log")

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

def start_bokeh_visualizer():
    visualizer_path = os.path.join('mischbares', 'visualizer', 'autolab_visualizer.py')
    subprocess.Popen(["bokeh", "serve", visualizer_path, "--show"])


def banana_instance():
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


def start_orchestrator_experimentation():
    """ Intantiate the orchestrator scheduler. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/start'],
                  params={'start': {'collectionkey': "db_test"}}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None).json()




def end_orchestrator_experimentation():
    sequence = dict(soe=['orchestrator/finish'], params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None).json()


def main():
    """Main function."""
    log.info("Start to do one experiment")
    proc_values = {
    "ocp": [20,100,0.0], #duration, interval_time, ocp_potential,
    #"cv_staircase": [0.4, 1.5, -1, 0.005, 2, 0.1, 0.001],
    #"ca": [20, 1, 0.5, 0.0001, 0.2], #duration, applied_potential, interval_time, capacity, diffusion_coefficient
    # "cp": [21, 2e-6, 0.6, 0.0002],
    # "eis": [0.2, 1, 1, 10, 10000, 0.2, 2e-6, "R0_R1_C1"]
}
    #TODO log in the user and connect to the database
    # Check it user with "test_username" exists, if not create it
    users = Users()
    if users.get_user("test_username") is None:
        users.register_user("test_username", "test_fisrt_name", "test_last_name", "test_email",
                            "test_password")
    users.login_user("test_username", "test_password")
    users.close()

    # start the orchestrator
    start_orchestrator_experimentation()
    curr = [0.0001, 0.0005]
    for i in range(1, 3):
        #create an experiment object and get the experiment id
        #TODO create a procedure object with the measurement id and the experiment id and give it to the function
        _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2).cp_measurement(apply_current=curr[i-1])
        # _, _, sequence = AutolabProcedures(measurement_num=i,
        #                        save_dir=r"C:\Users\LaborRatte23-3\Documents\repositories\test_data_mischbares",
        #                                 number_of_electrons=2, electrode_area=6.2, concentration_of_active_material=6.2,
        #                                 mass_of_active_material=6.2,
        #                        user_id=users.user_id, material="LFP").ocp_measurement()
        params = dict(experiment=json.dumps(sequence),thread=0)
        requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment", params=params, timeout=None).json()
        
        # Wait for input from the user to continue
        input("Press Enter to finish...")

    end_orchestrator_experimentation()

def is_server_ready(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def wait_for_servers_to_be_ready():
    server_urls = [f"http://{host_url}:{port_server}/health",
                   f"http://{host_url}:{port_action}/health",
                   f"http://{host_url}:{port_orchestrator}/health"]

    while True:
        if all(is_server_ready(url) for url in server_urls):
            break
        print("Waiting for servers to be ready...")
        time.sleep(1)

# main function
if __name__ == "__main__":
    processes = [Process(target=run_server),
                 Process(target=run_action),
                 Process(target=run_orchestrator)]

    for proc in processes:
        proc.start()
    wait_for_servers_to_be_ready()
    # Start the visualizer in a separate process
    visualizer_process = Process(target=start_bokeh_visualizer)
    visualizer_process.start()
    print("Starting visualizer...")
    time.sleep(15)
    main()
    for proc in processes:
        proc.kill()
