"""Main module."""
import subprocess
import os
import requests
import time
import shutil
import json
from multiprocessing import Process

# postgres

from mischbares.logger import logger
from mischbares.action import autolab_action
from mischbares.server import autolab_server
from mischbares.orchestrator import orchestrator
from mischbares.config.main_config import config

from mischbares.utils.utils import send_to_telegram

from mischbares.db.user import Users

from mischbares.server import lang_server
from mischbares.action import lang_action

from mischbares.action import hamilton_action
from mischbares.server import hamilton_server

from mischbares.procedures.autolab_procedures import AutolabProcedures
import mischbares.procedures.sequential_procedures as seq_exp

log = logger.setup_applevel_logger(file_name="mischbares.log")

host_url = config['servers']['autolab']['host']
port_action = config['servers']['autolab']['port']
port_server = config['servers']['autolabDriver']['port']
port_orchestrator = config['servers']['orchestrator']['port']

################################################################################
# in the config should be paased: "test_username", "test_fisrt_name", "test_last_name", "test_email",
#                                   "test_password",  material="LFP", user_id=2, number_of_electrons=2,
                        # electrode_area=6.2, concentration_of_active_material=6.2,
                        # mass_of_active_material=6.2
                       # motor_pos = [(0,0,0), (1,1,0), (1,1,0), (2,2,0)]
# dummy config :
# how many batch of experiment you want?
num_batch = 1

# how many experiment in each batch and what procedure should be there
number_exp_in_each_batch = 4
duration = [i for i in range(10, 30, 5)]

for batch in num_batch: # in each batch they are the same experiment
    for exp in number_exp_in_each_batch:
        if batch == 1:
            experimental_info = {f"batch_{batch}": {exp: \
                {'ocp_measurement':{'measurement_duration':duration[number_exp_in_each_batch]},
                 'motor_pos': motor_pos[batch][exp]}}} # key is the number of experiment and value is the auto type procedure

        if batch == 2:
            experimental_info = {f"batch_{batch}": {exp: \
                {'cv_staircase_measurement':{'start_value':0, 'upper_vortex': 0.2,
                                             'lower_vortex': -0.2, 'stop_value': 0.1}}}}
total_number_of_experiment = num_batch * number_exp_in_each_batch # can be different though : just the summation basically
###############################################################################
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
    sequence = dict(soe=['orchestrator/finish'], params={'finish': None}, meta={})
    params = dict(experiment=json.dumps(sequence),thread=0)
    requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment",
                            params=params, timeout=None).json()
    send_to_telegram(message=f"Experiment finished: \n Closing experiment", message_type="info")

def main(experimental_info, configuration_experiment, total_number_of_experiment=1, db_identification = None):
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

    #amount_of_pump = [0, 600]
    
    i = 1
    for batch in batch_num:
        for exp in experiment_num :
        #requests.get(f"http://{lang_host_url}:{lang_port_action}/lang/moveWaste", timeout=None)
        #soe = ['lang/moveWaste_0', 'hamilton/pumpR_0']
        #params = {'moveWaste_0': {'x_pos': 0, 'y_pos':0, 'z_pos':0},
        #          'pumpR_0':{'volume': amount_of_pump[i-1]}}
        #sequence = dict(soe=soe,params=params,meta={})
        #parameters = dict(experiment=json.dumps(sequence),thread=0)
        #create an experiment object and get the experiment id
        #TODO create a procedure object with the measurement id and the experiment id and give it to the function
        # configuration_experiment[material], ...
        autolab_initialization = AutolabProcedures(measurement_num=0, material="LFP", user_id=2, number_of_electrons=2,
                                        electrode_area=6.2, concentration_of_active_material=6.2,
                                        mass_of_active_material=6.2)
        #name_of_autolab_procedure = experimental_info[f'batch_{batch}'][f'exp_{exp}']
        #procedure = getattr(name_of_autolab_procedure)
        soe, params, sequence = autolab_initialization.procedure  #cp_measurement(apply_current=curr[i-1])
        if sequence:
            _,_,sequence = seq_exp.perfom_sequential_experiment(soe, params,
                autolab_initialization.current_range_autolab,
                experimental_info[f'batch_{batch}'][f'exp_{exp}']['motorpos'])
        # _, _, sequence = AutolabProcedures(measurement_num=i,
        #                        save_dir=r"C:\Users\LaborRatte23-3\Documents\repositories\test_data_mischbares",
        #                                 number_of_electrons=2, electrode_area=6.2, concentration_of_active_material=6.2,
        #                                 mass_of_active_material=6.2,
        #                        user_id=users.user_id, material="LFP").ocp_measurement()
        params = dict(experiment=json.dumps(sequence),thread=0)
        requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/addExperiment", params=params,
                      timeout=None).json()
        i +=1
        #input("Press Enter to continue...")


    # Run a while loop for 200 seconds
    start_time = time.time()
    time_in = time.time()
    time_out = 200*60

    while True:
        # check the orchestrator is on pause every 10 seconds

        response = requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/getStatus", timeout=None).json()

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
    main()
    for proc in processes:
        proc.kill()



