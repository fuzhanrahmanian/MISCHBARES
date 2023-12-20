"""Main module."""
import os
import requests
import time
import shutil
import json
import subprocess
import inspect
from multiprocessing import Process

# postgres

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

EXP_CONFIGS = ["batch_config", "experiment_config", "general_config"]


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


def banana_instance():
    """Start the server and action in a separate processes."""
    processes = [Process(target=run_server_hamilton),
                 Process(target=run_action_hamilton),
                 Process(target=run_lang_server),
                 Process(target=run_lang_action),
                 Process(target=run_server),
                 Process(target=run_action),
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
    shutil.rmtree('mischbares/tests/data', ignore_errors=True)
    shutil.rmtree('data/test', ignore_errors=True)


def start_orchestrator_experimentation():
    """ Intantiate the orchestrator scheduler. """
    # Assuming the start fucniotns works
    sequence = dict(soe=['orchestrator/start'],
                  params={'start': {'collectionkey': "qc_drop_test"}}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None).json()


def end_orchestrator_experimentation():
    """ Intantiate the orchestrator scheduler.
    """
    sequence = dict(soe=['orchestrator/finish'], params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
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
# def main():
#     # Check if ["batch_config", experiment_config, general_config] exists in the folder saved_config

#     # """Main function."""
#     log.info("Start to do one experiment")
#     proc_values = {
#     "ocp": [20,100,0.0], #duration, interval_time, ocp_potential,
#     #"cv_staircase": [0.4, 1.5, -1, 0.005, 2, 0.1, 0.001],
#     #"ca": [20, 1, 0.5, 0.0001, 0.2], #duration, applied_potential, interval_time, capacity, diffusion_coefficient
#     # "cp": [21, 2e-6, 0.6, 0.0002],
#     # "eis": [0.2, 1, 1, 10, 10000, 0.2, 2e-6, "R0_R1_C1"]
# }
#     #TODO log in the user and connect to the database
#     # Check it user with "test_username" exists, if not create it
#     users = Users()
#     if users.get_user("test_username") is None:
#         users.register_user("test_username", "test_fisrt_name", "test_last_name", "test_email",
#                             "test_password")
#     users.login_user("test_username", "test_password")
#     users.close()

#     # start the orchestrator
#     start_orchestrator_experimentation()
#     curr = [0.0001, 0.0005]

#     amount_of_pump = [0, 600]


#     for i in range(1, 3):

#         #requests.get(f"http://{lang_host_url}:{lang_port_action}/lang/moveWaste", timeout=None)
#         soe = ['lang/moveWaste_0', 'hamilton/pumpR_0']
#         params = {'moveWaste_0': {'x_pos': 0, 'y_pos':0, 'z_pos':0},
#                   'pumpR_0':{'volume': amount_of_pump[i-1]}}
#         sequence = dict(soe=soe,params=params,meta={})
#         parameters = dict(experiment=json.dumps(sequence),thread=0)
#         #create an experiment object and get the experiment id
#         #TODO create a procedure object with the measurement id and the experiment id and give it to the function
#         # _, _, sequence = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
#         #                                 electrode_area=6.2, concentration_of_active_material=6.2,
#         #                                 mass_of_active_material=6.2).cp_measurement(apply_current=curr[i-1])
#         # _, _, sequence = AutolabProcedures(measurement_num=i,
#         #                        save_dir=r"C:\Users\LaborRatte23-3\Documents\repositories\test_data_mischbares",
#         #                                 number_of_electrons=2, electrode_area=6.2, concentration_of_active_material=6.2,
#         #                                 mass_of_active_material=6.2,
#         #                        user_id=users.user_id, material="LFP").ocp_measurement()
#         # params = dict(experiment=json.dumps(sequence),thread=0)
#         requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment", params=parameters,
#                       timeout=None).json()
#         #input("Press Enter to continue...")


#     # Run a while loop for 200 seconds
#     time_in = time.time()
#     time_out = 200*60

#     while True:
#         # check the orchestrator is on pause every 10 seconds

#         response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/getStatus", timeout=None).json()

#         if response['0']['status'] == "paused":
#             end_orchestrator_experimentation()
#             break

#         # check if the time is out
#         if time.time() - time_in > time_out:
#             end_orchestrator_experimentation()
#             break
#         # wait for 10 seconds
#         time.sleep(10)


def main(exp_config):
    # Check if ["batch_config", experiment_config, general_config] exists in the folder saved_config

    # """Main function."""
    log.info("Start to do one experiment")
    #TODO log in the user and connect to the database
    # THIS is just a placeholder
    user_id = 2
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
                    user_id=user_id,
                    number_of_electrons=exp_config.general_configs["number_of_electrons"],
                    electrode_area=exp_config.general_configs["electrode_area"],
                    concentration_of_active_material=\
                        exp_config.general_configs["concentration_of_active_material"],
                    mass_of_active_material=exp_config.general_configs["mass_of_active_material"])

            for method_name, args in exp_config.batch_config[f"batch_{batch_num}"][f"experiment_{exp_num}"]:
                soe_autolab, params_autolab, _ =\
                    call_method_with_dict(autolab_instantiation, method_name, args)
            _, _, sequence = seq_exp.perfom_sequential_experiment(soe_autolab=soe_autolab,
                            params_autolab=params_autolab,
                            current_range_autolab= autolab_instantiation.current_current_range,
                            sample_position=exp_config.general_configs["motor_pos"][motor_pos_idx])
            motor_pos_idx += 1
            params = dict(experiment=json.dumps(sequence),thread=0)
            requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                                params=params, timeout=None).json()

    # Run a while loop for 200 seconds
    time_in = time.time()
    time_out = 200*60

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
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False


def wait_for_servers_to_be_ready():
    # TODO : check if others need it or not
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
    print("Starting visualizer...")
    time.sleep(15)
    input("Press Enter to start the experiment...")
    main(exp_config)
    for proc in processes:
        proc.kill()



