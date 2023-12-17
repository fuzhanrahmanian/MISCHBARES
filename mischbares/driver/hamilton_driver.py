from pydantic import BaseModel
import sys
import clr
import numpy as np

from mischbares.config.main_config import config

from mischbares.logger import logger

log = logger.get_logger("hamilton_driver")

path = config['pump']['Hamilton']['path']
dlls = config['pump']['Hamilton']['dlls']
PUMP_IP = config['pump']['Hamilton']['IP']
hamilton_conf = config['pump']['Hamilton']['conf']

sys.path.append(path)

for dll in dlls:
    print(f'Adding {dll}')
    clr.AddReference(dll)

from Hamilton.Components.TransportLayer import Protocols
from Hamilton import MicroLab
from Hamilton.MicroLab import Components

class return_class(BaseModel):
    parameters: dict = None
    data: dict = None

class Hamilton:
    def __init__(self):
        self.conf = hamilton_conf
        self.connect()

    def connect(self):
        """Connect to the pumps"""
        self.ml600Chain = MicroLab.DaisyChain()

            #self.discovered = self.ml600Chain.Discover(5)
            #self.ml600Chain.Connect(self.discovered[0].Address,self.discovered[0].Port)
        if not self.ml600Chain.get_IsConnected():
            try:
                self.ml600Chain.Connect(PUMP_IP)
                log.info("Made a connection to Microlab 600")
            except:
                log.error("Failed to connect to Microlab 600")
                raise Exception("Failed to connect to Microlab 600")

        self.InstrumentOnChain = self.ml600Chain.get_ML600s()[0].get_ChainPosition()
        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.LeftPump.Syringe.SetSize(np.uint32(self.conf['left']['syringe']['volume']))
        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.RightPump.Syringe.SetSize(np.uint32(self.conf['right']['syringe']['volume']))
        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.LeftPump.Syringe.SetFlowRate(np.uint32(self.conf['left']['syringe']['flowRate']))
        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.RightPump.Syringe.SetFlowRate(np.uint32(self.conf['right']['syringe']['flowRate']))
        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.LeftPump.Syringe.SetInitFlowRate(np.uint32(self.conf['left']['syringe']['initFlowRate']))
        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.RightPump.Syringe.SetInitFlowRate(np.uint32(self.conf['right']['syringe']['initFlowRate']))

        self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.Pumps.InitializeDefault()
        if self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.Pumps.AreInitialized():
            log.info("Pumps are initialized")

    def pump(self,leftVol=0,rightVol=0,leftPort=0,rightPort=0,delayLeft=0,delayRight=0):
        """Pump a volume from a port
        Args:
            leftVol (int, optional): Volume to pump from left syringe. Defaults to 0.
            rightVol (int, optional): Volume to pump from right syringe. Defaults to 0.
            leftPort (int, optional): Port to pump from left syringe. Defaults to 0.
            rightPort (int, optional): Port to pump from right syringe. Defaults to 0.
            delayLeft (int, optional): Delay in ms for left syringe. Defaults to 0.
            delayRight (int, optional): Delay in ms for right syringe. Defaults to 0.
        Returns:
            ml600Chain.ML600s: Returns the pump object
        """
        left_volume = np.int32(leftVol)
        right_volume = np.int32(rightVol)
        left_port = np.byte(leftPort)
        right_port = np.byte(rightPort)
        delay_right = np.uint(delayRight)
        delay_left = np.uint32(delayLeft)
        ret = self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.Pumps.AspirateFromPortsWithDelay(left_volume, right_volume,
                                                                                                         left_port, right_port,
                                                                                                         delay_right, delay_left)
        return ret
    
    def getStatus(self):
        """Helper function to get the status of the pumps

        Returns:
            dict: Returns a dict with the status of the pumps
        """
        volume_left = self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.LeftPump.Syringe.GetRemainingVolume()
        volume_right = self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.RightPump.Syringe.GetRemainingVolume()
        valve_pump_left = self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.LeftPump.Valve.GetNumberedPos()
        valve_pump_right = self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.RightPump.Valve.GetNumberedPos()
        return dict(vl=volume_left,vr=volume_right,vpl=valve_pump_left,vpr=valve_pump_right)


    def moveAbs(self,leftSteps=0,rightSteps=0,leftPort=0,rightPort=0,delayLeft=0,delayRight=0):
        """Move the pumps to a certain position

        Args:
            leftSteps (int, optional): Steps to move left syringe. Defaults to 0.
            rightSteps (int, optional): Steps to move right syringe. Defaults to 0.
            leftPort (int, optional): Port to move left syringe. Defaults to 0.
            rightPort (int, optional): Port to move right syringe. Defaults to 0.
            delayLeft (int, optional): Delay in ms for left syringe. Defaults to 0.
            delayRight (int, optional): Delay in ms for right syringe. Defaults to 0.
        Returns:
            ml600Chain.ML600s: Returns the pump object
        """
        log.info(f"Moving pumps to {leftSteps} and {rightSteps}")
        left_volume = np.int32(leftSteps) #in nL
        right_volume = np.int32(rightSteps)
        left_port = np.byte(leftPort) #1,2 or 9,10
        right_port = np.byte(rightPort)
        delay_right = np.uint(delayRight) # ms
        delay_left = np.uint32(delayLeft)
        ret = self.ml600Chain.ML600s[self.InstrumentOnChain].Instrument.Pumps.MoveAbsoluteInStepsWithDelay(left_volume, right_volume, left_port, right_port, delay_right, delay_left)
        return ret

    def disconnect(self):
        """ Disconnect the pumps"""
        log.info("Disconnecting pumps")
        status = self.getStatus()
        # Get the remaining volume and pump it out
        self.pump(leftVol=-status['vl'],rightVol=-status['vr'],leftPort=self.conf['left']['valve']['prefOut'], rightPort=self.conf['right']['valve']['prefOut'])
        try:
            self.ml600Chain.Disconnect()
        except:
            log.error("Failed to disconnect pumps")
            raise Exception("Failed to disconnect pumps")