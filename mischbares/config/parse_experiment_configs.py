import json
from mischbares.logger import logger


class ParserExperimentConfigs():
    def __init__(self, general_config:str, experiment_config:str, batch_config:str):
        # open the json files
        self.expertiment_configs = json.load(open(experiment_config))
        self.general_configs = json.load(open(general_config))
        self.batch_configs = json.load(open(batch_config))


        # 0,0,1; 0,0.5,1; format this to tuple. One tuple is delimited by ;
        motor_tuple = []
        for motor in self.general_configs['motor_pos']:
            motor_tuple.append(tuple(map(float, motor.split(','))))
        self.general_configs['motor_pos'] = motor_tuple

        # Check that the len of motor positions is the same as the len of the length of batch configs#
        if len(self.general_configs['motor_pos']) != len(self.batch_configs):
            raise ValueError("The length of the motor positions and the potentials is not the same.")
