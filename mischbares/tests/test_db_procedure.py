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
                           test_proc_user.user_id, datetime.now().strftime(("%H:%M:%S")),
                           number_of_electrons=1, electrode_area=1, concentration_of_active_material=1,
                           mass_of_active_material=1)

procedures = config["procedures"].keys()

proc_values = {
    "ocp": [20,100],
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


def test_add_add_cv_cycle_data():
    """test adding cv cycle data"""
    # Open the cv_cycle file and save the data as PD
    with open("mischbares/tests/test_files/cv_cycle.json") as f:
        data = json.load(f)
    temperature = data["Temperature [K]"]
    procedure.add_measurement("cv_staircase", experiment_id=procedure.experiment_id)
    assert procedure.add_procedure_information(*proc_values["cv_staircase"], procedure.measurement_id) is True
    for cycle in data["E_half_info"]:
        cycle_number = cycle.split("_")[-1]
        E_half, corrosion_points = [], []
        for _, pair_dict in data["E_half_info"][cycle].items():
            E_half.append((pair_dict["E_half"], pair_dict["I_half"]))
            corrosion_points.append((pair_dict["corrosion_point"]["voltage"], pair_dict["corrosion_point"]["current"]))

        peak_anodic, height_anodic, D_anodic = [], [], []
        for _, peak_dict in data["anodic_info"][cycle].items():
            peak_anodic.append((peak_dict["voltage"], peak_dict["current"]))
            if "D" in peak_dict.keys():
                D_anodic.append(peak_dict["D"])
            else:
                D_anodic.append(None)
            # check if height is in the dictionary
            if "height" in peak_dict.keys():
                height_anodic.append(peak_dict["height"])
            else:
                height_anodic.append(None)

        peak_cathodic, height_cathodic, D_cathodic = [], [], []
        for _, peak_dict in data["cathodic_info"][cycle].items():
            peak_cathodic.append((peak_dict["voltage"], peak_dict["current"]))
            if "D" in peak_dict.keys():
                D_cathodic.append(peak_dict["D"])
            else:
                D_cathodic.append(None)
            if "height" in peak_dict.keys():
                height_cathodic.append(peak_dict["height"])
            else:
                height_cathodic.append(None)

        assert procedure.add_cv_cycle_data(cycle_number, peak_anodic, peak_cathodic, D_anodic, D_cathodic, E_half, height_anodic,
                                    height_cathodic, corrosion_points, temperature, procedure.procedure_id)

    test_cv_cycle_data = procedure.get_cv_cycle_data(procedure_id=procedure.procedure_id)
    assert test_cv_cycle_data is not None and type(test_cv_cycle_data).__name__ == "DataFrame"
    assert temperature == test_cv_cycle_data["temperature"].iloc[0]