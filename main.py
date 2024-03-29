"""Main module."""
import os
import requests
import time
import shutil
import json
import subprocess
import inspect
from multiprocessing import Process
import sys
from flask import jsonify

from mischbares.logger import logger
from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.orchestrator import orchestrator
from mischbares.config.parse_experiment_configs import ParserExperimentConfigs
from mischbares.config.main_config import config
from mischbares.procedures.autolab_procedures import AutolabProcedures
import mischbares.procedures.sequential_procedures as seq_exp

from mischbares.utils.utils import send_to_telegram

from mischbares.db.user import Users

from mischbares.server import lang_server
from mischbares.action import lang_action

from mischbares.action import hamilton_action
from mischbares.server import hamilton_server


log = logger.setup_applevel_logger(file_name="mischbares.log")

host_url = config['servers']['autolab']['host']
port_action = config['servers']['autolab']['port']
port_server = config['servers']['autolabDriver']['port']
port_orchestrator = config['servers']['orchestrator']['port']

EXP_CONFIGS = ["batch_config.json", "experiment_config.json", "general_config.json"]


def run_lang_action():
    """Start the Autolab server."""
    lang_action.main()


def run_lang_server():
    """Start the Autolab server."""
    lang_server.main()


def run_action_hamilton():
    """Start the Autolab server."""
    hamilton_action.main()


def run_server_hamilton():
    """Start the Autolab server."""
    hamilton_server.main()


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


