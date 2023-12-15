""" Contains the analysis driver for the autolab driver with Madap. """
import os

from madap.echem.voltammetry import voltammetry_CA, voltammetry_CP, voltammetry_CV

from mischbares.logger import logger
from mischbares.utils import utils
from madap.data_acquisition import data_acquisition as da



log = logger.get_logger("autolab_driver")

class MadapArgs:
    # pylint: disable=too-many-instance-attributes
    """This class implements the arguments"""
    eis_plots = ["nyquist" ,"nyquist_fit", "residual", "bode"]
    arrhenius_plots = ["arrhenius", "arrhenius_fit"]
    ca_plots = ["CA", "Log_CA", "CC", "Cottrell", "Anson", "Voltage"]
    cp_plots = ["CP", "CC", "Cottrell", "Voltage_Profile", "Potential_Rate", "Differential_Capacity"]


    def __init__(self, db_procedure, measurement_id):
        experiment_id = db_procedure.get_experiment_id_by_measurement_id(measurement_id)["experiment_id"][0]
        experiment_args = db_procedure.get_experiment(int(experiment_id))
        self.procedure = None
        self.impedance_procedure= None
        self.file = None
        self.plots = None
        self.results = None
        self.header_list = None
        self.specific= None
        self.cell_constant = None
        self.suggested_circuit = None
        self.initial_values = None
        self.upper_limit_quantile = None
        self.lower_limit_quantile = None
        self.applied_current = None
        self.measured_current_units = "A" # Standard Potentionstat units
        self.measured_time_units = "s" # Standard Potentionstat units
        self.applied_voltage = None
        self.mass_of_active_material = experiment_args["mass_of_active_material"][0]
        self.electrode_area = experiment_args["electrode_area"][0]
        self.concentration_of_active_material = experiment_args["concentration_of_active_material"][0]
        self.number_of_electrons = experiment_args["number_of_electrons"][0]
        self.cycle_list = None
        self.penalty_value = None
        self.temperature = None
        self.window_size = None

class AnalysisDriver():
    def __init__(self, procedure_configuration, data, parse_instruction, db_procedure, measurement_id):
        self.procedure_configuration = procedure_configuration
        self.parse_instruction = parse_instruction
        self.data = data
        self.procedure=self.procedure_configuration["procedure"]
        self.madap_args = MadapArgs(db_procedure, measurement_id)
        self.call_madap()


    def call_madap(self):
        """Perform the analysis with Madap"""
        result_dir = utils.create_dir(os.path.join(self.procedure_configuration["save_dir"], self.procedure))
        self.analysis_cls = self.create_analysis_class()
        self.analysis_cls.perform_all_actions(save_dir=result_dir, plots=self.madap_args.plots)


    def create_analysis_class(self):
        """create the class for the analysis

        Returns:
            class: the class for the analysis
        """
        if self.procedure == "ca":
            self.madap_args.plots = self.madap_args.ca_plots
            current_data = self.data[self.parse_instruction[0]]["WE(1).Current"]
            voltage_data = self.data[self.parse_instruction[0]]["WE(1).Potential"]
            time_data = self.data[self.parse_instruction[0]]["Corrected time"]
            charge_data = self.data[self.parse_instruction[0]]["WE(1).Charge"]
            return voltammetry_CA.Voltammetry_CA(current=da.format_data(current_data),
                                                 voltage=da.format_data(voltage_data),
                                                 time=da.format_data(time_data),
                                                 charge=da.format_data(charge_data),
                                                 args=self.madap_args)
        if self.procedure == "cp":
            self.madap_args.plots = self.madap_args.cp_plots
            current_data = self.data[self.parse_instruction[0]]["WE(1).Current"]
            voltage_data = self.data[self.parse_instruction[0]]["WE(1).Potential"]
            time_data = self.data[self.parse_instruction[0]]["Corrected time"]
            charge_data = self.data[self.parse_instruction[0]]["WE(1).Charge"]
            return voltammetry_CP.Voltammetry_CP(current=da.format_data(current_data),
                                                 voltage=da.format_data(voltage_data),
                                                 time=da.format_data(time_data),
                                                 charge=da.format_data(charge_data),
                                                 args=self.madap_args)
        if self.procedure == "cv":
            self.madap_args.plots = self.madap_args.cv_plots
            return voltammetry_CV.Voltammetry_CV()
        else:
            log.error("Procedure %s not supported", self.procedure)
            return None

    def create_args(self):
        """create the arguments for the analysis"""
        if self.procedure == "ca":
            self.madap_args.applied_voltage = self.procedure_configuration["setpoints"]["applypotential"]["Setpoint value"]
        if self.procedure == "cp":
            self.madap_args.applied_current = self.procedure_configuration["setpoints"]["applycurrent"]["Setpoint value"]
