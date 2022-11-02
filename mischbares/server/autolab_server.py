"""autolab dirver"""
import os
import time
import re

import json
#pylint: disable=E0611
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
import uvicorn

from mischbares.config.main_config_2 import config
from mischbares.driver.autolab_driver import Autolab
from mischbares.logger import logger
from mischbares.utils import utils

log = logger.get_logger("autolab_server")
SERVERKEY= "autolabDriver"


app = FastAPI(title="Autolab", description="AutolabDriver API", version="2.1.0")


#pylint: disable=R0903
class ReturnClass(BaseModel):
    """
    define a return class for returning the result with pydantic
    """
    parameters: dict = None
    data: dict = None


@app.on_event("startup")
def startup_event():
    """startup event for initializing the autolab driver
    """
    global AUTOLAB
    AUTOLAB = Autolab(config[SERVERKEY])
    log.info("Autolab server started")


@app.get("/autolabDriver/cellonoff")
def set_cell(onoff: str):
    """turn the cell on or off.

    Args:
        onoff (str): "on" or "off" for the cell.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    AUTOLAB.set_cell(onoff)
    retc = ReturnClass(parameters={'onoff': onoff}, data=None)
    log.info("set_cell: %s at the server level", onoff)
    return retc


@app.get("/autolabDriver/reset")
def reset():
    """reset the autolab driver

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    AUTOLAB.reset()
    retc = ReturnClass(parameters=None, data=None)
    log.info("Autolab reset at the server level")
    return retc


@app.get("/autolabDriver/abort")
def abort():
    """abort the current procedure.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    AUTOLAB.abort()
    retc = ReturnClass(parameters=None, data=None)
    log.info("Autolab abort at the server level")
    return retc


@app.on_event("shutdown")
def disconnect():
    """ disconnect from the instrument.
    """
    AUTOLAB.disconnect()
    log.info("Autolab server shutdown")


@app.get("/autolabDriver/setstability")
def set_stability(stability: str):
    """set the stability of the instrument.

    Args:
        stability (str): "high", "low".

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    AUTOLAB.set_stability(stability)
    retc = ReturnClass(parameters={'stability': stability}, data=None)
    log.info("set_stability: %s at the server level", stability)
    return retc


@app.get("/autolabDriver/potential")
def potential():
    """get the current of the instrument vs. reference electrode.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    ret = AUTOLAB.potential()
    retc = ReturnClass(parameters=None, data={'potential': ret, 'units': 'V'})
    return retc


@app.get("/autolabDriver/appliedpotential")
def applied_potential():
    """get the applied potential of the instrument vs. reference electrode.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    ret = AUTOLAB.applied_potential()
    retc = ReturnClass(parameters=None, data={
                        'applied_potential': ret, 'units': 'V'})
    return retc


@app.get("/autolabDriver/current")
def current():
    """get the current of the instrument vs. reference electrode.

    Returns:
        current (float): current value.
    """
    ret = AUTOLAB.current()
    retc = ReturnClass(parameters=None, data={'current': ret, 'units': 'A'})
    return retc


@app.get("/autolabDriver/ismeasuring")
def measure_status():
    """check if the instrument is measuring.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    ret = AUTOLAB.measure_status()
    retc = ReturnClass(parameters=None, data={'measure_status': ret})
    return retc


@app.get("/autolabDriver/setcurrentrange")
def set_current_range(crange: str):
    """set the current range of the instrument.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    AUTOLAB.set_current_range(crange)
    res = [re.findall(r'(\d+)(\w+)', crange)[0]]
    retc = ReturnClass(
        parameters={'parameters': crange, 'units': res[0][1]}, data=None)
    log.info("set_current_range: %s with unit %s at the server level", crange, res[0][1])
    return retc


@app.get("/autolabDriver/measure")
async def perform_measurement(procedure: str, setpoints: str, plot_type: str, on_off_status: str,
                              parse_instruction : str, save_dir: str, optional_name: str):
    """perform the measurement

    Args:
        procedure (str): the procedure to be performed.
        setpoints (dict): the setpoints of the procedure.
        plot_type (str): the type of plot.
        on_off_status (str): the status of the instrument.
        parse_instruction (list[str]): the instruction for parsing the data.
        save_dir (str): save directory.
        optional_name (str): optional file name.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    # eval to convert the string to dict
    setpoints = eval(setpoints)

    if isinstance(parse_instruction, list):
        parse_instruction = [parse_instruction]

    data = await AUTOLAB.perform_measurement(procedure = procedure, setpoints = setpoints,
                                             plot_type = plot_type,
                                             on_off_status = on_off_status,
                                             save_dir = save_dir, optional_name = optional_name,
                                             parse_instruction = parse_instruction)

    retc = ReturnClass(measurement_type='potentiostat_autolab',
                        parameters={'command': 'perform_measurement',
                                    'parameters': dict(procedure=procedure, setpoints=setpoints,
                                                       plot_type=plot_type,
                                                       on_off_status=on_off_status,
                                                       parse_instruction=parse_instruction,
                                                       save_dir=save_dir,
                                                       optional_name=optional_name)},
                        data=data)
    log.info(f"perforn {procedure} wih parameters {setpoints} at the server level \n the result \
                                                                                    is \n {data}")
    return retc



#TODO: check the functionality of this function
@app.websocket("/ws")
async def websocket_messages(websocket: WebSocket):
    """websocket for the autolab driver and visualise the results.

    Args:
        websocket (WebSocket): _description_
    """
    await websocket.accept()
    while True:
        data = await AUTOLAB.queue.get()
        print('data: '+str(data))
        data = {k: [v] for k, v in zip(
            ["t_s", "freq", "Ewe_V", "Ach_V", "Z_real", "Z_imag", "phase", "modulus", "I_A"], data)}
        await websocket.send_text(json.dumps(time.time()))
        await websocket.send_text(json.dumps(data))



@app.get("/autolabDriver/retrieve")
def retrieve(save_dir: str, file_name: str):
    """retrieve the data from the nox file.

    Args:
        safepath (str): the path of the nox file.
        file_name (str): the name of the nox file.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """

    data = utils.load_data_as_json(directory=save_dir, name=file_name.replace('.nox', 'data.json'))
    retc = ReturnClass(parameters = {'save_dir': save_dir, 'file_name': file_name},
                        data= data)
    log.info(f"retrieve the data from {save_dir} with file name {file_name} \
                at the server level with data \n {data}")
    return retc


if __name__ == "__main__":
    uvicorn.run(app, host=config['servers'][SERVERKEY]
                ['host'], port=config['servers'][SERVERKEY]['port'])
