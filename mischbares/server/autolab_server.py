"""autolab dirver"""
import os
import time
import re

import json
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
import uvicorn

from mischbares.config.main_config_sdc_2 import config
from mischbares.driver.autolab_driver import Autolab
from mischbares.logger import logger
from mischbares.utils import utils

log = logger.get_logger("autolab_server")
SERVERKEY= "autolabDriver"


app = FastAPI(title="Autolab", description="AutolabDriver API", version="2.1.0")

#pylint: disable=R0903
class return_class(BaseModel):
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


@app.get("/autolabDriver/cellonoff")
def set_cell(onoff: str):
    """turn the cell on or off.

    Args:
        onoff (str): "on" or "off" for the cell.
    """
    AUTOLAB.set_cell(onoff)
    retc = return_class(parameters={'onoff': onoff}, data=None)
    return retc


@app.get("/autolabDriver/abort")
def abort():
    """abort the current procedure.
    """
    AUTOLAB.abort()
    retc = return_class(parameters=None, data=None)
    return retc


@app.on_event("shutdown")
def disconnect():
    """ disconnect from the instrument.
    """
    AUTOLAB.disconnect()


@app.get("/autolabDriver/setstability")
def set_stability(stability: str):
    """set the stability of the instrument.

    Args:
        stability (str): "high", "low".
    """
    AUTOLAB.set_stability(stability)
    retc = return_class(parameters={'stability': stability}, data=None)
    return retc


@app.get("/autolabDriver/potential")
def potential():
    """get the current of the instrument vs. reference electrode.

    Returns:
        float: current pottential.
    """
    ret = AUTOLAB.potential()
    retc = return_class(parameters=None, data={'potential': ret, 'units': 'V'})
    return retc


@app.get("/autolabDriver/appliedpotential")
def applied_potential():
    """get the applied potential of the instrument vs. reference electrode.

    Returns:
        flaot: applied potential.
    """
    ret = AUTOLAB.applied_potential()
    retc = return_class(parameters=None, data={
                        'applied_potential': ret, 'units': 'V'})
    return retc


@app.get("/autolabDriver/current")
def current():
    """get the current of the instrument vs. reference electrode.

    Returns:
        current (float): current value.
    """
    ret = AUTOLAB.current()
    retc = return_class(parameters=None, data={'current': ret, 'units': 'A'})
    return retc


@app.get("/autolabDriver/ismeasuring")
def measure_status():
    """check if the instrument is measuring.

    Returns:
        bool: True if measuring, False if not.
    """
    ret = AUTOLAB.measure_status()
    retc = return_class(parameters=None, data={'ismeasuring': ret})
    return retc


@app.get("/autolabDriver/setcurrentrange")
def set_current_range(crange: str):
    """set the current range of the instrument.

    Args:
        current_range (str): set the current range of the instrument.
    """
    AUTOLAB.set_current_range(crange)
    res = [re.findall(r'(\d+)(\w+)', crange)[0]]
    retc = return_class(
        parameters={'parameters': crange, 'units': res[0][1]}, data=None)
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
        data (dict): extracted data from the nox file of the procedure.
    """
    setpoints = eval(setpoints)
    parseinstruction = [parse_instruction]

    data = await AUTOLAB.perform_measurement(procedure, setpoints, plot_type, on_off_status, save_dir, optional_name, parseinstruction)

    retc = return_class(measurement_type='potentiostat_autolab',
                        parameters={'command': 'measure',
                                    'parameters': dict(procedure=procedure, setpointjson=setpoints,
                                                       plot=plot_type, onoffafter=on_off_status,
                                                       safepath=save_dir, filename=optional_name, parseinstruction=parseinstruction)},
                        data=data)
    return retc




@app.websocket("/ws")
async def websocket_messages(websocket: WebSocket):
    """websocket for the autolab driver and visualise the results.

    Args:
        websocket (WebSocket): _description_
    """
    await websocket.accept()
    while True:
        data = await AUTOLAB.q.get()
        print('data: '+str(data))
        data = {k: [v] for k, v in zip(
            ["t_s", "freq", "Ewe_V", "Ach_V", "Z_real", "Z_imag", "phase", "modulus", "I_A"], data)}
        await websocket.send_text(json.dumps(time.time()))
        await websocket.send_text(json.dumps(data))



@app.get("/autolabDriver/retrieve")
def retrieve(safepath: str, filename: str):
    """retrieve the data from the nox file.

    Args:
        safepath (str): _description_
        filename (str): _description_

    Returns:
        _type_: _description_
    """
    conf = dict(safepath=safepath, filename=filename)
    path = os.path.join(conf['safepath'], conf['filename'])
    with open(path.replace('.nox', '_data.json'), 'r') as f:
        ret = json.load(f)
    retc = return_class(parameters={'safepath': safepath, 'filename': filename},
                        data={'appliedpotential': ret})
    return retc


if __name__ == "__main__":
    uvicorn.run(app, host=config['servers'][SERVERKEY]
                ['host'], port=config['servers'][SERVERKEY]['port'])
