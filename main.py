"""Main module."""
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
    for i in range(1, 2):
        #create an experiment object and get the experiment id
        #TODO create a procedure object with the measurement id and the experiment id and give it to the function
        _, _, sequence = AutolabProcedures(measurement_num=i,
                                save_dir=r"C:\Users\LaborRatte23-3\Documents\repositories\test_data_mischbares",
                                user_id=users.user_id).eis_cv_staircase_measurement(start_value=0,
                                                                                upper_vortex=0.1,
                                                                                lower_vortex=-0.1,
                                                                                stop_value=0.001,
                                                                                measure_at_ocp=True)
        params = dict(experiment=json.dumps(sequence),thread=0)
        requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment", params=params, timeout=None).json()
        time.sleep(300)

    end_orchestrator_experimentation()



# main function
if __name__ == "__main__":
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
    main()
    for proc in processes:
        proc.kill()
