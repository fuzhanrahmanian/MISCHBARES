"""main config file for sdc_2"""

import socket
from mischbares.config.autolab_config import autolab_config


config = {}

ip_adress = socket.gethostbyname(socket.gethostname())
print(f"ip adress is {ip_adress}")

config["servers"] = dict(autolabDriver = dict(host=ip_adress, port=15111), # autolab
                         autolab = dict(host=ip_adress, port = 15112),
                         orchestrator=dict(host=ip_adress, port=15115),
                         hamiltonDriver=dict(host=ip_adress, port=16049, qc_motor="langDriver",
                                                                         qc_motor_safe_pos=['lang', 'langAction', 'safe_waste_pos']),
                         hamilton=dict(host=ip_adress, port=16050),
                         langDriver=dict(host=ip_adress, port=15211),
                         lang=dict(host=ip_adress, port=15212))

config['orchestrator'] = dict(path='data')#, kadiurl="http://127.0.0.1:13377")
config['instrument'] = "SDC"
config['procedures'] = {"ocp": "recordsignal",  "ca": "recordsignal", "cp": "recordsignal",\
                        "cv_staircase": "FHCyclicVoltammetry2", "eis": 'FIAMeasPotentiostatic',\
                        } #"lissajous": ['FIAMeasPotentiostatic', 'FIAMeasurement']
config['pump'] = {"Hamilton": {"path": r'C:\Program Files (x86)\Hamilton Company\ML600 Programming Helper Tool',
                               "dlls": ['Hamilton.Components.TransportLayer.ComLink',
                                        'Hamilton.Components.TransportLayer.Discovery',
                                        'Hamilton.Components.TransportLayer.HamCli',
                                        'Hamilton.Components.TransportLayer.Protocols',
                                        'Hamilton.MicroLab.MicroLabDaisyChain',
                                        'Hamilton.Module.ML600'],
                               "IP": "192.168.31.235",
                               "conf": dict(left=dict(syringe=dict(volume=1000000,
                                                                    flowRate=50000,#nL/s
                                                                    initFlowRate=50000),
                                                                    valve=dict(prefIn=1,prefOut=3)),
                                            right=dict(syringe=dict(volume=1000000,
                                                                    flowRate=50000,
                                                                    initFlowRate=50000),
                                                                    valve=dict(prefIn=2,prefOut=1)))}}

config['lang'] = dict(langDriver= dict(velocity_x=5, velocity_y=5, velocity_z=5,
                            serial_port='COM3',
                            path_pylang=r"C:\Users\LaborRatte23-3\Documents\git\pyLang"),
                      langAction = dict(safe_home_pos=[0.0, 0.0, 0.0],
                                        safe_waste_pos=[0.0, -35.0, 0.0],
                                        safe_clean_pos_1=[81.0, -35.0, 7],
                                        safe_clean_pos_2=[74.0, -35.0, 0.0],
                                        safe_sample_pos=[0.0, 0.0, 0.0]))

config["QC"] = dict(waste_camera=dict(camera_num=0,offset_x=40, offset_y=120, delay=10, timeout=60),
                    telegram=dict(api_token="", chat_id=""))
# TEST POISTION FOR THE LANG QC: [45.7, 27.2, 15.2]
config.update(autolab_config)
