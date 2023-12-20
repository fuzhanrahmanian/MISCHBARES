"""lang driver"""
import os
import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from mischbares.config.main_config import config
from mischbares.logger import logger
from mischbares.driver.lang_driver import langNet

log = logger.get_logger("lang_server")
SERVERKEY = "langDriver"

lang_motor = None

app = FastAPI(title="Lang server",
    description="This is a fancy motor driver server",
    version="1.0")


class return_class(BaseModel):
    parameters: dict = None
    data: dict = None

@app.get("/health")
def health_check():
    """ health check to see if the server is up and running
    Returns:
        dict: status
    """
    return {"status": "healthy"}


@app.get("/langDriver/connect")
def connect():
    """connect to the lang motor

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.connect()
    retc = return_class(parameters={},data={})
    return retc


@app.get("/langDriver/disconnected")
def disconnect():
    """disconnect from the lang motor

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.disconnect()
    retc = return_class(parameters={},data={})
    return retc

@app.get("/langDriver/goHome")
def goHome():
    """go home with the lang motor

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.goHome()
    retc = return_class(parameters={},data={})
    return retc


@app.get("/langDriver/moveRelFar")
def moveRelFar(dx: float, dy: float, dz: float):
    """move the lang motor relative far

    Args:
        dx (float): distance to move in x
        dy (float): distance to move in y
        dz (float): distance to move in z

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.moveRelFar(dx, dy, dz)
    retc = return_class(parameters={'dx': dx, 'dy': dy, 'dz':dz,
                            'units':{'dx':'mm','dy':'mm','dz':'mm'}},
                            data={})
    return retc


@app.get("/langDriver/getPos")
def getPos():
    """get the position of the lang motor

    Returns:
        retc (return_class): return class with the parameters and the data
    """

    data= lang_motor.getPos()
    retc = return_class(parameters={},data={'pos':data,'units':'mm'})
    return retc

@app.get("/langDriver/moveRelZ")
def moveRelZ(dz: float, wait: bool=True):
    """move the lang motor relative in z

    Args:
        dz (float): distance to move in z
        wait (bool): wait until the move is finished

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.moveRelZ(dz, wait)
    retc = return_class(parameters={'dz': dz, 'wait': wait,'units':{'dz':'mm'}},data={})
    return retc


@app.get("/langDriver/moveRelXY")
def moveRelXY(dx: float, dy: float, wait: bool=True):
    """ move the lang motor relative in x and y

    Args:
        dx (float): distance to move in x
        dy (float): distance to move in y
        wait (bool): wait until the move is finished

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.moveRelXY(dx, dy, wait)
    retc = return_class(parameters={'dx': dx, 'dy': dy, 'wait': wait,'units':{'dx':'mm','dy':'mm'}},
                        data={})
    return retc


@app.get("/langDriver/moveAbsXY")
def moveAbsXY(x: float, y: float, wait: bool=True):
    """ move the lang motor absolute in x and y

    Args:
        x (float): distance to move in x
        y (float): distance to move in y
        wait (bool): wait until the move is finished

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.moveAbsXY(x, y, wait)
    retc = return_class(parameters={'x': x, 'y': y, 'wait': wait},data={})
    return retc


@app.get("/langDriver/moveAbsZ")
def moveAbsZ(z_pos: float, wait: bool=True):
    """ move the lang motor absolute in z

    Args:
        z_pos (float): distance to move in z
        wait (bool): wait until the move is finished

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.moveAbsZ(z_pos, wait)
    retc = return_class(parameters={'z': z_pos, 'wait': wait,'units':{'z':'mm'}},
                        data={})
    return retc


@app.get("/langDriver/moveAbsFar")
def moveAbsFar(dx: float, dy: float, dz: float):
    """ move the lang motor absolute far

    Args:
        dx (float): distance to move in x
        dy (float): distance to move in y
        dz (float): distance to move in z

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.moveAbsFar(dx, dy, dz)
    retc = return_class(parameters={'dx': dx, 'dy': dy, 'dz': dz,
                                    'units':{'dx':'mm','dy':'mm','dz':'mm'}},data={})
    return retc


@app.get("/langDriver/stopMove")
def stopMove():
    """ stop the lang motor

    Returns:
        retc (return_class): return class with the parameters and the data
    """
    lang_motor.stopMove()
    retc = return_class(parameters={},data={})
    return retc

@app.on_event("shutdown")
def shutDown():
    """ shutdown the lang motor
    """
    lang_motor.disconnect()


def main():
    """main function"""
    global lang_motor
    lang_motor = langNet()
    uvicorn.run(app, host=config['servers'][SERVERKEY]['host'],
                port=config['servers'][SERVERKEY]['port'])

    log.info("instantiated motor")


if __name__ == "__main__":
    main()