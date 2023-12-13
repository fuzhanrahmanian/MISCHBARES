"""Main module."""
import requests
import time
import shutil
import json
from multiprocessing import Process

# postgres
import psycopg2
from mischbares.logger import logger
from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.orchestrator import orchestrator
from mischbares.config.main_config import config
from mischbares.procedures.autolab_procedures import AutolabProcedures

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

    #TODO log in the user and connect to the database

    # start the orchestrator
    start_orchestrator_experimentation()
    for i in range(1, 2):
        #TODO create an experiment object and get the experiment id
        #TODO create a measurement object and get the measurement id
        #TODO create a procedure object with the measurement id and the experiment id and give it to the function
        _, _, sequence = AutolabProcedures(measurement_num=i, save_dir=r"C:\Users\SDC_1\Documents\repositories\test_data_mischbares").ocp_measurement()
        params = dict(experiment=json.dumps(sequence),thread=0)
        requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                                params=params, timeout=None).json()

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
