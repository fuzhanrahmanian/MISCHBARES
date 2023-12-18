import sys
import time
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests

from mischbares.config.main_config import config
from mischbares.logger import logger

SERVERKEY = "lang"
DRIVER_KEY = "langDriver"
DRIVER_URL = f"http://{config['servers'][DRIVER_KEY]['host']}:{config['servers'][DRIVER_KEY]['port']}"

log = logger.get_logger("lang_action")

app = FastAPI(title="lang server",
    description="This is a fancy lang motor action server",
    version="1.0.0")



class return_class(BaseModel):
    parameters :dict = None
    data: dict = None


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
def moveDown(dz: float, steps: float, threshold:float=0.26):
    """ move the lang motor down until the force is exceeded
    Args:
        dz (float): distance to move in z direction
        steps (float): maximum steps to move down
        maxForce (float): maximum force to apply
        threshold (float): threshold to stop moving down

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    steps = int(steps)
    step = 0
    while step < steps: # TODO: Add QC with the potentiostat to check if the contact is formed
        if dz < threshold:
            requests.get("{}/langDriver/moveRelFar".format(DRIVER_URL), params= dict(dx = 0, dy = 0, dz = dz)).json()
            log.info(f"steps: {step}")
            step += 1
            time.sleep(0.7)
        else:
            log.info("Threshold exceeded")
            break
    if step > steps: # TODO: Check if potential is 0. -> Die soon
        log.warning("Force exceeded the max and the force sensor will die soon (RIP)")

    pos = requests.get("{}/langDriver/getPos".format(DRIVER_URL)).json()

    retc = return_class(parameters= {"dz": dz,"steps":steps,
                                    'units':{'dz':'mm'}},
                        data= {'raw':pos, 'res':{
                              'units':{'pos':'mm'}}})

    return retc

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
