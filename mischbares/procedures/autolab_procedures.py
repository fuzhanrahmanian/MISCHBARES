""" General assembles autolab procedures for orchestrator and UI"""
import json
from mischbares.logger import logger

log = logger.get_logger("autolab_procedures")
class AutolabProcedures:
    """ General assembles autolab procedures for orchestrator and UI"""

    def __init__(self, measurement_num, current_range = '10mA', save_dir = 'mischbares/tests'):
        self.measurement_num = measurement_num
        self.current_range = current_range
        self.save_dir = save_dir


    def __repr__(self) -> str:
        """Return the representation of the general autolab procedures."""
        return "AutolabProcedures to perform a complete sequence of event by orchestrator"


    # 1. currentRange_ocp
    def ocp_measurement(self, measurement_duration = 10):
        """ocp measurement procedure from orchestrator level.
        Args:
            measurement_duration (int, optional): measurement duration in seconds. Defaults to 10.
        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe = [f'autolab/measure_{self.measurement_num}']
        params = {f'measure_{self.measurement_num}': {'procedure': 'ocp',
                        'plot_type':'tCV',
                        'parse_instruction': json.dumps(['recordsignal']),
                        'save_dir': self.save_dir,
                        'setpoints': json.dumps({'recordsignal':
                                        {'Duration (s)': measurement_duration}}),
                        'current_range': self.current_range,
                        'on_off_status':'off',
                        'optional_name': 'ocp',
                        'measure_at_ocp': False}}
        log.info(f"initiate number {self.measurement_num} of ocp measurement with \n \
                    {params} parameters")
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 2. currentRange_ocp/ca
    def ca_measurement(self, measurement_duration = 10, apply_potential = 0.1,
                       interval_time = 0.5):
        """cyclic ammperometry measurement procedure from orchestrator level.

        Args:
            measurement_duration (int, optional): measurement duration in seconds. Defaults to 10.
            apply_potential (float, optional): apply potential in V. Defaults to 0.1.
            interval_time (float, optional): interval time in seconds. Defaults to 0.5.

        Returns:
            soe (list): list of the sequence of events.
            Params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe = [f'autolab/measure_{self.measurement_num}']
        params = {f'measure_{self.measurement_num}': {'procedure': 'ca',
                            'plot_type':'tCV',
                            'parse_instruction': json.dumps(['recordsignal']),
                            'save_dir': self.save_dir,
                            'setpoints': json.dumps({'applypotential':
                                                {'Setpoint value': apply_potential},
                                                'recordsignal':
                                                    {'Duration (s)': measurement_duration,
                                                    'Interval time (s)': interval_time}}),
                                'current_range': self.current_range,
                                'on_off_status':'off',
                                'optional_name': 'ca',
                                'measure_at_ocp': True}}
        log.info(f"initiate number {self.measurement_num} of ca measurement with \n \
                    {params} parameters")
        sequence = dict(soe=soe, params=params, meta={})
        return soe, params, sequence


    # 3. currentRange_ocp/cp
    def cp_measurement(self, measurement_duration = 10, apply_current = 0.000001,
                       interval_time = 0.5):
        """cyclic potentiometric measurement procedure from orchestrator level.

        Args:
            measurement_duration (int, optional): measurement duration in seconds. Defaults to 10.
            apply_current (float, optional): apply current in A. Defaults to 0.000001.
            interval_time (float, optional): interval time in seconds. Defaults to 0.5.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe = [f'autolab/measure_{self.measurement_num}']
        params = {f'measure_{self.measurement_num}': {'procedure':'cp',
                                'plot_type':'tCV',
                                'parse_instruction': json.dumps(['recordsignal']),
                                'save_dir': self.save_dir,
                                'setpoints': json.dumps({'applycurrent':\
                                            {'Setpoint value': apply_current},
                                            'recordsignal': {'Duration (s)': measurement_duration,
                                            'Interval time (s)': interval_time}}),
                                'current_range': self.current_range,
                                'on_off_status':'off',
                                'optional_name': 'cp',
                                'measure_at_ocp': True}}
        log.info(f"initiate number {self.measurement_num} of cp measurement with \n \
                    {params} parameters")
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 4. currentRange_ocp/eis
    def eis_measurement(self, apply_potential = 0.1, measure_at_ocp = True):
        """electrochemical impedance spectroscopy measurement procedure from orchestrator level.
        Args:
            apply_potential (float, optional): potential in V. Defaults to 0.01.
            integration_time (float, optional): integration time in seconds. Defaults to 0.125.
            integration_cycle (int, optional): integration cycle. Defaults to 1.
            upper_frequency_level (int, optional): upper frequency level in Hz. Defaults to 10000.
            measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """

        soe = [f'autolab/measure_{self.measurement_num}']

        if measure_at_ocp is False:
            experiment_setpoints = {'Set potential':{'Setpoint value': apply_potential}}
        else:
            experiment_setpoints = {}

        params = {f'measure_{self.measurement_num}': {'procedure':'eis',
                                'plot_type':'impedance',
                                'parse_instruction':json.dumps(['FIAMeasPotentiostatic', 'FIAMeasurement']),
                                'save_dir':self.save_dir,
                                'setpoints':json.dumps(experiment_setpoints),
                                'current_range':self.current_range,
                                'on_off_status':'off',
                                'optional_name':'eis',
                                'measure_at_ocp': measure_at_ocp}}

        log.info(f"initiate number {self.measurement_num} of eis measurement with \n \
                    {params} parameters")
        sequence = dict(soe=soe, params=params, meta={})
        return soe, params, sequence


    # 5. currentRange_ocp/ca_ocp/eis
    def ca_eis_measurement(self,measurement_duration = 10, ca_potential = 0.1,
                           ca_interval_time = 0.5, eis_potential = 0.1,
                           eis_measure_at_ocp = True):
        """sequence of cyclic amperometric and electrochemical impedance spectroscopy measurement
            from orchestrator level.
        Args:
            measurement_duration (int, optional): measurement duration in seconds.
                                                Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.1.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration = measurement_duration,
                                        apply_potential = ca_potential,
                                        interval_time = ca_interval_time)
        log.info(f"initiate number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        self.measurement_num += 1

        log.info(f"measurement number {self.measurement_num} of eis measurement with \n \
                    ocp {eis_measure_at_ocp}")
        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                            measure_at_ocp = eis_measure_at_ocp)
        soe = soe_ca + soe_eis
        params = {**params_ca, **params_eis}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 6. currentRange_ocp/eis-ocp/ca
    def eis_ca_measurement(self, measurement_duration = 10, ca_potential = 0.1,
                           ca_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of electrochemical impedance spectroscopy and cyclic amperometric measurement
            from orchestrator level.
        Args:
            measurement_duration (int, optional): measurement duration in seconds.
                                                Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.1.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                    measure_at_ocp = eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of eis measurement with \n \
                   ocp {eis_measure_at_ocp}")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration = measurement_duration,
                                        apply_potential = ca_potential,
                                        interval_time = ca_interval_time)

        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        soe = soe_eis + soe_ca
        params = {**params_eis, **params_ca}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 7. currentRange_ocp/cp-ocp/eis
    def cp_eis_measurement(self, measurement_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and electrochemical impedance spectroscopy measurement
            from orchestrator level.
        Args:
            measurement_duration (int, optional): measurement duration in seconds.
                                                Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = measurement_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)

        log.info(f"initiate number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        log.info(f"measurement number {self.measurement_num} of eis measurement with \n \
                    ocp {eis_measure_at_ocp}")

        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                            measure_at_ocp = eis_measure_at_ocp)

        soe = soe_cp + soe_eis
        params = {**params_cp, **params_eis}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 8. currentRange_ocp/eis-ocp/cp
    def eis_cp_measurement(self, measurement_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and electrochemical impedance spectroscopy measurement
            from orchestrator level.
        Args:
            measurement_duration (int, optional): measurement duration in seconds.
                                                Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                                      measure_at_ocp = eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of eis measurement with \n \
                   ocp {eis_measure_at_ocp}")


        self.measurement_num += 1
        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = measurement_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)

        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_cp} parameters")

        soe = soe_eis + soe_cp
        params = {**params_eis, **params_cp}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence



    # 9. currentRange_ocp/cp-threshold-ca (cccv)
    def cp_ca_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"initiate number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        soe = soe_cp + soe_ca
        params = {**params_cp, **params_ca}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 10. currentRange_ocp/ca-threshold-cp (cvcc)
    def ca_cp_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"initiate number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")
        self.measurement_num += 1

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)

        log.info(f"measurement number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        soe = soe_ca + soe_cp
        params = {**params_ca, **params_cp}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 11. currentRange_ocp/cp-threshold-ca-ocp/eis
    def cp_ca_eis_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """

        soe_cp, params_cp, _ = self.cp_measurement( measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"initiate number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        self.measurement_num += 1

        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                                      measure_at_ocp = eis_measure_at_ocp)
        log.info(f"measurement number {self.measurement_num} of eis measurement with \n \
                    {eis_measure_at_ocp} ocp and {params_eis} parameters")

        soe = soe_cp + soe_ca + soe_eis
        params = {**params_cp, **params_ca, **params_eis}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 12. currentRange_ocp/ca-threshold-cp-ocp/eis
    def ca_cp_eis_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.
        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"initiate number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        self.measurement_num += 1

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"measurement number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                                      measure_at_ocp = eis_measure_at_ocp)
        log.info(f"measurement number {self.measurement_num} of eis measurement with \n \
                    {eis_measure_at_ocp} ocp and {params_eis} parameters")

        soe = soe_ca + soe_cp + soe_eis
        params = {**params_ca, **params_cp, **params_eis}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 13. currentRange_ocp/eis-ocp/ca-threshold-cp
    def eis_ca_cp_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                                      measure_at_ocp = eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of eis measurement with \n \
                    {eis_measure_at_ocp} ocp and {params_eis} parameters")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        self.measurement_num += 1

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"measurement number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        soe = soe_eis + soe_ca + soe_cp
        params = {**params_eis , **params_ca, **params_cp}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence



    # 14. currentRange_ocp/eis-ocp/cp-threshold-ca
    def eis_cp_ca_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5, eis_potential = 0.1, eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            eis_potential (float, optional): potential in V. Defaults to 0.1.
            eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_eis, params_eis, _ = self.eis_measurement(apply_potential = eis_potential,
                                                      measure_at_ocp = eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of eis measurement with \n \
                    {eis_measure_at_ocp} ocp and {params_eis} parameters")

        self.measurement_num += 1

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"measurement number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        soe = soe_eis + soe_cp + soe_ca
        params = {**params_eis , **params_cp, **params_ca}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 15. currentRange_ocp/eis-ocp/cp-threshold-ca-ocp/eis (cccv)
    def eis_cp_ca_eis_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5, first_eis_potential = 0.1,
                           first_eis_measure_at_ocp = True,
                           second_eis_potential = 0.1, second_eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            first_eis_potential (float, optional): potential in V. Defaults to 0.1.
            first_eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.
            second_eis_potential (float, optional): potential in V. Defaults to 0.1.
            second_eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.
        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_first_eis, params_first_eis, _ = self.eis_measurement(
                                        apply_potential = first_eis_potential,
                                        measure_at_ocp = first_eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of first eis measurement with \n \
                    {first_eis_measure_at_ocp} ocp and {params_first_eis} parameters")

        self.measurement_num += 1

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"measurement number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        self.measurement_num += 1

        soe_second_eis, params_second_eis, _ = self.eis_measurement(
                                        apply_potential = second_eis_potential,
                                        measure_at_ocp = second_eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of second eis measurement with \n \
                    {second_eis_measure_at_ocp} ocp and {params_second_eis} parameters")

        soe = soe_first_eis + soe_cp + soe_ca + soe_second_eis
        params = {**params_first_eis , **params_cp, **params_ca, **params_second_eis}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence


    # 16. currentRange_ocp/eis-ocp/ca-threshold-cp-ocp/eis (cvcc)
    def eis_ca_cp_eis_measurement(self, cp_duration = 10, cp_current = 0.00001,
                           cp_interval_time = 0.5, ca_duration = 10, ca_potential = 0.0,
                           ca_interval_time = 0.5, first_eis_potential = 0.1,
                           first_eis_measure_at_ocp = True,
                           second_eis_potential = 0.1, second_eis_measure_at_ocp = True):
        """sequence of cyclic potentiostatic and amperometric measurement from orchestrator level.
        Args:
            cp_duration (int, optional): measurement duration in seconds. Defaults to 10.
            cp_current (float, optional): current in A. Defaults to 0.00001.
            cp_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            ca_duration (int, optional): measurement duration in seconds. Defaults to 10.
            ca_potential (float, optional): potential in V. Defaults to 0.0.
            ca_interval_time (float, optional): interval time in seconds. Defaults to 0.5.
            first_eis_potential (float, optional): potential in V. Defaults to 0.1.
            first_eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.
            second_eis_potential (float, optional): potential in V. Defaults to 0.1.
            second_eis_measure_at_ocp (bool, optional): measure at ocp. Defaults to True.

        Returns:
            soe (list): list of the sequence of events.
            params (dict): dictionary of the parameters.
            sequence (dict): dict of the sequence of events with parameters.
        """
        soe_first_eis, params_first_eis, _ = self.eis_measurement(
                                        apply_potential = first_eis_potential,
                                        measure_at_ocp = first_eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of first eis measurement with \n \
                    {first_eis_measure_at_ocp} ocp and {params_first_eis} parameters")

        self.measurement_num += 1

        soe_ca, params_ca, _ = self.ca_measurement(measurement_duration= ca_duration,
                                        apply_potential = ca_potential,
                                        interval_time= ca_interval_time)
        log.info(f"measurement number {self.measurement_num} of ca measurement with \n \
                    {params_ca} parameters")

        self.measurement_num += 1

        soe_cp, params_cp, _ = self.cp_measurement(measurement_duration = cp_duration,
                                        apply_current = cp_current,
                                        interval_time = cp_interval_time)
        log.info(f"measurement number {self.measurement_num} of cp measurement with \n \
                    {params_cp} parameters")

        self.measurement_num += 1

        soe_second_eis, params_second_eis, _ = self.eis_measurement(
                                        apply_potential = second_eis_potential,
                                        measure_at_ocp = second_eis_measure_at_ocp)
        log.info(f"initiate number {self.measurement_num} of second eis measurement with \n \
                    {second_eis_measure_at_ocp} ocp and {params_second_eis} parameters")

        soe = soe_first_eis + soe_ca + soe_cp + soe_second_eis
        params = {**params_first_eis , **params_ca, **params_cp, **params_second_eis}
        sequence = dict(soe = soe, params = params, meta={})
        return soe, params, sequence

#TODO add custom sequence for a given procedure
