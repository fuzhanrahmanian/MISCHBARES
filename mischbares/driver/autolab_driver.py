"""autolab dirver"""
import os
import sys
import time
from time import sleep
from copy import copy
import asyncio
import numpy as np
import clr

from mischbares.logger import logger
from mischbares.utils import utils

log = logger.get_logger("autolab_driver")

class Autolab:
    """autolab class for defining the base functions of Metrohm instrument.
    """

    def __init__(self, autolab_conf):
        #init a Queue for the visualizer
        self.queue = asyncio.Queue() # loop=asyncio.get_event_loop()
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
        except Exception as exp:
            log.error(f"Cannot find the autolab SDK. With error {exp}")
            sys.exit()

        self.inst = sdk.Instrument()
        self.connect()
        self.proc = None
        self._save_dir = None
        self._optional_name = None
        self.finished_procedure = None
        self.data = None
        self.current_range_procedure_setting = dict(ca = "switchpotentiostatic",
                                                    cp = "switchgalvanostatic",
                                                    eis = "Autolab control")
        self.ocp_procedure_setting = dict(ca = "applypotential0",
                                          cp = "applycurrent0",
                                          eis = "Set potential")

    @property
    def save_dir(self):
        """get the save directory.

        Returns:
            str: save directory.
        """
        return self._save_dir


    @property
    def optional_name(self):
        """get the optional name.

        Returns:
            str: optional name.
        """
        return self._optional_name


    @save_dir.setter
    def save_dir(self, save_dir):
        """set the save directory.

        Args:
            save_dir (str): save directory.
        """
        self._save_dir = save_dir


    @optional_name.setter
    def optional_name(self, optional_name):
        """set the optional name.

        Args:
            optional_name (str): optional name.
        """
        self._optional_name = optional_name


    def connect(self):
        """connect to the instrument.
        """
        try:
            self.inst.HardwareSetupFile = self.hwsetupf
            self.inst.AutolabConnection.EmbeddedExeFileToStart = self.micsetupf
            self.inst.Connect()
            log.info("Connected to Autolab")
        except Exception as exp:
            log.error(exp)
            sys.exit()


    def set_cell(self, onoff):
        """turn the cell on or off.

        Args:
            onoff (str): "on" or "off" for the cell.
        """
        if onoff == 'on':
            log.info("turning cell on")
            self.inst.Ei.CellOnOff = 1

        elif onoff == 'off':
            log.info("turning cell off")
            self.inst.Ei.CellOnOff = 0

        elif onoff == 'na':
            log.info("no action for cell")

    # reset the instrument
    def reset(self):
        """reset the instrument.
        """
        self.set_cell("off")
        self.set_cell("on")
        log.info("instrument reset")


    def abort(self):
        """abort the current procedure.
        """
        try:
            self.proc.Abort()
            log.info("procedure aborted")
        except:
            log.info("Failed to abort, no procedure is loaded")


    def disconnect(self):
        """ disconnect from the instrument.
        """
        self.proc.Abort()
        self.inst.Disconnect()
        log.info("Disconnected from Autolab")


    def set_stability(self, stability):
        """set the stability of the instrument.

        Args:
            stability (str): "high", "low".
        """

        if stability=="high":
            log.info("setting stability to high")
            self.inst.Ei.Bandwith = 2
        else:
            log.info("setting stability to low")
            self.inst.Ei.Bandwith = 1


    def load_procedure(self, name):
        """load a procedure.

        Args:
            name (str): name of the procedure.
        """
        try:
            self.proc = self.inst.LoadProcedure(self.proceduresd[name])
            log.info(f"procedure {name} loaded")
        except Exception as exp:
            log.error(exp)
            sys.exit()


    def potential(self):
        """get the current of the instrument vs. reference electrode.

        Returns:
            float: current pottential.
        """
        current_potential = float(self.inst.Ei.get_Potential())
        log.info(f"current potential vs. reference electrode is {current_potential}")
        return current_potential


    def applied_potential(self):
        """get the applied potential of the instrument vs. reference electrode.

        Returns:
            flaot: applied potential.
        """
        applied_potential = float(self.inst.Ei.PotentialApplied)
        log.info(f"current applied potential vs. reference electrode is {applied_potential}")
        return applied_potential


    def current(self):
        """get the current of the instrument vs. reference electrode.

        Returns:
            current (float): current value.
        """
        current = float(self.inst.Ei.Current)
        log.info(f"applied current vs. reference electrode is {current}")
        return current


    def measure_status(self):
        """check if the instrument is measuring.

        Returns:
            bool: True if measuring, False if not.
        """
        try:
            return self.proc.IsMeasuring
        except:
            log.info("no procedure is loaded")
            return False


    def set_current_range(self, current_range):
        """set the current range of the instrument.

        Args:
            current_range (str): set the current range of the instrument.
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

        log.info(f"current range set to {current_range}\
                with the value {self.inst.Ei.CurrentRange}")
        return self.inst.Ei.CurrentRange


    def set_setpoints(self, procedure, setpoints, current_range):
        """set the setpoints of the procedure.

        Args:
            procedure (str): name of the procedure.
            setpoints (dict): a dictionary of the procedure's parameters.
            current_range (str): the current range of the instrument.
        """
        if procedure in list(self.current_range_procedure_setting.keys()):
            # set the current range
            new_current_range = self.set_current_range(current_range)

            # change current range in the correcponded experiment
            current_comm = self.current_range_procedure_setting[procedure]
            self.proc.Commands[current_comm].CommandParameters["WE(1).Current range"].Value = \
                                                                                    new_current_range
            log.info(f"current range set to {current_range} in procedure {procedure} \n \
                        the experment settings are {setpoints}")

        if  setpoints is None or setpoints == {}:
            log.info(f"no parameters for {procedure}")

        else:
            for comm, params in setpoints.items():

                for param, value in params.items():
                    self.proc.Commands[comm].CommandParameters[param].Value = value
                    log.info(f"set {param} to {value}")


    def set_ocp_value(self, procedure, ocp_value):
        """ set the ocp potential or current of the procedure.
        Args:
            procedure (str): name of the procedure.
            ocp_value (float): ocp potential or current value.
        """
        ocp_command = self.ocp_procedure_setting[procedure]
        self.proc.Commands[ocp_command].CommandParameters["Setpoint value"].Value = ocp_value


    async def get_ocp_on_the_fly(self):
        """get the on the fly OCP value as initial point for autolab procedures.

        Returns:
            current (float): current value at ocp.
            potential (float): potential value at ocp.
        """
        self.load_procedure	("ocp")
        # measure the procedure for 10 seconds
        self.proc.Measure()

        await asyncio.sleep(10)

        # extracting the OCP values
        ocp_values = []
        for ocp_item in ['WE(1).Current', 'WE(1).Potential']:
            extracted_values =\
                list(self.proc.Commands['recordsignal'].Signals.get_Item(ocp_item).Value)
            log.info(f"extracted {ocp_item} value: {extracted_values}")

            # due to oscillation, an averaged value is used
            ocp_values.append(np.mean(extracted_values[-5:]))

        # empty the procedure
        self.proc = None
        # first value is the current, second value is the potential
        return ocp_values[0], ocp_values[1]


    # This function needs to be modified to work with the bokeh visualizer properly
    # Todo
    async def visualize_measurement(self, measurement_type):
        """an async function to run while the instrument is measuring used for the visualizer.

        Args:
            measurement_type (str): the type of measurement for plotting.
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


    def parse_nox(self, parse_instruction, save_dir = None, optional_name = None):
        """parse the data from the saved nox file

        Args:
            parse_instruction (str): the instruction for parsing the data.
            save_dir (str, optional): save directory. Defaults to None.
            optional_name (str, optional): optional file name. Defaults to None.

        Returns:
            data (dict): extracted data
        """
        # get the saved procedure and parse it
        if save_dir:
            self.save_dir = save_dir
        if optional_name:
            self.optional_name = optional_name

        # load the finished procedure
        log.info(f"loading procedure from {self.save_dir} with filename {self.optional_name}")
        self.finished_procedure = self.inst.LoadProcedure(
                                        os.path.join(self.save_dir, f"{self.optional_name}.nox"))

        self.data = {}
        # check if the procedure is a list
        if not isinstance(parse_instruction, list):
            parse_instruction = [parse_instruction]
        for comm in parse_instruction:
            # get the procedure's parameters
            names = [str(n) for n in self.finished_procedure.Commands[comm].Signals.Names]
            # get the data for each parameter
            self.data[comm] = {n: [float(f) for f in \
                                self.finished_procedure.Commands[comm].Signals.get_Item(n).Value] \
                               for n in names}
        utils.save_data_as_json(directory = self.save_dir, data = self.data, \
                                name = self.optional_name.replace('.nox', '.json'))

        return self.data



    async def perform_measurement(self, procedure, plot_type,
                                    parse_instruction, save_dir,
                                    setpoints = None, current_range = "1mA",
                                    on_off_status = "off",
                                    optional_name = None, measure_at_ocp = False):
        """perform the measurement

        Args:
            procedure (str): the procedure to be performed.
            plot_type (str): the type of plot.
            parse_instruction (list[str]): the instruction for parsing the data.
            save_dir (str): save directory.
            setpoints (dict): the setpoints of the procedure.
            current_range (str): the current range. Defaults to "1mA".
            on_off_status (str): the status of the instrument. Defaults to "off".
            optional_name (str): optional file name. Defaults to None.
            measure_at_ocp (bool): whether to measure at ocp. Default is False.
        Returns:
            data (dict): extracted data from the nox file of the procedure.
        """

        # define a save path for saving th nox files of the measurements
        save_dir = utils.create_dir(os.path.join(save_dir, "data"))
        log.info(f"The procedure path is {save_dir}")

        # create a file name for the nox file
        name = utils.assemble_file_name(self.__class__.__name__, optional_name) if \
                optional_name else utils.assemble_file_name(self.__class__.__name__)

        if measure_at_ocp:
            if procedure == "cp":
                ocp_value, _ = await self.get_ocp_on_the_fly()

            elif procedure == "ca" or procedure == "eis":
                _, ocp_value = await self.get_ocp_on_the_fly()

            else:
                log.error("The procedure is not supported for measuring at OCP")

        # load the procedure
        self.load_procedure(procedure)
        if measure_at_ocp:
            self.set_ocp_value(procedure, ocp_value)

        log.info(f"loading the procedure {procedure}")

        # set the setpoints
        self.set_setpoints(procedure, setpoints, current_range)

        # measure the procedure
        self.proc.Measure()
        log.info("measuring the procedure")
        #
        # Todo
        # visualize the measurement live while it is being measured
        await self.visualize_measurement(plot_type)

        # cell status after measurement
        self.set_cell(on_off_status)

        # time required for switching the cell off and save the data
        await asyncio.sleep(2)
        self.proc.SaveAs(os.path.join(save_dir, f"{name}.nox"))

        # make a configuration of the procedure
        procedure_configuration = dict(procedure = procedure, setpoints = setpoints,
                                    plot_type = plot_type, on_off_status = on_off_status,
                                    save_dir = save_dir, file_name= name,
                                    parse_instructions = parse_instruction)

        utils.save_data_as_json(directory = save_dir, data = procedure_configuration,
                                name = f"{name}_configuration")
        await asyncio.sleep(0.2)

        data = self.parse_nox(parse_instruction = parse_instruction,
                              save_dir = save_dir, optional_name = name)
        await asyncio.sleep(0.2)
        log.info(f"finished measuring and saving procedure {procedure}")

        return data
