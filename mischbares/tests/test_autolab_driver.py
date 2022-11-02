""" Test file for the autolab driver """
import os
import pytest

from mischbares.config.main_config_2 import config
from mischbares.driver.autolab_driver import Autolab

AUTOLAB = Autolab(config["autolabDriver"])

def test_load_procedure():
    AUTOLAB.load_procedure("ocp")
    assert AUTOLAB.proc.FileName[-21:-4] == "OCP_record_signal"
