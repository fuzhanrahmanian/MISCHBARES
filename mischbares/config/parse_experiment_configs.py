import json
from mischbares.logger import logger


class ParserExperimentConfigs():
    def __init__(self, general_config:str, experiment_config:str, batch_config:str):
        # open the json files
        self.experiment_configs = json.load(open(f"saved_config/{experiment_config}"))
        self.general_configs = json.load(open(f"saved_config/{general_config}"))
        self.batch_configs = json.load(open(f"saved_config/{batch_config}"))
        # parse the configs
        self.parse_general_config()
        self.parse_experiment_config()


    def parse_general_config(self):
        """This function will parse the general config file. The following keys will be parsed:
        - number_of_electrons
        - electrode_area
        - concentration_of_active_material
        - mass_of_active_material
        - motor_pos
        """
        # number of electrones to int
        self.general_configs['number_of_electrons'] =\
            int(self.general_configs['number_of_electrons'])
        # electrode_area to float
        self.general_configs['electrode_area'] =\
            float(self.general_configs['electrode_area'])
        # concentration_of_active_material to float
        self.general_configs['concentration_of_active_material'] =\
            float(self.general_configs['concentration_of_active_material'])
        # mass_of_active_material to float
        self.general_configs['mass_of_active_material'] =\
            float(self.general_configs['mass_of_active_material'])
        # create a list of tuple from motor_pos
        motor_tuple = self.general_configs['motor_pos'].split(';')
        motor_tuple = [tuple(map(float, motor.split(','))) for motor in motor_tuple]


    def parse_experiment_config(self):
        """This function will parse the experiment config file. The following keys will be parsed:
        - num_of_batch
        - num_of_experiment_in_each_batch
        """
        # num_of_batch to int
        self.experiment_configs['num_of_batch'] =\
            int(self.experiment_configs['num_of_batch'])
        # num_of_experiment_in_each_batch to int
        self.experiment_configs['num_of_experiment_in_each_batch'] =\
            int(self.experiment_configs['num_of_experiment_in_each_batch'])

