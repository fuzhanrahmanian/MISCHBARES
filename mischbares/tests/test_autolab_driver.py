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
    applied_potential = AUTOLAB.potential()
    assert round(applied_potential, 2) == 0.0


def test_current():
    """Test setting a current
    """
    applied_current = AUTOLAB.current()
    assert round(applied_current, 2) == 0.0


# def test_