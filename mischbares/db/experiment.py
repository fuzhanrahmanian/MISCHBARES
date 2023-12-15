"""Class for handling the experiment table in the database. """

from mischbares.db.database import Database
from mischbares.logger import logger

log = logger.get_logger("db_experiment")

class Experiments(Database):
    """class for handling experiment data"""
    def __init__(self):
        super().__init__()
        self.experiment_id = None

    def add_experiment(self, material, date, user_id, start_time, number_of_electrons,
                       electrode_area, concentration_of_active_material, mass_of_active_material):
        """add an experiment to the database

        Args:
            material (str): The material of the experiment
            date (date): The date of the experiment
            user_id (int): The id of the user
            start_time (time): The start time of the experiment
        Returns:
            commit_status (bool): True if the commit was successful
        """
        duration = "00:00:00"
        commit_status = self.commit("INSERT INTO experiments \
                (experiment_id, material, date, user_id, start_time, number_of_electrons, electrode_area, concentration_of_active_material, mass_of_active_material, duration)\
                VALUES (nextval('experiment_experiment_id_seq'::regclass), %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                (material, date, user_id, start_time, number_of_electrons, electrode_area, concentration_of_active_material, mass_of_active_material, duration))
        if commit_status:
            self.experiment_id = int(self.execute("SELECT currval('experiment_experiment_id_seq'::regclass)").iloc[0][0])
            log.info(f"Experiment {material} added.")
        return commit_status

    def get_experiment(self, experiment_id):
        """get an experiment from the database

        Args:
            experiment_id (int): The id of the experiment
        Returns:
            experiment (dict): A dictionary containing the experiment's data
        """
        sql = "SELECT * FROM experiments WHERE experiment_id = %s"
        experiment = self.execute(sql, (experiment_id,))
        return experiment


    def get_all_experiments_by_user(self, user_id):
        """get all experiments from the database

        Args:
            user_id (int): The id of the user
        Returns:
            experiments (list): A list containing all experiments
        """
        sql = "SELECT * FROM experiments WHERE user_id = %s"
        experiments = self.execute(sql, (user_id,))
        return experiments
