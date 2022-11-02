""" Test file for the autolab driver """

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
    assert Autolab.proc.Commands["FHLevel"].CommandParameters["Duration"] == 20
