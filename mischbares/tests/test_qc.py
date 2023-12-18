import pytest
from multiprocessing import Process
from mischbares.driver.hamilton_driver import Hamilton
from mischbares.quality_control.drop_detection import DropDetection
from mischbares.config.main_config import config
hamilton_conf = config['pump']['Hamilton']['conf']


def pumpSingleR(pump, volume: int=0, times:int=1):
    """ pump a certain volume from a certain port.

    Args:
        volume (int): volume to pump from the right syringe
        times (int): number of times to pump
    """
    #we usually had all volumes for the other pumps in microliters
    #so here we expect he input to be in microliters and convert it to nL
    volnl = volume*1000 # micro liter

    if volnl > 0:
        In = 'prefIn'
        Out = 'prefOut'
    else:
        In = 'prefOut'
        Out = 'prefIn'

    for _ in range(times):
        #first aspirate a negative volume through the preferred in port
        pump.pump(rightVol=abs(volnl), leftVol=0, rightPort=hamilton_conf['right']['valve'][In], leftPort=0, delayLeft=0, delayRight=0)


        #then eject through the preferred out port
        pump.pump(rightVol=-abs(volnl), leftVol=0, rightPort=hamilton_conf['right']['valve'][Out], leftPort=0, delayLeft=0, delayRight=0)

def run_pump():
    pump = Hamilton()
    pumpSingleR(pump, volume=200, times=1)

def test_timeout_detection():
    """
    Test the timeout detection.

    Asserts:
        drop_detection.drop_detected: False
    """
    drop_detection = DropDetection(timeout=5)
    # Catch the timeout exception
    with pytest.raises(TimeoutError):
        drop_detection.analyze_video_dynamic_roi()
    assert drop_detection.get_drop_detection_status() == False

def test_detection_with_pump():
    """
    Test the detection with pump.

    Args:
        drop_detection: An instance of the drop detection class.

    Asserts:
        drop_detection.drop_detected: True
    """
    drop_detection = DropDetection()
    # Create and start the pump process
    pump_process = Process(target=run_pump)
    pump_process.start()
    # Start drop detection
    drop_detection.analyze_video_dynamic_roi()

    assert drop_detection.get_drop_detection_status() == True

