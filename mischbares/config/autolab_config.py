"""configuration file for autolab"""
# autolab_config contains of autolabDriver and autolab keys
# in the autolabDriver section, the driver to use is specified.
# in the autolab the url and procedures will be described
import os

config_path, _ = os.path.split(__file__)

autolab_config = {}

autolab_config['autolabDriver'] = dict(basep = os.path.join(config_path, 'autolab_configuration',
                                        'Autolab SDK 1.11'),
                procp = os.path.join(config_path, 'electrochemical_procedures'),
                hwsetupf = os.path.join(config_path, 'autolab_configuration',
                                        '12.0', 'HardwareSetup.AUT88173.xml'),
                micsetupf = os.path.join(config_path, 'autolab_configuration', 'Autolab SDK 1.11',
                                        'Hardware Setup Files', 'Adk.bin'),
                proceuduresd = {'cp': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CP.nox'),
                                'ca': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CA.nox'),
                                'cv': os.path.join(config_path, 'electrochemical_procedures',
                                                   'CV.nox'),
                                'eis': os.path.join(config_path, 'electrochemical_procedures',
                                                    'EIS.nox'),
                                'on': os.path.join(config_path, 'electrochemical_procedures',
                                                   'ON.nox'),
                                'off': os.path.join(config_path, 'electrochemical_procedures',
                                                    'OFF.nox'),
                                'ocp_cv': os.path.join(config_path, 'electrochemical_procedures',
                                                       'OCP_CV.nox'),
                                'ocp': os.path.join(config_path, 'electrochemical_procedures',
                                                    'OCP_record_signal.nox')})

# action should get the driver url
autolab_config['autolab'] = dict(url = 'http://192.168.31.121:13374')
