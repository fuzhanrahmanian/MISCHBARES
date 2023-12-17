import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import time
import json
import os

from mischbares.logger import logger
from mischbares.config.main_config import config

log = logger.get_logger("hamilton_server")
DRIVERKEY = 'hamiltonDriver'
driver_url = config['servers'][DRIVERKEY]
ACTIONKEY = 'hamilton'
action_url = config['servers'][ACTIONKEY]
hamilton_conf = config['pump']['Hamilton']['conf']

app = FastAPI(title="Hamilton syringe pump action server",
    description="This is a very fancy pump action server",
    version="1.0.0")

class return_class(BaseModel):
    parameters: dict = None
    data: dict = None


@app.get("/hamilton/pumpL/")
def pumpSingleL(volume: int=0, times:int=1):
    """pump a certain volume from a certain port.
    The volume is passed in microliters and converted to nanoliters.

    Args:
        volume (int): volume to pump from the left syringe
        times (int): number of times to pump
    Returns:
        retc (return_class): return class with the parameters and the data
    """
    # Convert volume to nanoliters
    volume_nl = volume*1000
    return_left = []

    if volume_nl > 0:
        In = 'prefIn'
        Out = 'prefOut'
    else:
        In = 'prefOut'
        Out = 'prefIn'

    for _ in range(times):
        #first aspirate a negative volume through the preferred in port
        aspiration_params = dict(leftVol=abs(volume_nl), rightVol=0,
                        leftPort=hamilton_conf['left']['valve'][In],
                        rightPort=0, delayLeft=0, delayRight=0)
        res_aspiration = requests.get(f"http://{driver_url['host']}:{driver_url['port']}/hamiltonDriver/pump", timeout=None,
                            params=aspiration_params).json()
        return_left.append(res_aspiration)

        #then eject through the preferred out port
        dispens_params = dict(leftVol=-abs(volume_nl), rightVol=0,
                        leftPort=hamilton_conf['left']['valve'][Out],
                        rightPort=0, delayLeft=0, delayRight=0)
        res_dispens = requests.get(f"http://{driver_url['host']}:{driver_url['port']}/hamiltonDriver/pump", timeout=None,
                            params=dispens_params).json()

        return_left.append(res_dispens)

    retc = return_class(parameters= {'volumeR':volume,'times':times},
                    data = {i:return_left[i] for i in range(len(return_left))})
    return retc

@app.get("/hamilton/pumpR/")
def pumpSingleR(volume: int=0, times:int=1):
    """pump a certain volume from a certain port.

    Args:
        volume (int): volume to pump from the right syringe
        times (int): number of times to pump

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    # Convert volume to nanoliters
    volume_nl = volume*1000
    return_right = []

    if volume_nl > 0:
        In = 'prefIn'
        Out = 'prefOut'
    else:
        In = 'prefOut'
        Out = 'prefIn'

    for _ in range(times):
        #first aspirate a negative volume through the preferred in port
        aspiration_params = dict(rightVol=abs(volume_nl),
                                 leftVol=0, rightPort=hamilton_conf['right']['valve'][In],
                                 leftPort=0, delayLeft=0,
                                 delayRight=0)

        res_aspiration = requests.get(f"http://{driver_url['host']}:{driver_url['port']}/hamiltonDriver/pump", timeout=None,
                            params=aspiration_params).json()

        return_right.append(res_aspiration)

        #then eject through the preferred out port
        dispens_params = dict(rightVol=-abs(volume_nl), leftVol=0,
                              rightPort=hamilton_conf['right']['valve'][Out],
                              leftPort=0, delayLeft=0, delayRight=0)
        res_dispens = requests.get(f"http://{driver_url['host']}:{driver_url['port']}/hamiltonDriver/pump", timeout=None,
                            params=dispens_params).json()
        return_right.append(res_dispens)

    retc = return_class(parameters= {'volumeR':volume,'times':times},
                    data = {i:return_right[i] for i in range(len(return_right))})

    return retc

def main():
    """Start the server."""
    uvicorn.run(app, host=action_url['host'], port=action_url['port'])

if __name__ == "__main__":
    main()