"""Class for handling motor data in the database. """

from mischbares.db.experiment import Experiments
from mischbares.logger import logger

log = logger.get_logger("db_motor")

class Motor(Experiments):
    """class for handling motor data"""
    def __init__(self):
        super().__init__()

    def add_motor_positions(self, x_coordinate, y_coordinate,
                            z_coordinate, experiment_id):
        """add a motor to the database

        Args:
            x_coordinate (float): The x coordinate of the motor
            y_coordinate (float): The y coordinate of the motor
        """
        commit_status = self.commit("INSERT INTO motor_positions \
                (x_coordinate, y_coordinate, z_coordinate, experiment_id)\
                VALUES (%s, %s, %s, %s)", \
                (x_coordinate, y_coordinate, z_coordinate, experiment_id))
        if commit_status:
            log.info(f"Motor positions ({x_coordinate}, {y_coordinate}) added.")
        return commit_status


    def get_motor_positions(self, experiment_id):
        """get the motor position from the database

        Args:
            experiment_id (int): The id of the experiment
        Returns:
            motor_positions (dict): A dict containing the motor positions
        """

        sql = "SELECT * FROM motor_positions WHERE experiment_id = %s"
        motor_positions = self.execute(sql, (experiment_id,))
        return motor_positions