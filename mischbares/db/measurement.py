""" Class for handling the measurment database table."""

from mischbares.db.experiment import Experiments
from mischbares.config.main_config import config
from mischbares.logger import logger

log = logger.get_logger("db_measurments")

class Measurements(Experiments):
    """class for handling measurement data"""
    def __init__(self):
        super().__init__()
        self.measurement_id = None
        self.procedure_name = None
        self.parser = None


    def add_measurement(self, procedure_name, experiment_id):
        """add a measurement to the database

        Args:
            procedure_name (str): The name of the procedure
            experiment_id (int): The id of the experiment the measurement belongs to
        Returns:
            commit_status (bool): True if the commit was successful
        """
        if not procedure_name in config["procedures"].keys():
            log.error(f"Procedure {procedure_name} not found in config.")
            return False
        self.parser = config["procedures"][procedure_name]
        commit_status = self.commit("INSERT INTO measurements \
            (measurement_id, procedure_name, experiment_id)\
            VALUES (nextval('measurment_measurment_id_seq'::regclass), %s, %s)", \
            (procedure_name, experiment_id)) # This typo in measurment_measurment_id_seq is a typo in the database
        if commit_status:
            self.measurement_id = int(self.execute("SELECT currval('measurment_measurment_id_seq'::regclass)").iloc[0][0])
            self.procedure_name = procedure_name
            log.info(f"Measurement {procedure_name} added.")
        return commit_status


    def get_measurement(self, measurement_id):
        """get a measurement from the database

        Args:
            measurement_id (int): The id of the measurement
        Returns:
        """
        sql = "SELECT * FROM measurements WHERE measurement_id = %s"
        measurement = self.execute(sql, (measurement_id,))
        return measurement

    def get_experiment_id_by_measurement_id(self, measurement_id):
        """get a measurement from the database given a measurement id

        Args:
            measurement_id (int): The id of the measurement
        Returns:
            experiment_id (int): The id of the experiment
        """
        sql = "SELECT experiment_id FROM measurements WHERE measurement_id = %s"
        experiment_id = self.execute(sql, (measurement_id,))
        return experiment_id

    def get_measurements_by_experiment_id(self, experiment_id):
        """get a measurement from the database given an experiment id

        Args:
            experiment_id (int): The id of the experiment
        Returns:
            measurements (list): A list containing all measurements
        """
        sql = "SELECT * FROM measurements WHERE experiment_id = %s"
        measurements = self.execute(sql, (experiment_id,))
        return measurements

    def get_measurements_by_procedure_name(self, procedure_name):
        """get a measurement from the database

        Args:
            procedure_name (str): The name of the procedure
        Returns:
            measurements (list): A list containing all measurements
        """
        sql = "SELECT * FROM measurements WHERE procedure_name = %s"
        measurments = self.execute(sql, (procedure_name,))
        return measurments


    def get_measurements_by_user_id(self, user_id):
        """get a measurement from the database

        Args:
            user_id (int): The id of the user
        Returns:
            measurements (list): A list containing all measurements and the user_id
        """
        sql = "SELECT measurements.*, users.user_id \
               FROM measurements \
               JOIN experiments ON measurements.experiment_id = experiments.experiment_id \
               JOIN users on experiments.user_id = users.user_id \
               WHERE users.user_id = %s"
        measurements = self.execute(sql, (user_id,))
        return measurements