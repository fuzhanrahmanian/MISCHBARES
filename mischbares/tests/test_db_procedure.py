import json
from datetime import datetime

from mischbares.config.main_config import config
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
procedure.add_experiment("test_experiment_all_procedure", datetime.now().strftime(("%Y-%m-%d")),
                           test_proc_user.user_id, datetime.now().strftime(("%H:%M:%S")))

procedures = config["procedures"].keys()

proc_values = {
    "ocp": [20,100,0.0],
    "cv_staircase": [0.4, 1.5, -1, 0.005, 2, 0.1, 0.001],
    "ca": [20, 1, 0.5, 0.0001, 0.2],
    "cp": [21, 2e-6, 0.6, 0.0002],
    "eis": [0.2, 1, 1, 10, 10000, 0.2, 2e-6, "R0_R1_C1"]
}

def test_add_procedure_information():
    """test adding procedure and raw data information"""

    for proc in procedures:
        # Add a measurement with the procedure name
        procedure.add_measurement(proc, experiment_id=procedure.experiment_id)
        assert procedure.add_procedure_information(*proc_values[proc], procedure.measurement_id) is True
        test_proc = procedure.get_procedure_information(proc)
        assert test_proc is not None and type(test_proc).__name__ == "DataFrame"

        with open(f"mischbares/tests/test_files/{proc}_finalized.json") as f:
            data = json.load(f)
            assert procedure.add_raw_procedure_data(data[config["procedures"][proc]]) is True
            test_raw_data = procedure.get_raw_data_by_procedure(proc)
            assert test_raw_data is not None and type(test_raw_data).__name__ == "DataFrame"

    procedure.close()