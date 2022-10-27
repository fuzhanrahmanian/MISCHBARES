"""autolab dirver"""
import os
import sys
import time
from time import sleep
from copy import copy
import json
import asyncio
import clr

from mischbares.logger import logger
from mischbares.utils import utils

log = logger.get_logger("autolab_driver")

class Autolab:
    """autolab class for defining the base functions of Metrohm instrument
    """

    def __init__(self,autolab_conf):
        #init a Queue for the visualizer
        self.queue = asyncio.Queue(loop=asyncio.get_event_loop())
        self.basep = autolab_conf["basep"]
        sys.path.append(self.basep)
        self.procp = autolab_conf["procp"]
        self.hwsetupf = autolab_conf["hwsetupf"]
        self.micsetupf = autolab_conf["micsetupf"]
        self.proceduresd = autolab_conf["proceuduresd"]
        try:
            # pylint: disable=E1101, E0401, C0415
            clr.AddReference("EcoChemie.Autolab.Sdk")
            from EcoChemie.Autolab import Sdk as sdk
        except:
            log.error("cannot find the autolab SDK")

        self.inst = sdk.Instrument()
        self.connect()
        self.proc = None


    def connect(self):
        """connect to the instrument
        """
        self.inst.HardwareSetupFile = self.hwsetupf
        self.inst.AutolabConnection.EmbeddedExeFileToStart = self.micsetupf
        self.inst.Connect()
        log.info("Connected to Autolab")


    def set_cell(self, onoff):
        """turn the cell on or off

        Args:
            onoff (str): "on" or "off" for the cell
        """
        if onoff == 'on':
            log.info("turning cell on")
            self.inst.Ei.CellOnOff = 1

        elif onoff == 'off':
            log.info("turning cell off")
            self.inst.Ei.CellOnOff = 0

        elif onoff == 'na':
            log.info("no action for cell")


    def abort(self):
        """abort the current procedure
        """
        try:
            self.proc.Abort()
            log.info("procedure aborted")
        except:
            log.info("Failed to abort, no procedure is loaded")


    def disconnect(self):
        """ disconnect from the instrument
        """
        self.proc.Abort()
        self.inst.Disconnect()
        log.info("Disconnected from Autolab")


    def set_stability(self, stability):
        """set the stability of the instrument

        Args:
            stability (str): "high", "low"
        """

        if stability=="high":
            log.info("setting stability to high")
            self.inst.Ei.Bandwith = 2
        else:
            log.info("setting stability to low")
            self.inst.Ei.Bandwith = 1


    def load_procedure(self, name):
        """load a procedure

        Args:
            name (str): name of the procedure
        """
        self.proc = self.inst.LoadProcedure(self.proceduresd[name])
        log.info(f"procedure {name} loaded")


    def potential(self):
        """get the current of the instrument vs. reference electrode

        Returns:
            float: current pottential
        """
        applied_potential = float(self.inst.Ei.get_Potential())
        log.info(f"current potential vs. reference electrode is {applied_potential}")
        return applied_potential


    def applied_potential(self):
        """get the applied potential of the instrument vs. reference electrode

        Returns:
            flaot: applied potential
        """
        current_potential = float(self.inst.Ei.PotentialApplied)
        log.info(f"current applied potential vs. reference electrode is {current_potential}")
        return current_potential


    def current(self):
        """get the current of the instrument vs. reference electrode

        Returns:
            _type_: float
        """
        current = float(self.inst.Ei.Current)
        log.info(f"applied current vs. reference electrode is {current}")
        return current


    def measure_status(self):
        """check if the instrument is measuring

        Returns:
            _type_: bool
        """
        try:
            return self.proc.IsMeasuring
        except:
            log.info("no procedure is loaded")
            return False


    def set_current_range(self, current_range):
        """_summary_

        Args:
            current_range (str): set the current range of the instrument
        """

        if current_range == "10A":
            self.inst.Ei.CurrentRange = 1

        elif current_range == "1A":
            self.inst.Ei.CurrentRange = 0

        elif current_range == "100A":
            self.inst.Ei.CurrentRange = -1

        elif current_range == "10mA":
            self.inst.Ei.CurrentRange = -2

        elif current_range == "1mA":
            self.inst.Ei.CurrentRange = -3

        elif current_range == "100uA":
            self.inst.Ei.CurrentRange = -4

        elif current_range == "10uA":
            self.inst.Ei.CurrentRange = -5

        elif current_range == "1uA":
            self.inst.Ei.CurrentRange = -6

        elif current_range == "100nA":
            self.inst.Ei.CurrentRange = -7

        elif current_range == "10nA":
            self.inst.Ei.CurrentRange = -8


    def set_setpoints(self, setpoints):
        """set the setpoints of the procedure

        Args:
            setpoints (dict): a dictionary of the procedure's parameters
        """
        for comm, params in setpoints.items():

            if  params is None:
                log.info(f"no parameters for {comm}")
                continue

            for param, value in params.items():
                self.proc.Commands[comm].CommandParameters[param].Value = value

    # This function needs to be modified to work with the bokeh visualizer properly
    async def visualize_measurement(self, measurement_type):
        """an async function to run while the instrument is measuring used for the visualizer

        Args:
            measurement_type (str): the type of measurement for plotting
        """

        start_time = copy(time.monotonic())

        while self.proc.IsMeasuring:
            freq = 100  # not to cause an exception
            sleep(0.5)
            current_time = copy(time.monotonic())

            measure_time = current_time-start_time

            if measurement_type == 'impedance':
                try:
                    # get the parameters of the measurement
                    freq = self.proc.FraCommands['FIAScan'].get_FIAMeasurement().Frequency
                    hreal = self.proc.FraCommands['FIAScan'].get_FIAMeasurement().H_Real
                    imag = self.proc.FraCommands['FIAScan'].get_FIAMeasurement().H_Imaginary
                    phase = self.proc.FraCommands['FIAScan'].get_FIAMeasurement().H_Phase
                    modulus = self.proc.FraCommands['FIAScan'].get_FIAMeasurement().H_Modulus
                    log.info(f"frequency: {freq}, real: {hreal}, imaginary: {imag},\
                                phase: {phase}, modulus: {modulus}")
                    await self.queue.put([measure_time, freq, 0.0, 0.0, hreal, imag,
                                          phase, modulus, 0.0])

                except:
                    log.info("no measurement yet")

                await asyncio.sleep(0.6)

            elif measurement_type == 'tCV':

                measured_current = self.current()
                measured_potential = self.potential()
                log.info(f"time: {measure_time}, measured current: {measured_current},\
                            measured potential: {measured_potential}")

                await self.queue.put([measure_time, 0.0, measured_potential,
                                      0.0, 0.0, 0.0, 0.0, 0.0, measured_current])
                await asyncio.sleep(0.4)


    def parse_nox(self, conf):
        """parse the nox file to get the procedure's parameters as a json dictionary

        Args:
            conf (dict): a dictionary of the procedure's parameters

        Returns:
            data(dict): a dictionary of the data and procedure's parameters
        """

        path = os.path.join(conf['safepath'],conf['filename'])
        self.finishedProc = self.inst.LoadProcedure(path)
        self.data = {}
        for comm in conf['parseinstructions']:
            names = [str(n) for n in self.finishedProc.Commands[comm].Signals.Names]
            self.data[comm] = {n: [float(f) for f in self.finishedProc.Commands[comm].Signals.get_Item(n).Value] for n in names}
        with open(path.replace('.nox', '_data.json'), 'w') as f:
            json.dump(self.data, f)

        return self.data

    def parseFRA(self,conf):
        path = os.path.join(conf['safepath'],conf['filename'])
        self.finishedProc = self.inst.LoadProcedure(path)

        self.data = {} 
        comm = 'FHLevel'   
        names = [str(n) for n in self.finishedProc.Commands[comm].Signals.Names]
        self.data[comm] = {n: [float(f) for f in self.finishedProc.Commands[comm].Signals.get_Item(n).Value] for n in names}
        
        self.fradata = {i:[] for i in range(578)} #2537 #7337
        for o in range(578):
            myComm = self.finishedProc.FraCommands.get_Item(o)
            sig_names = [n for n in myComm.Signals.Names]    
            for n in sig_names:
                if not type(myComm.Signals.get_Item(n).Value) == None:
                    try:
                        if type(myComm.Signals.get_Item(n).Value)==float:
                            self.fradata[o].append({n:myComm.Signals.get_Item(n).Value})
                        else:
                            self.fradata[o].append({n:[float(f) for f in myComm.Signals.get_Item(n).Value]})
                    except:
                        print('.')
        self.analyse_data = {i: [] for i in range(220)}
        j = 0
        for i in range(578):
            if len(self.fradata[i]) > 7:
                #if len(data[i][1]['Frequency']) == 1: 
                self.analyse_data[j].append(self.fradata[i])
                j += 1

        self.final_result = self.analyse_data.copy()
        self.final_result.update(self.data)

        with open(path.replace('.nox', '_data.json'), 'w') as f:
            json.dump(self.final_result, f)

        return self.final_result


    async def performMeasurement(self, procedure,setpoints,plot,onoffafter,safepath,filename, parseinstruction):
        conf = dict(procedure=procedure,setpoints=setpoints,
                     plot=plot,onoffafter=onoffafter,safepath=safepath,filename=filename,parseinstructions=parseinstruction)
        #LOAD PROCEDURE
        self.load_procedure(conf['procedure'])
        #SET SETPOINTS
        self.set_setpoints(conf['setpoints'])
        #MEASURE
        self.proc.Measure()
        #PLOT LIVE
        await self.visualize_measurement(conf['plot'])
        #CELL ON/OFF
        self.set_cell(conf['onoffafter'])
        #SAVE
        sleep(0.3) #give the potentiostat some time to stwich everything off and save the data
        print("going to save some stuff")
        self.proc.SaveAs(os.path.join(conf['safepath'],conf['filename']))
        print("going to save in a selected folder")
        json.dump(conf,open(os.path.join(conf['safepath'],conf['filename'].replace('.nox','_conf.json')),'w'))
        print("data is saved safety now")
        sleep(0.1)
        if conf['procedure'] == 'ms':
            data = self.parseFRA(conf)    
        else: 
            data = self.parse_nox(conf)
        print("going out from measuring folder")
        sleep(0.1)
        return data
