"""autolab dirver"""
import time
import re

import json
#pylint: disable=E0611
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
import uvicorn

from mischbares.config.main_config import config
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
    #pylint: disable=W0601
    global AUTOLAB
    AUTOLAB = Autolab(config[SERVERKEY])
    log.info("Autolab server started")


@app.get("/autolabDriver/cellonoff")
def set_cell(onoff: str):
    """turn the cell on or off.

    Args:
        onoff (str): "on" or "off" for the cell.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    AUTOLAB.set_cell(onoff)
    retc = ReturnClass(parameters = {'onoff': onoff}, data = {})
    log.info("set_cell: %s at the server level", onoff)
    return retc


@app.get("/autolabDriver/reset")
def reset():
    """reset the autolab driver

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    AUTOLAB.reset()
    retc = ReturnClass(parameters={}, data={})
    log.info("Autolab reset at the server level")
    return retc


@app.get("/autolabDriver/abort")
def abort():
    """abort the current procedure.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    AUTOLAB.abort()
    retc = ReturnClass(parameters={}, data={})
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
        retc (ReturnClass): return class with the parameters and the data.
    """
    AUTOLAB.set_stability(stability)
    retc = ReturnClass(parameters={'stability': stability}, data={})
    log.info("set_stability: %s at the server level", stability)
    return retc


@app.get("/autolabDriver/potential")
def potential():
    """get the current of the instrument vs. reference electrode.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    ret = AUTOLAB.potential()
    retc = ReturnClass(parameters= {}, data={'potential': ret, 'units': 'V'})
    return retc


@app.get("/autolabDriver/appliedpotential")
def applied_potential():
    """get the applied potential of the instrument vs. reference electrode.

    Returns:
        retc (ReturnClass): return class with the parameters and the data.
    """
    ret = AUTOLAB.applied_potential()
    retc = ReturnClass(parameters={}, data={
                        'applied_potential': ret, 'units': 'V'})
    return retc


@app.get("/autolabDriver/current")
def current():
    """get the current of the instrument vs. reference electrode.

    Returns:
        current (float): current value.
    """
    ret = AUTOLAB.current()
    retc = ReturnClass(parameters={}, data={'current': ret, 'units': 'A'})
    return retc


@app.get("/autolabDriver/ismeasuring")
def measure_status():
    """check if the instrument is measuring.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """
    ret = AUTOLAB.measure_status()
    retc = ReturnClass(parameters={}, data={'measure_status': ret})
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
        parameters={'parameters': crange, 'units': res[0][1]}, data={})
    log.info("set_current_range: %s with unit %s at the server level", crange, res[0][1])
    return retc


@app.get("/autolabDriver/measure")
async def perform_measurement(procedure: str, plot_type: str,
                              parse_instruction, save_dir: str,
                              setpoints, current_range: str = "1mA",
                              on_off_status: str = "off",
                              optional_name: str = None, measure_at_ocp: bool = False,
                              measurement_id: int = None):
    """perform the measurement

    Args:
        procedure (str): the procedure to be performed.
        plot_type (str): the type of plot.
        parse_instruction (list[str]): the instruction for parsing the data.
        save_dir (str): save directory.
        setpoints (dict): the setpoints of the procedure. Defaults to None.
        current_range (str): the current range of the instrument. Defaults to "1mA".
        on_off_status (str): the status of the instrument. Defaults to "off".
        optional_name (str): optional file name. Defaults to None.
        measure_at_ocp (bool): measure at ocp. Defaults to False.

    Returns:
        retc (ReturnClass): return class with the parameters and the data
    """

    # eval to convert the string to dict
    if setpoints is not None:
        setpoints = eval(setpoints)

    # check the instance of the parse instruction
    if isinstance(parse_instruction, str):
        parse_instruction = eval(parse_instruction)

    data = await AUTOLAB.perform_measurement(procedure = procedure, plot_type = plot_type,
                                            parse_instruction = parse_instruction,
                                            save_dir = save_dir,
                                            setpoints = setpoints,
                                            current_range = current_range,
                                            on_off_status = on_off_status,
                                            optional_name = optional_name,
                                            measure_at_ocp = measure_at_ocp,
                                            measurement_id = measurement_id)

    retc = ReturnClass(measurement_type='potentiostat_autolab',
                        parameters={'command': 'perform_measurement',
                                    'parameters': dict(procedure=procedure, setpoints=setpoints,
                                                    current_range=current_range,
                                                    measure_at_ocp=measure_at_ocp,
                                                    plot_type=plot_type,
                                                    on_off_status=on_off_status,
                                                    parse_instruction=parse_instruction,
                                                    save_dir=save_dir,
                                                    optional_name=optional_name)},
                        data=data)
    log.info(f"perform {procedure} wih parameters {setpoints} at the server level \n the result is \n {data}")
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


def main():
    """main function to run the server.
    """
    uvicorn.run(app, host=config['servers'][SERVERKEY]
                ['host'], port=config['servers'][SERVERKEY]['port'])


if __name__ == "__main__":
    main()
