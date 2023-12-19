"""Test the database measurement class."""
from datetime import datetime

from mischbares.db.user import Users
from mischbares.db.experiment import Experiments
from mischbares.db.motor import Motor

# add a test_meas_user to the database to test the measurement class

test_meas_user = Users()
test_meas_user.register_user("test_motor_user", "test", "motor_user", "test_motor_user@test.de",
                            "test_psw_motor_user")

# Login as test_motor_user
test_meas_user.login_user("test_motor_user", "test_psw_motor_user")

motor_pos = [(9,8,7),(10,11,12),(2.3,2.5,2.7)]

# add a test_experiment to the database to test the measurement class
experiments = Experiments()
# get current date in format YYYY:mm:dd
experiments.add_experiment("test_experiment_motor", datetime.now().strftime(("%Y-%m-%d")),
                        test_meas_user.user_id, datetime.now().strftime(("%H:%M:%S")),
                        number_of_electrons=314, electrode_area=3.14,
                        concentration_of_active_material=3.14,
                        mass_of_active_material=3.14)

motor = Motor()

def test_add_motor_positions():
    for pos in motor_pos:
        assert motor.add_motor_positions(pos[0], pos[1], pos[2], experiments.experiment_id) is True

def test_get_motor_positions():
    motor_pos_db = motor.get_motor_positions(experiments.experiment_id)
    assert motor_pos_db is not None and type(motor_pos_db).__name__ == "DataFrame"
    for i in range(len(motor_pos)):
        assert motor_pos_db["x_coordinate"].values[i] == motor_pos[i][0]
        assert motor_pos_db["y_coordinate"].values[i] == motor_pos[i][1]
        assert motor_pos_db["z_coordinate"].values[i] == motor_pos[i][2]