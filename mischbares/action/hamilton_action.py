import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import threading
import time

import mischbares.utils.utils as utils
from mischbares.logger import logger
from mischbares.config.main_config import config
from mischbares.quality_control.drop_detection import DropDetection


log = logger.get_logger("hamilton_server")
DRIVERKEY = 'hamiltonDriver'
driver_url = config['servers'][DRIVERKEY]
ACTIONKEY = 'hamilton'
action_url = config['servers'][ACTIONKEY]
hamilton_conf = config['pump']['Hamilton']['conf']

QC_MOTOR_KEY = config['servers'][DRIVERKEY]['qc_motor']
QC_MOTOR_SAFE_POS = config['servers'][DRIVERKEY]['qc_motor_safe_pos']
qc_motor_host = config['servers'][QC_MOTOR_KEY]['host']
qc_motor_port = config['servers'][QC_MOTOR_KEY]['port']


app = FastAPI(title="Hamilton syringe pump action server",
    description="This is a very fancy pump action server",
    version="1.0.0")

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

        time.sleep(5)
        check_waste_thread = threading.Thread(target=check_waste)
        check_waste_thread.start()
        #then eject through the preferred out port
        dispens_params = dict(leftVol=-abs(volume_nl), rightVol=0,
                        leftPort=hamilton_conf['left']['valve'][Out],
                        rightPort=0, delayLeft=0, delayRight=0)

        res_dispens = requests.get(f"http://{driver_url['host']}:{driver_url['port']}/hamiltonDriver/pump", timeout=None,
                            params=dispens_params).json()

        return_left.append(res_dispens)

    check_waste_thread.join()

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

        time.sleep(5)
        check_waste_thread = threading.Thread(target=check_waste)
        check_waste_thread.start()
        #then eject through the preferred out port
        dispens_params = dict(rightVol=-abs(volume_nl), leftVol=0,
                              rightPort=hamilton_conf['right']['valve'][Out],
                              leftPort=0, delayLeft=0, delayRight=0)
        res_dispens = requests.get(f"http://{driver_url['host']}:{driver_url['port']}/hamiltonDriver/pump", timeout=None,
                            params=dispens_params).json()


        return_right.append(res_dispens)

    check_waste_thread.join()

    retc = return_class(parameters= {'volumeR':volume,'times':times},
                    data = {i:return_right[i] for i in range(len(return_right))})

    return retc

def check_waste():
    """
    Checks if the motor is at the waste position and starts drop detection.

    This function sends a request to the motor to get its current position.
    If the motor is at the waste position, it starts the drop detection process.
    Otherwise, it raises a ValueError indicating that the motor is not at the waste position.

    Raises:
        KeyError: If the key is not found in the config file.
        ValueError: If the length of the safe position and the current position do not match.
        TimeoutError: If the drop detection times out or
    """
    position_motor = requests.get(f"http://{qc_motor_host}:{qc_motor_port}/langDriver/getPos", timeout=None)
    if position_motor.status_code == 200:
        safe_position = utils.get_nested_value(config, QC_MOTOR_SAFE_POS)
        drop_detection = DropDetection()
        if not len(eval(position_motor.content)['data']['pos']) == len(safe_position):
            raise ValueError("The length of the safe position and the current position do not match")
        else:
            if [round(i, 0) for i in eval(position_motor.content)['data']['pos']] == safe_position:
                log.info("Motor is at the waste position, start drop detection")
                drop_detection.analyze_video_dynamic_roi()
                if drop_detection.got_timeout_error:
                    utils.send_to_telegram(message=f"Detection timed out: \n \n Material bottle is empty, please refill it.", message_type="error")
                    drop_detection.timeout = config["QC"]["waste_camera"]["kill_timeout"]
                    start_time = time.time()
                    drop_detection.analyze_video_dynamic_roi()

                    if drop_detection.got_timeout_error:
                        log.info("Detection timed out again, stop the experiment")
                        utils.send_to_telegram(message=f"Detection timed out again: \n \n Closing experiment", message_type="error")
                        host_url = config['servers']['orchestrator']['host']
                        port_orchestrator = config['servers']['orchestrator']['port']
                        requests.post(f"http://{host_url}:{port_orchestrator}/orchestrator/pause", timeout=None)
            else:
                log.info("Motor is not at the waste position, do not start drop detection")

            if drop_detection.get_drop_detection_status():
                log.info("Drop detected, continue with the experiment")
    else:
        raise RuntimeError("Error getting the position of the motor. Status code: ", position_motor.status_code)


def main():
    """Start the server."""
    uvicorn.run(app, host=action_url['host'], port=action_url['port'])

if __name__ == "__main__":
    main()