def start_orchestrator_experimentation():
    """ Intantiate the orchestrator scheduler. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/start'],
                  params={'start': {'collectionkey': "test"}}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None).json()


def end_orchestrator_experimentation():
    """
    Ends the orchestrator experimentation by sending a request to the orchestrator API
    and sending a message to Telegram.

    This function constructs a sequence dictionary, converts it to JSON, and sends it
    as a parameter in a POST request to the orchestrator API. It also sends a message
    to Telegram with information about the finished experiment.

    Args:
        None

    Returns:
        None
    """
    sequence = dict(soe=['orchestrator/finish'], params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence), thread=0)
    requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                  params=params, timeout=None).json()
    send_to_telegram(message=f"Experiment finished: \n Closing experiment", message_type="info")


def call_method_with_dict(obj, method_name, arg_dict):
    """Call a method with a dictionary of arguments.

    Args:
        obj (object): Object containing the method.
        method_name (str): Name of the method.
        arg_dict (dict): Dictionary of arguments.

    Returns:
        object: Return value of the method.
    """
    # Check if the method exists in the object
    if hasattr(obj, method_name):
        method = getattr(obj, method_name)
    else:
        raise ValueError(f"Method {method_name} not found in the object.")

    # Get the signature of the method
    sig = inspect.signature(method)

    # Prepare arguments, converting types if necessary
    args = {}
    for param in sig.parameters.values():
        if param.name in arg_dict:
            # Convert the type if necessary
            value = arg_dict[param.name]
            if param.annotation != inspect.Parameter.empty and param.annotation is not type(value):
                try:
                    value = param.annotation(value)
                except ValueError:
                    raise ValueError(f"Cannot convert parameter {param.name} to {param.annotation}")

            args[param.name] = value

    # Call the method with the arguments
    return method(**args)


def main(exp_config):
    # """Main function."""
    global USER_ID
    # get total number of batches and the number of experiments per batch
    num_batches = exp_config.experiment_configs["num_of_batch"]
    num_experiments = exp_config.experiment_configs["num_of_experiment_in_each_batch"]
    # start the orchestrator
    start_orchestrator_experimentation()
    motor_pos_idx = 0
    for batch_num in range(num_batches):

        for exp_num in range(num_experiments):
            autolab_instantiation =\
                AutolabProcedures(measurement_num=0,
                    material=exp_config.general_configs["material"],
                    user_id=USER_ID,
                    number_of_electrons=exp_config.general_configs["number_of_electrons"],
                    electrode_area=exp_config.general_configs["electrode_area"],
                    concentration_of_active_material=\
                        exp_config.general_configs["concentration_of_active_material"],
                    mass_of_active_material=exp_config.general_configs["mass_of_active_material"],
                    current_range="1µA")
            # soe = ['lang/moveWaste_0', 'hamilton/pumpR_0']
            # params = {'moveWaste_0': {'x_pos':0, 'y_pos':0, 'z_pos':0},
            #             'pumpR_0': {'volume':700}}
            # sequence = dict(soe=soe, params=params, meta={})
            for method_name, args in exp_config.batch_configs[f"batch_{batch_num+1}"][f"experiment_{exp_num+1}"].items():
               soe_autolab, params_autolab, _ =\
                   call_method_with_dict(autolab_instantiation, method_name, args)
            _, _, sequence = seq_exp.perfom_sequential_experiment(soe_autolab=soe_autolab,
                            params_autolab=params_autolab,
                            current_range_autolab= autolab_instantiation.current_range,
                            sample_position=exp_config.general_configs["motor_pos"][motor_pos_idx])
            motor_pos_idx += 1
            params = dict(experiment=json.dumps(sequence),thread=0)
            requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                                params=params, timeout=None).json()

    # Run a while loop for 200 minutes
    time_in = time.time()
    time_out = 30*60

    while True:
        # check the orchestrator is on pause every 10 seconds
        response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/getStatus",
                                 timeout=None).json()

        if response['0']['status'] == "paused":
            end_orchestrator_experimentation()
            break

        # check if the time is out
        if time.time() - time_in > time_out:
            end_orchestrator_experimentation()
            break
        # wait for 10 seconds
        time.sleep(10)


def is_server_ready(url):
    """
    Checks if the server at the given URL is ready.

    Args:
        url (str): The URL of the server to check.

    Returns:
        bool: True if the server is ready and returns a 200 status code, False otherwise.
    """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


import time

def wait_for_servers_to_be_ready():
    """
    Waits for all servers to be ready by periodically checking their health endpoints.

    This function continuously checks the health endpoints of multiple servers until all servers are ready.
    It uses a list of server URLs to check their health status. The function will break out of the loop
    and return when all servers are ready.

    Returns:
        None
    """
    server_urls = [f"http://{host_url}:{port_server}/health",
                    f"http://{host_url}:{port_action}/health",
                    f"http://{host_url}:{port_orchestrator}/health",
                    f"http://{host_url}:{config['servers']['langDriver']['port']}/health",
                    f"http://{host_url}:{config['servers']['lang']['port']}/health",
                    f"http://{host_url}:{config['servers']['hamiltonDriver']['port']}/health",
                    f"http://{host_url}:{config['servers']['hamilton']['port']}/health"]

    while True:
        if all(is_server_ready(url) for url in server_urls):
            break
        log.info("Waiting for servers to be ready...")
        time.sleep(1)



if __name__ == "__main__":
    global USER_ID
    USER_ID = sys.argv[1]
    log.info(f"Running MISCHBARES for user {USER_ID}")
    # Get the first argument from the command line (user id)

    # Check if ["batch_config", "experiment_config", "general_config"] are files in saved_config folder
    # if not log and exit
    for file in ["batch_config.json", "experiment_config.json", "general_config.json"]:
        if not os.path.exists(os.path.join("saved_config", file)):
            log.error(f"{file} does not exist in saved_config folder")
            exit(1)
    # TODO: check the db , if the user exists
    exp_config = ParserExperimentConfigs(general_config=EXP_CONFIGS[2],
                                experiment_config=EXP_CONFIGS[1],
                                batch_config=EXP_CONFIGS[0])
    log.info("Starting servers, drivers and actions...")
    processes = [Process(target=run_server_hamilton),
                 Process(target=run_action_hamilton),
                 Process(target=run_lang_server),
                 Process(target=run_lang_action),
                 Process(target=run_server),
                 Process(target=run_action),
                 Process(target=run_orchestrator)]
    for proc in processes:
        proc.start()
    wait_for_servers_to_be_ready()
    # Start the visualizer in a separate process
    visualizer_process = Process(target=start_bokeh_visualizer)
    visualizer_process.start()
    log.info("Starting visualizer...")
    while not is_server_ready("http://localhost:5006/autolab_visualizer"):
         time.sleep(1)
    input("Press Enter to start the experiment...\n")
    main(exp_config)
    for proc in processes:
        proc.kill()



