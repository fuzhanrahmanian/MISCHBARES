import time
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

from mischbares.logger import logger
from mischbares.config.main_config import config
from mischbares.driver.hamilton_driver import Hamilton

log = logger.get_logger("hamilton_server")

app = FastAPI(title="Hamilton Syringe PumpDriver server",
    description="This is a very fancy syringe pump server",
    version="1.0.0")


class return_class(BaseModel):
    parameters: dict = None
    data: dict = None

hamilton_pump = None

@app.get("/hamiltonDriver/pump")
def pump(leftVol:int=0,rightVol:int=0,leftPort:int=0,rightPort:int=0,delayLeft:int=0,delayRight:int=0):
    """pump a certain volume from a certain port

    Args:
        leftVol (int): volume to pump from the left syringe
        rightVol (int): volume to pump from the right syringe
        leftPort (int): port to pump from the left syringe
        rightPort (int): port to pump from the right syringe
        delayLeft (int): delay in ms after pumping from the left syringe
        delayRight (int): delay in ms after pumping from the right syringe

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    global hamilton_pump
    hamilton_pump.pump(leftVol=leftVol,rightVol=rightVol,leftPort=leftPort,rightPort=rightPort,delayLeft=delayLeft,delayRight=delayRight)
    retc = return_class(parameters=dict(leftVol=leftVol,rightVol=rightVol,
                                        leftPort=leftPort,rightPort=rightPort,
                                        delayLeft=delayLeft,delayRight=delayRight),
                                        data={})
    return retc


@app.get("/hamiltonDriver/getStatus")
def readStatus():
    """read the status of the pump

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    global hamilton_pump
    ret = hamilton_pump.getStatus()
    data = dict(volume_nL_left=ret['vl'],
                volume_nL_right=ret['vr'],
                valve_position_left=ret['vpl'],
                valve_position_right=ret['vpr'])
    retc = return_class(parameters={},data=data)
    return retc


@app.on_event("shutdown")
def shutdown():
    """shutdown the pump"""
    global hamilton_pump
    hamilton_pump.shutdown()
    retc = return_class(parameters={},data={})
    return retc

def main():
    """main function"""
    global hamilton_pump
    hamilton_pump = Hamilton()
    uvicorn.run(app, host=config['servers']['hamiltonDriver']['host'], port=config['servers']['hamiltonDriver']['port'])

if __name__ == "__main__":
    main()
