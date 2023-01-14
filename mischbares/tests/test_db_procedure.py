import json
from datetime import datetime

from mischbares.db.user import Users
from mischbares.db.experiment import Experiments
from mischbares.db.measurement import Measurements
from mischbares.db.procedure import Procedure

test_proc_user = Users()
test_proc_user.register_user("test_proc_user", "test", "proc_user", "test_proc_user@test.de",
                            "test_psw_proc_user")

# Login as test_meas_user
test_proc_user.login_user("test_proc_user", "test_psw_proc_user")

procedure = Procedure()
procedure.add_experiment("test_experiment_ocp_procedure", datetime.now().strftime(("%Y-%m-%d")),
                           test_proc_user.user_id, datetime.now().strftime(("%H:%M:%S")))
procedure.add_measurement("ocp", experiment_id=procedure.experiment_id)


def test_add_procedure_information():
    assert procedure.add_procedure_information(20, 100, 0.0, procedure.measurement_id) is True

    last_proc = test_proc_user.execute('SELECT MAX(procedure_id) FROM ocp_procedure')
    test_proc = procedure.get_procedure_information("ocp")
    assert test_proc is not None and type(test_proc).__name__ == "DataFrame" and \
         test_proc["duration"].values[0] == 20 and test_proc["interval_time"].values[0] == 100 and \
         test_proc["ocp_potential"].values[0] == 0.0

def test_add_raw_procedure_data():
    """test adding raw procedure data"""
    # Import the data from the test json file
    with open("mischbares/tests/test_files/ocp_finalized.json") as f:
        data = json.load(f)
    assert procedure.add_raw_procedure_data(data['recordsignal']) is True

    test_raw_data = procedure.get_raw_data_by_procedure("ocp")
    assert test_raw_data is not None and type(test_raw_data).__name__ == "DataFrame" and \
        len(test_raw_data) == 400 and test_raw_data["corrected_time"].values[0] == 0.0

    procedure.close()