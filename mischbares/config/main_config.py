"""main config file for sdc_2"""

import socket
from mischbares.config.autolab_config import autolab_config


config = {}

ip_adress = socket.gethostbyname(socket.gethostname())

config["servers"] = dict(autolabDriver = dict(host=ip_adress, port=15474), # autolab
                         autolab = dict(host=ip_adress, port = 15475),
                         orchestrator=dict(host=ip_adress, port=15480))

config['orchestrator'] = dict(path='data')#, kadiurl="http://127.0.0.1:13377")
config['instrument'] = "SDC"
config['procedures'] = {"ocp": "recordsignal",  "ca": "recordsignal", "cp": "recordsignal",\
                        "cv_staircase": "FHCyclicVoltammetry2", "eis": 'FIAMeasPotentiostatic',\
                        } #"lissajous": ['FIAMeasPotentiostatic', 'FIAMeasurement']
config.update(autolab_config)
