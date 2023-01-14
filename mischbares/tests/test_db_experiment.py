"""Test the database experiment class."""
from datetime import datetime

from mischbares.db.user import Users
from mischbares.db.experiment import Experiments
from mischbares.db.motor import Motor

# add a test_exp_user to the database to test the experiment class

test_exp_user = Users()
test_exp_user.register_user("test_exp_user", "test", "exp_user", "test_exp_user@test.de",
                            "test_psw_exp_user")

# Login as test_exp_user
test_exp_user.login_user("test_exp_user", "test_psw_exp_user")

def test_add_experiment():
    """Test the add_experiment method."""

    experiments = Experiments()
    assert experiments.add_experiment("test_material", datetime.now().strftime(("%Y-%m-%d")), \
        test_exp_user.user_id, "12:00:00") is True

    # Check that the experiment is not None and of type tuple and has material "test_material"
    last_exp = test_exp_user.execute('SELECT MAX(experiment_id) FROM experiments')
    test_experiment = experiments.get_experiment(int(last_exp['max'].values[0]))
    assert test_experiment is not None and type(test_experiment).__name__ == "DataFrame" and \
        test_experiment["material"].values[0] == "test_material"

    experiments.close()


def test_get_all_experiments_by_user():
    """Test the get_all_experiments_by_user method."""

    experiments = Experiments()
    test_exp_by_user = experiments.get_all_experiments_by_user(test_exp_user.user_id)
    assert test_exp_by_user is not None and type(test_exp_by_user).__name__ == "DataFrame"
    # Assert that all user ids is the same as the test_exp_user's user id
    assert test_exp_by_user["user_id"].unique()[0] == test_exp_user.user_id
    assert test_exp_by_user["material"].unique()[0] == "test_material"
    assert len(test_exp_by_user["user_id"].unique()) == 1
    experiments.close()


def test_add_experiment_with_motor():
    """Test the add_experiment method."""
    experiment_motor = Motor()
    # add the experiment

    experiment_motor.add_experiment("test_material_for_motor", "2021-01-01", \
        test_exp_user.user_id, "2:00:00")

    assert experiment_motor.add_motor_positions(2.5, 2) is True
    pos = experiment_motor.get_motor_positions(experiment_motor.experiment_id)
    assert pos is not None and type(pos).__name__ == "DataFrame" and pos["x_coordinate"].values[0] == 2.5 and \
        pos["y_coordinate"].values[0] == 2 and pos["experiment_id"].values[0] == experiment_motor.experiment_id


