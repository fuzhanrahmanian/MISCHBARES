import os
import time
import json
import numpy as np
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests

from mischbares.utils.utils import send_to_telegram
from mischbares.config.main_config import config
from mischbares.logger import logger

SERVERKEY = "lang"
DRIVER_KEY = "langDriver"
DRIVER_URL = f"http://{config['servers'][DRIVER_KEY]['host']}:{config['servers'][DRIVER_KEY]['port']}"

AUTOLAB_HOST = config['servers']['autolab']['host']
AUTOLAB_PORT = config['servers']['autolab']['port']

HAMILTON_HOST = config['servers']['hamilton']['host']
HAMILTON_PORT = config['servers']['hamilton']['port']

log = logger.get_logger("lang_action")

app = FastAPI(title="lang server",
    description="This is a fancy lang motor action server",
    version="1.0.0")

QC_POTENTIAL_LIST = []

class return_class(BaseModel):
    parameters :dict = None
    data: dict = None

@app.get("/health")
def health_check():
    """ health check to see if the server is up and running
    Returns:
        dict: status
    """
    return {"status": "healthy"}

@app.get("/lang/getPos")
def getPos():
    """ get the current position of the lang motor

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    res = requests.get("{}/langDriver/getPos".format(DRIVER_URL)).json()
    retc = return_class(parameters= {}, data=res)
    return retc


@app.get("/lang/moveRel")
def moveRelFar( dx: float, dy: float, dz: float):
    """ move the lang motor relative to the current position

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    requests.get("{}/langDriver/moveRelFar".format(DRIVER_URL), params= {"dx": dx, "dy": dy, "dz": dz}).json()
    retc = return_class(parameters= {"dx": dx, "dy": dy, "dz": dz,'units':{'dx':'mm','dy':'mm','dz':'mm'}},data={})
    return retc


