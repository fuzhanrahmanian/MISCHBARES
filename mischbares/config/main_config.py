"""main config file for sdc_2"""

import socket
from mischbares.config.autolab_config import autolab_config


config = {}

ip_adress = socket.gethostbyname(socket.gethostname())

config["servers"] = dict(autolabDriver = dict(host=ip_adress, port=15374), # autolab
                         autolab = dict(host=ip_adress, port = 15375),
                         orchestrator=dict(host=ip_adress, port=15380))

config['orchestrator'] = dict(path='data')#, kadiurl="http://127.0.0.1:13377")
config['instrument'] = "SDC"

config.update(autolab_config)
