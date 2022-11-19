""" autolab action"""
from time import sleep
import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests

import numpy as np

from mischbares.config.main_config import config
from mischbares.logger import logger
from mischbares.utils import utils

log = logger.get_logger("autolab_action")
SERVERKEY = "autolab"
SERVER_URL = config[SERVERKEY]['url']
app = FastAPI(title="Autolab", description="Autolab API", version="2.1.0")


#pylint: disable=R0903
class ReturnClass(BaseModel):
    """
    define a return class for returning the result with pydantic.
    """
    parameters: dict = None
    data: dict = None

@app.get("/autolab/cellonoff/")
def set_cell(onoff:str):
    """turn the cell on or off.

    Args:
        onoff (str): "on" or "off" for the cell.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    res = requests.get(f"{SERVER_URL}/autolabDriver/cellonoff", params={'onoff':onoff},
                       timeout=None).json()
    retc = ReturnClass(parameters = {'cellonoff':onoff}, data = res)
    log.info("set_cell: %s at the action level", onoff)
    return retc


@app.get("/autolab/potential/")
def potential():
    """get the current potential of the cell.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    res = requests.get(f"{SERVER_URL}/autolabDriver/potential", timeout=None).json()
    retc = ReturnClass(parameters = {}, data = res)
    return retc


@app.get("/autolab/appliedpotential/")
def applied_potential():
    """get the current applied potential of the cell vs reference electrode.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    res = requests.get(f"{SERVER_URL}/autolabDriver/appliedpotential", timeout=None).json()
    retc = ReturnClass(parameters = {}, data = res)
    return retc


@app.get("/autolab/current/")
def current():
    """get the current applied potential of the cell vs reference electrode.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    res = requests.get(f"{SERVER_URL}/autolabDriver/current", timeout=None).json()
    retc = ReturnClass(parameters = {}, data = res)
    return retc


@app.get("/autolab/ismeasuring/")
def measure_status():
    """check if the instrument is measuring.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    res = requests.get(f"{SERVER_URL}/autolabDriver/ismeasuring", timeout=None).json()
    retc = ReturnClass(parameters = {}, data = res)
    return retc


@app.get("/autolab/setcurrentrange/")
def set_current_range(crange:str):
    """set the current range of the instrument.

    Args:
        crange (str): current range of the instrument
                        (10A, 1A, 100A, 10mA, 1mA, 100uA, 10uA, 1uA, 100nA, 10nA).

    Returns:
        _type_: _description_
    """
    res = requests.get(f"{SERVER_URL}/autolabDriver/setcurrentrange",
                        params={'crange':crange}, timeout=None).json()
    retc = ReturnClass(parameters= {'crange': crange}, data = res)
    return retc


@app.get("/autolab/measure/")
def measure(procedure: str, plot_type: str, parse_instruction, save_dir: str,
            setpoints, current_range: str = "1mA",
            on_off_status: str = "off",
            optional_name: str = None, measure_at_ocp: bool = False):
    """measure the requested procedure.
    Args:
        procedure (str): procedure to be measured.
        plot_type (str): plot type of the procedure.
        parse_instruction (str): parse instruction of the procedure.
        save_dir (str): save directory of the procedure.
        setpoints (str): setpoints of the procedure.
        current_range (str, optional): current range of the instrument.
        on_off_status (str, optional): on or off status of the cell.
        optional_name (str, optional): optional name of the procedure.
        measure_at_ocp (bool, optional): measure at ocp or not.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    log.info("measure: %s at action level", procedure)

    measure_conf = dict(procedure = procedure, plot_type = plot_type,
                        parse_instruction = parse_instruction,
                        save_dir = save_dir, setpoints = setpoints,
                        current_range = current_range,
                        on_off_status = on_off_status,
                        optional_name = optional_name,
                        measure_at_ocp = measure_at_ocp)

    log.info("The procedure parameters at action level is: %s", measure_conf)

    res = requests.get(f"{SERVER_URL}/autolabDriver/measure",
                        params=measure_conf, timeout=None).json()

    retc = ReturnClass(parameters = measure_conf, data = res)

    return retc


@app.get("/autolab/retrieve")
def retrieve(save_dir: str, file_name: str):
    """retrieve the data from the file.

    Args:
        save_dir (str): directory of the file.
        file_name (str): name of the file.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    conf = dict(safepath= save_dir,filename = file_name)
    res = requests.get(f"{SERVER_URL}/autolabDriver/retrieve", params=conf, timeout=None).json()
    retc = ReturnClass(parameters = {'save_dir':save_dir,'file_name':file_name}, data = res)
    return retc


def main():
    """main function to run the action.
    """
    uvicorn.run(app, host=config['servers'][SERVERKEY]['host'],
                port=config['servers'][SERVERKEY]['port'])


if __name__ == "__main__":
    main()