@app.get("/lang/moveDown") #24 is the maximum amount that it can go down (24 - 2(initial) = 22)
def moveDown(dz: float, steps: int, threshold:float=0.20):
    """ move the lang motor down until the force is exceeded
    Args:
        dz (float): distance to move in z direction
        steps (int): maximum steps to move down
        maxForce (float): maximum force to apply
        threshold (float): threshold to stop moving down

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    steps = int(steps)
    breakdown_of_steps = dz / steps
    if breakdown_of_steps > threshold:
        breakdown_of_steps = threshold

    step = 0
    potential_threshold = config["QC"]["lang"]["potential_threshold"]
    contact_established = False
    # create a temporary folder called _temp
    os.makedirs("_temp", exist_ok=True)

    lang_params = dict(procedure='ocp', plot_type='tCV',
                  parse_instruction= json.dumps(['recordsignal']),
                  save_dir= "_temp",
                  setpoints= json.dumps({'recordsignal':
                                        {'Duration (s)': 2}}))

    while step < steps: # TODO: Add QC with the potentiostat to check if the contact is formed
        requests.get("{}/langDriver/moveRelFar".format(DRIVER_URL),
                        params= dict(dx = 0, dy = 0, dz = breakdown_of_steps)).json()
        log.info(f"steps: {step}")
        step += 1
        time.sleep(1)
        # Get potential from autolab
        # just measure if steps is more than steps -3:
        if step > steps - 3:
            response = requests.get(f"http://{AUTOLAB_HOST}:{AUTOLAB_PORT}/autolab/measure",
                                    params=lang_params,
                                    timeout=None)
            potential = _decode_potential(response)
            QC_POTENTIAL_LIST.append(potential)
            if abs(potential) < potential_threshold:
                log.info("Contact established")
                contact_established = True
                break

    if not contact_established:
        for critical_step in range(config["QC"]["lang"]["max_critical_steps"]):
            if abs(potential) > potential_threshold:
                log.warning("No contact established, adding 20 micro-liter of solution")
                # pump 15ml
                params = dict(volume=int(20))
                response = requests.get(f"http://{HAMILTON_HOST}:{HAMILTON_PORT}/hamilton/pumpR", timeout=None,
                                params=params)
                time.sleep(5)
                # Get potential from autolab
                response = requests.get(f"http://{AUTOLAB_HOST}:{AUTOLAB_PORT}/autolab/measure",
                                        params=lang_params,
                                        timeout=None)
                potential = _decode_potential(response)
                QC_POTENTIAL_LIST.append(potential)
                if abs(potential) > potential_threshold:
                    # MoveRelFar by breakdown_of_steps
                    requests.get("{}/langDriver/moveRelFar".format(DRIVER_URL),
                                    params= dict(dx = 0, dy = 0, dz = breakdown_of_steps)).json()
                    time.sleep(1)
                    # Get potential from autolab
                    response = requests.get(f"http://{AUTOLAB_HOST}:{AUTOLAB_PORT}/autolab/measure",
                                            params=lang_params,
                                            timeout=None)
                    potential = _decode_potential(response)
                    QC_POTENTIAL_LIST.append(potential)
            else:
                log.info("Contact established")
                contact_established = True
                break

    if not contact_established:
        time_in = time.time()
        time_out = config["QC"]["lang"]["timeout"]
        send_to_telegram(message=f"No contact established, measuring every 20s for {time_out}s",
                         message_type="info")
        while time.time() - time_in < time_out:
            # measure the potential every 30 seconds
            time.sleep(20)
            # Get potential from autolab
            response = requests.get(f"http://{AUTOLAB_HOST}:{AUTOLAB_PORT}/autolab/measure",
                                    params=lang_params,
                                    timeout=None)
            potential = _decode_potential(response)
            QC_POTENTIAL_LIST.append(potential)
            if abs(potential) < potential_threshold:
                contact_established = True
                send_to_telegram(message="Contact established. Continuing with the experiment",
                                 message_type="info")
                break

    if not contact_established:
        # Pause orchestrator and send a message to telegram
        # move abs to z = 0 and move to home
        requests.get("{}/langDriver/moveRelFar".format(DRIVER_URL),
                        params= dict(dx = 0, dy = 0, dz = -10)).json()
        requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL),
                        params= dict(dx = 0, dy = 0, dz = 0)).json()
        send_to_telegram(message="No contact established. Pausing the experiment. Please check the cell.",
                         message_type="error")
        host_url = config['servers']['orchestrator']['host']
        port_orchestrator = config['servers']['orchestrator']['port']
        requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/pause", timeout=None)


    if step > steps: # TODO: Check if potential is 0. -> Die soon
        log.warning("Force exceeded the max and the force sensor will die soon (RIP)")

    pos = requests.get("{}/langDriver/getPos".format(DRIVER_URL)).json()

    retc = return_class(parameters= {"dz": dz,"steps":steps,
                                    'units':{'dz':'mm'}},
                        data= {'raw':pos, 'res':{
                              'units':{'pos':'mm'}}})
    # Save the QC potential list
    np.savetxt(f"QC_POTENTIAL_LIST_{datetime.now().strftime(('%m-%d-%H-%M'))}.csv",
               QC_POTENTIAL_LIST, delimiter=",")
    return retc

def _decode_potential(response):
    evaluate_potential = eval(response.content.decode("utf-8").replace("null", "None")\
                                .replace("false", "False"))
    evaluate_potential = evaluate_potential['data']['data']['recordsignal']['WE(1).Potential']
    evaluate_potential = np.mean(evaluate_potential)
    return evaluate_potential

@app.get("/lang/moveAbs")
def moveAbsFar(dx: float, dy: float, dz: float):
    """ move the lang motor to the absolute position

    Args:
        dx (float): distance to move in x direction
        dy (float): distance to move in y direction
        dz (float): distance to move in z direction

    Returns:
        retc (return_class): return class with the parameters and the data
    """

    log.info("the x and y position of the next point is {} and {}".format(dx, dy))
    log.info("types are {} and {}".format(type(dx), type(dy)))
    requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL), params= {"dx": dx, "dy": dy, "dz": dz}).json()
    retc = return_class(parameters= {"dx": dx, "dy": dy, "dz": dz,'units':{'dx':'mm','dy':'mm','dz':'mm'}},data={})
    return retc


@app.get("/lang/moveHome")
def moveHome():
    """ move the lang motor to the home position

    Returns:
        retc (return_class): return class with the parameters and the data
    """

    res = requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL),
                       params=dict(dx=config[SERVERKEY]['langAction']['safe_home_pos'][0],
                                   dy=config[SERVERKEY]['langAction']['safe_home_pos'][1],
                                   dz=config[SERVERKEY]['langAction']['safe_home_pos'][2])).json()
    retc = return_class(parameters={},data=res)
    return retc

@app.get("/lang/moveWaste")
def moveWaste(x_pos: float=0, y_pos: float=0, z_pos: float=0): #these three coordinates define the home position. This helps us to align the positions based on the reference point 
    """ move the lang motor to the waste position
    Args:
        x_pos (float): distance to move in x direction
        y_pos (float): distance to move in y direction
        z_pos (float): distance to move in z direction

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    res = requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL),
                       params=dict(dx=x_pos+config[SERVERKEY]['langAction']['safe_waste_pos'][0],
                                    dy=y_pos+config[SERVERKEY]['langAction']['safe_waste_pos'][1],
                                    dz=z_pos+config[SERVERKEY]['langAction']['safe_waste_pos'][2])).json()
    retc = return_class(parameters= {"x": x_pos, "y": y_pos, "z": z_pos,'units':{'x':'mm','y':'mm','z':'mm'}},
                        data=res)
    return retc


