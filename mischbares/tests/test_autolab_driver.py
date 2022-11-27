""" Test file for the autolab driver """
import os
import numpy as np
import asyncio
from mischbares.config.main_config import config
from mischbares.driver.autolab_driver import Autolab

AUTOLAB = Autolab(config["autolabDriver"])

def test_load_procedure():
    """Test loading a procedure
    """
    AUTOLAB.load_procedure("ocp")
    assert AUTOLAB.proc.FileName[-18:-4] == "OCP_MISCHBARES"


def test_potential():
    """Test setting a potential
    """
    current_potential = AUTOLAB.potential()
    assert round(current_potential, 2) == 0.0


def test_current():
    """Test setting a current
    """
    current = AUTOLAB.current()
    assert round(current, 2) == 0.0


def test_applied_potential():
    """Test setting a potential
    """
    applied_potential = AUTOLAB.applied_potential()
    assert round(applied_potential, 2) == 0.0


def test_measure_status():
    """Test measuring the status
    """
    status = AUTOLAB.measure_status()
    assert status is False


def test_set_setpoints():
    """Test setting the setpoints
    """
    AUTOLAB.load_procedure("ocp")
    AUTOLAB.set_setpoints(procedure = "ocp", setpoints = {'recordsignal': {'Duration (s)': 20}},\
                            current_range = "1uA")
    assert AUTOLAB.proc.Commands["FHLevel"].CommandParameters["Duration"].Value == 20


def test_parse_nox():
    """Test parsing a nox file
    """
    data = AUTOLAB.parse_nox(parse_instruction = ['recordsignal'],
                      save_dir = os.path.join(os.getcwd(), "results"),
                      optional_name = "OCP_example")
    assert round(np.mean(data['recordsignal']['WE(1).Potential']), 3) == 0.0


def test_measure():
    """Test measuring
    """
    AUTOLAB.load_procedure("ocp")
    AUTOLAB.set_setpoints(procedure = "ocp", setpoints = {'recordsignal': {'Duration (s)': 10}},\
                            current_range = "1uA")
    AUTOLAB.proc.Measure()
    AUTOLAB.proc.SaveAs(os.path.join(os.getcwd(), "results", "test.nox"))
    assert len([str(n) for n in AUTOLAB.proc.Commands['recordsignal'].Signals.Names]) == 10


def test_ocp_on_the_fly():
    """Test measuring open circuit potential on the fly
    """
    _, ocp_potential = AUTOLAB.get_ocp_on_the_fly()
    assert round(ocp_potential, 2) == 0.0

# from here can be just run by debugging

def test_ca_at_ocp():
    """ Test performing ca measurement at ocp potential
    """
    data = AUTOLAB.perform_measurement(procedure = "ca",\
            setpoints = {'applypotential': {'Setpoint value': 0.7},\
                'recordsignal': {'Duration (s)': 5, 'Interval time (s)': 0.5}},\
            save_dir= "mischbares/tests",
            plot_type ='tCV', parse_instruction = ['recordsignal'], \
            current_range= "100uA", measure_at_ocp = True)
    assert len(data['recordsignal'].keys()) == 11
    assert round(data['recordsignal']['WE(1).Potential'][-1], 1) == 0.7


def test_cp_at_ocp():
    """ Test performing cp measurement at ocp potential
    """
    data = AUTOLAB.perform_measurement(procedure = "cp",\
            setpoints = {'applycurrent': {'Setpoint value': 0.00001},\
                'recordsignal': {'Duration (s)': 10, 'Interval time (s)': 0.5}},\
            save_dir= "mischbares/tests",\
            plot_type ='tCV', parse_instruction = ['recordsignal'], \
            current_range = "100uA", measure_at_ocp = True)
    assert len(data['recordsignal'].keys()) == 11
    assert round(data["recordsignal"]['WE(1).Current'][-1], 1) == 0.0


def test_eis_at_ocp():
    """ Test performing eis measurement at ocp potential
    """
    data = asyncio.run(AUTOLAB.perform_measurement(procedure = "eis", setpoints = None,
            save_dir= "mischbares/tests", plot_type ='impedance',
            parse_instruction = ["FIAMeasPotentiostatic", "FIAMeasurement"],
            current_range= "1mA", measure_at_ocp = True))
    assert len(data.keys()) ==2
    assert round(data["FIAMeasurement"]['Potential (DC)'][0], 1) == 0.0


def test_disconnect():
    """Test disconnecting
    """
    AUTOLAB.disconnect()
