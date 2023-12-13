"""configuration file for autolab"""
# autolab_config contains of autolabDriver and autolab keys
# in the autolabDriver section, the driver to use is specified.
# in the autolab the url and procedures will be described
import os
import socket

config_path, _ = os.path.split(__file__)

autolab_config = {}

ip_adress = socket.gethostbyname(socket.gethostname())

autolab_config['autolabDriver'] = dict(basep = os.path.join(config_path, 'autolab_configuration',
                                        'Autolab SDK 1.11'),
                procp = os.path.join(config_path, 'electrochemical_procedures'),
                hwsetupf = os.path.join(config_path, 'autolab_configuration',
                                        '12.0', 'HardwareSetup.AUT88173.xml'),
                micsetupf = os.path.join(config_path, 'autolab_configuration', 'Autolab SDK 1.11',
                                        'Hardware Setup Files', 'Adk.bin'),
                proceuduresd = {'cp': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CP_MISCHBARES.nox'),
                                'ca': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CA_MISCHBARES.nox'),
                                'cv_linear': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CV_LINEAR_MISCHBARES.nox'),
                                'cv_staircase': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CV_STAIRCASE_MISCHBARES.nox'),
                                'eis': os.path.join(config_path, 'electrochemical_procedures',
                                                    'EIS_MISCHBARES.nox'),
                                'eis_reverse': os.path.join(config_path,'electrochemical_procedures',
                                                'EIS_MISCHBARES_REVERSE.nox'),
                                'lissajous': os.path.join(config_path, 'electrochemical_procedures',
                                                          'LISSAJOUS_MISCHBARES.nox'),
                                'on': os.path.join(config_path, 'electrochemical_procedures',
                                                   'ON.nox'),
                                'off': os.path.join(config_path, 'electrochemical_procedures',
                                                    'OFF.nox'),
                                'ocp_cv': os.path.join(config_path, 'electrochemical_procedures',
                                                       'OCP_CV.nox'),
                                'ocp': os.path.join(config_path, 'electrochemical_procedures',
                                                    'OCP_MISCHBARES.nox')})

# action should get the driver url
autolab_config['autolab'] = dict(url = f'http://{ip_adress}:15474')