@app.get("/lang/moveSample")
def moveToSample(x_pos: float=0, y_pos: float=0, z_pos: float=0):
    """ move the lang motor to the sample position

    Args:
        x_pos (float): distance to move in x direction
        y_pos (float): distance to move in y direction
        z_pos (float): distance to move in z direction

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    res = requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL),
                       params=dict(dx=x_pos+config[SERVERKEY]['langAction']['safe_sample_pos'][0],
                                   dy=y_pos+config[SERVERKEY]['langAction']['safe_sample_pos'][1],
                                   dz=z_pos+config[SERVERKEY]['langAction']['safe_sample_pos'][2])).json()
    retc = return_class(parameters= {"x": x_pos, "y": y_pos, "z": z_pos,'units':{'x':'mm','y':'mm','z':'mm'}},
                        data=res)
    return retc


@app.get("/lang/RemoveDroplet")
def removeDrop(x_pos: float=0, y_pos: float=0, z_pos: float=0):
    """ move the lang motor to the waste position

    Args:
        x_pos (float): distance to move in x direction
        y_pos (float): distance to move in y direction
        z_pos (float): distance to move in z direction

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    raw = []
    raw.append(requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL),
                            params= dict(dx = x_pos + config[SERVERKEY]['langAction']['safe_clean_pos_1'][0],
                                         dy = y_pos + config[SERVERKEY]['langAction']['safe_clean_pos_1'][1],
                                         dz = z_pos + config[SERVERKEY]['langAction']['safe_clean_pos_1'][2])).json()) # because referene will start from 2 
    raw.append(requests.get("{}/langDriver/moveAbsFar".format(DRIVER_URL),
                            params= dict(dx = x_pos + config[SERVERKEY]['langAction']['safe_clean_pos_2'][0],
                                         dy = y_pos + config[SERVERKEY]['langAction']['safe_clean_pos_2'][1],
                                         dz = z_pos + config[SERVERKEY]['langAction']['safe_clean_pos_2'][2])).json())
    res = requests.get("{}/langDriver/getPos".format(DRIVER_URL)).json()
    raw.append(res)
    retc = return_class(parameters= {"x": x_pos, "y": y_pos, "z": z_pos,'units':{'x':'mm','y':'mm','z':'mm'}},
                        data={'raw':raw,'res':res['data']})
    return retc


@app.on_event("shutdown")
def shutDown():
    """ move the lang motor to the home position when the server is shut down"""
    moveHome()


def main():
    uvicorn.run(app, host=config['servers'][SERVERKEY]['host'],
                     port=config['servers'][SERVERKEY]['port'])


if __name__ == "__main__":
    main()
