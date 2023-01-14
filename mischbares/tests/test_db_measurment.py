"""Test the database measurement class."""
from datetime import datetime

from mischbares.db.user import Users
from mischbares.db.experiment import Experiments
from mischbares.db.measurement import Measurements

# add a test_meas_user to the database to test the measurement class

test_meas_user = Users()
test_meas_user.register_user("test_meas_user", "test", "meas_user", "test_meas_user@test.de",
                            "test_psw_meas_user")

# Login as test_meas_user
test_meas_user.login_user("test_meas_user", "test_psw_meas_user")

# add a test_experiment to the database to test the measurement class
experiments = Experiments()
experiments.add_experiment("test_experiment", "2024-02-02",
                           test_meas_user.user_id, datetime.now().strftime(("%H:%M:%S")))
#datetime.now().strftime(("%Y-%m-%d")
# test_procedure
procedure_name = "ocp"
wrong_procedure_name = "wrong_procedure"


def test_add_measurement():
    """Test the add_measurement method by adding a measurment for the newly created experiment."""

    measurment = Measurements()
    assert measurment.add_measurement(wrong_procedure_name, experiment_id=experiments.experiment_id) is False
    assert measurment.add_measurement(procedure_name, experiment_id=experiments.experiment_id) is True

    # Check that the measurement is not None and of type tuple and has procedure "ocp"
    last_meas = test_meas_user.execute('SELECT MAX(measurement_id) FROM measurements')
    test_meas = measurment.get_measurement(int(last_meas['max'].values[0]))
    assert test_meas is not None and type(test_meas).__name__ == "DataFrame" and \
        test_meas["procedure_name"].values[0] == procedure_name

    measurment.close()


def test_get_all_measurements_by_experiment_id():
    """Test the get_all_measurements_by_experiment method."""

    measurment = Measurements()
    # Add another measurement to the database with the same experiment id
    measurment.add_measurement(procedure_name, experiment_id=experiments.experiment_id)
    test_meas_by_exp = measurment.get_measurements_by_experiment_id(experiments.experiment_id)
    assert test_meas_by_exp is not None and type(test_meas_by_exp).__name__ == "DataFrame"
    # Assert that all experiment ids is the same
    assert test_meas_by_exp["experiment_id"].unique()[0] == experiments.experiment_id
    assert test_meas_by_exp["procedure_name"].unique()[0] == procedure_name
    assert len(test_meas_by_exp["experiment_id"].unique()) == 1
    measurment.close()

def test_get_measurements_by_procedure_name():
    """Test the get_measurement_by_procedure_name method."""

    measurment = Measurements()
    test_meas_by_procedure = measurment.get_measurements_by_procedure_name(procedure_name)
    assert test_meas_by_procedure is not None and type(test_meas_by_procedure).__name__ == "DataFrame"
    # Assert that all experiment ids is the same
    assert test_meas_by_procedure["procedure_name"].unique()[0] == procedure_name
    measurment.close()

def test_get_measurement_by_user_id():
    """Test the get_measurement_by_user_id method."""

    measurment = Measurements()
    test_meas_by_user = measurment.get_measurements_by_user_id(test_meas_user.user_id)
    assert test_meas_by_user is not None and type(test_meas_by_user).__name__ == "DataFrame"
    # Assert that all experiment ids is the same
    assert test_meas_by_user["user_id"].unique()[0] == test_meas_user.user_id
    measurment.close()