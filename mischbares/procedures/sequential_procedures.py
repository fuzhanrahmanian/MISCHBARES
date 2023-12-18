"""This will be used an sequential experimenation on the substrate is needed"""
import json
from datetime import datetime
from mischbares.logger import logger
from mischbares.config.main_config import config


log = logger.get_logger("autolab_procedures")

def perfom_sequential_experiment(soe_autolab, params_autolab,
                current_range_autolab, sample_position):

    sample_x_pos = sample_position[0]
    sample_y_pos = sample_position[1]
    sample_height = sample_position[2]
    initial_height = sample_height - 3.0
    cleaning_pos = config['lang']['lanAction']['safe_clean_pos_2']
    # move to waste/ dispense / go a bit to right / asipirate a little bit back /
    # go and clean yourself / go up first / gohome / go to sample until its heigh -3 /
    # move down to the substrate / set the range of autolab
    soe_preparation = ['lang/moveWaste_0', 'hamilton/pumpR_0','lang/moveWaste_1',
                       'hamilton/pumpR_1', 'lang/RemoveDroplet_0', 'lang/moveAbs_0',
                       'lang/moveAbs_1','lang/moveAbs_2', 'lang/moveAbs_3',
                       'lang/moveDown_0', 'autolab/setcurrentrange_0']
    params_preparation = {'moveWaste_0': {'x_pos':0, 'y_pos':0, 'z_pos':0},
                        'pumpR_0': {'volume':600},
                        'moveWaste_1': {'x_pos':5, 'y_pos':0, 'z_pos':0},
                        'pumpR_1': {'volume': -20},
                        'RemoveDroplet_0': {'x_pos':0, 'y_pos':0, 'z_pos':0},
                        'moveAbs_0': {'dx': cleaning_pos, 'dy': cleaning_pos, 'dz': 0},
                        'moveAbs_1': {'dx': 0, 'dy': 0, 'dz': 0},
                        'moveAbs_2': {'dx': sample_x_pos, 'dy': sample_y_pos, 'dz': 0},
                        'moveAbs_3': {'dx': sample_x_pos, 'dy': sample_y_pos, 'dz': initial_height},
                        'moveDown_0': {'dz': 3.0, 'steps': 20},
                        'setcurrentrange_0': {'crange': current_range_autolab}}

    # pump back a bit, go up, move home
    soe_post_up = ['hamilton/pumpR_2', 'lang/moveAbs_4', 'lang/moveAbs_5']
    params_post_up = {'pumpR_2': {'volume': -20},
                      'moveAbs_4': {'dx': sample_x_pos, 'dy': sample_y_pos, 'dz': 0},
                      'moveAbs_5': {'dx': 0, 'dy': 0, 'dz': 0}}

    soe = soe_preparation + soe_autolab + soe_post_up
    params = {**params_preparation, **params_autolab, **params_post_up}
    sequence = dict(soe, params, sequence)

    return soe, params, sequence
