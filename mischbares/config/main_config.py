"""main config file for sdc_2"""

import socket
from mischbares.config.autolab_config import autolab_config


config = {}

ip_adress = socket.gethostbyname(socket.gethostname())
print(f"ip adress is {ip_adress}")

config["servers"] = dict(autolabDriver = dict(host=ip_adress, port=15111), # autolab
                         autolab = dict(host=ip_adress, port = 15112),
                         orchestrator=dict(host=ip_adress, port=15115))

config['orchestrator'] = dict(path='data')#, kadiurl="http://127.0.0.1:13377")
config['instrument'] = "SDC"
config['procedures'] = {"ocp": "recordsignal",  "ca": "recordsignal", "cp": "recordsignal",\
                        "cv_staircase": "FHCyclicVoltammetry2", "eis": 'FIAMeasPotentiostatic',\
                        } #"lissajous": ['FIAMeasPotentiostatic', 'FIAMeasurement']
config.update(autolab_config)
