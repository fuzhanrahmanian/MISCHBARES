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


#TODO:this function need to be removed and data retrieval should be done with database.
def get_ocp_voltage(file_name, path="C:/Users/SDC_1/Documents/Github/sdc_gb"):
    """get the ocp voltage from the file.

    Args:
        file_name (str): file name of the file
        path (str, optional): path to the save data.
                              Defaults to "C:/Users/SDC_1/Documents/Github/sdc_gb".

    Returns:
        voltage (float): ocp voltage
    """
    data = utils.load_data_as_json(directory = path, name = f"{file_name}_data.json")
    voltage = np.round(np.mean(data['recordsignal']['WE(1).Potential'][-10:]),5)
    log.info("get_ocp_voltage: %s", voltage)
    return voltage


#TODO: this is a temporary solution for the measurement.It should be modified.
@app.get("/autolab/measure/")
def measure(procedure: str, setpoints: str, plot_type: str, on_off_status: str,
            parse_instruction: str, save_dir: str, optional_name: str = None, iteration: str = None):
    """
    Measure a recipe and manipulate the parameters:

    **measure_conf**: is explained in the echemprocedures folder
    """

    # Need to check whether there ocp voltage needs to be taken or not , and from which experiment
    log.info(f"setpoint json before is {setpoints}")
    if procedure=="ca":
        setpoints = eval(setpoints)
        log.infor("the applied potential is : %s", setpoints["applypotential"])

        if setpoints["applypotential"]["Setpoint value"] == "?":
            setpoints["applypotential"]["Setpoint value"] = \
                get_ocp_voltage(file_name = f"OCP_record_signal_{eval(iteration)}", path=save_dir)
        else:
            setpoints["applypotential"]["Setpoint value"] += \
                get_ocp_voltage(file_name = f"OCP_record_signal_{eval(iteration)}", path=save_dir)
        setpoints = json.dumps(setpoints)
        sleep(0.7)

    if procedure=="eis":
        setpoints = eval(setpoints)
        log.infor("the applied potential is : %s", setpoints["FHSetSetpointPotential"])
        if setpoints["FHSetSetpointPotential"]["Setpoint value"] == "?":
            setpoints["FHSetSetpointPotential"]["Setpoint value"] =\
                get_ocp_voltage(file_name = f"OCP_record_signal_{eval(iteration)}", path=save_dir)

        else:
            setpoints["FHSetSetpointPotential"]["Setpoint value"] +=\
                get_ocp_voltage(file_name = f"OCP_record_signal_{eval(iteration)}", path=save_dir)
        setpoints = json.dumps(setpoints)
        sleep(0.7)

    if procedure=="cv":
        setpoints = eval(setpoints)
        if setpoints["FHSetSetpointPotential"]["Setpoint value"] == "?":
            setpoints["FHSetSetpointPotential"]["Setpoint value"] =\
                get_ocp_voltage(file_name = f"OCP_record_signal_{eval(iteration)}", path=save_dir)
        else:
            setpoints["FHSetSetpointPotential"]["Setpoint value"] +=\
                get_ocp_voltage(file_name = f"OCP_record_signal_{eval(iteration)}", path=save_dir)

        setpoints["CVLinearScanAdc164"]["StartValue"] =\
            setpoints["FHSetSetpointPotential"]["Setpoint value"]
        setpoints["CVLinearScanAdc164"]["UpperVertex"] +=\
            setpoints["FHSetSetpointPotential"]["Setpoint value"]
        setpoints["CVLinearScanAdc164"]["LowerVertex"] +=\
            setpoints["FHSetSetpointPotential"]["Setpoint value"]

        setpoints = json.dumps(setpoints)
        sleep(0.7)
    log.info("setpoint json after ocp applied is %s", setpoints)

    measure_conf = dict(procedure=procedure,
                        setpoints=setpoints,
                        plot_type=plot_type,
                        on_off_status=on_off_status,
                        save_dir=save_dir,
                        optional_name=optional_name,
                        parse_instruction=parse_instruction)

    #TODO: log info needs to be modified.This is just for testing and temporaty.
    log.info("measure_conf: %s", measure_conf)

    #TODO: time out should be modified.
    res = requests.get(f"{SERVER_URL}/autolabDriver/measure",
                        params=measure_conf, timeout=None).json()

    retc = ReturnClass(parameters = measure_conf, data = res)
    #TODO: more proper log for this function.
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
