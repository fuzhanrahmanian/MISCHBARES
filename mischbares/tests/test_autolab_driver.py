""" Test file for the autolab driver """
import os
import numpy as np
from mischbares.config.main_config_2 import config
from mischbares.driver.autolab_driver import Autolab

AUTOLAB = Autolab(config["autolabDriver"])

def test_load_procedure():
    """Test loading a procedure
    """
    AUTOLAB.load_procedure("ocp")
    assert AUTOLAB.proc.FileName[-21:-4] == "OCP_record_signal"


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
    AUTOLAB.set_setpoints({'FHLevel': {'Duration': 20}})
    assert AUTOLAB.proc.Commands["FHLevel"].CommandParameters["Duration"].Value == 20


def test_parse_nox():
    """Test parsing a nox file
    """
    data = AUTOLAB.parse_nox(parse_instruction = ['recordsignal'],
                      save_dir = os.path.join(os.getcwd(), "results"),
                      optional_name = "OCP_example.nox")
    assert round(np.mean(data['recordsignal']['WE(1).Potential']), 3) == 0.0


def test_measure():
    """Test measuring
    """
    AUTOLAB.load_procedure("ocp")
    AUTOLAB.set_setpoints({'FHLevel': {'Duration': 10}})
    AUTOLAB.proc.Measure()
    AUTOLAB.proc.SaveAs(os.path.join(os.getcwd(), "results", "test.nox"))
    assert len([str(n) for n in AUTOLAB.proc.Commands['FHLevel'].Signals.Names]) == 6


def test_disconnect():
    """Test disconnecting
    """
    AUTOLAB.disconnect()
