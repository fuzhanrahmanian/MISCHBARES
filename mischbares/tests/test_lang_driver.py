import pytest
from mischbares.driver.lang_driver import langNet
from mischbares.config.main_config import config

lang_net = langNet()

def test_connect():
    lang_net.connect()
    assert lang_net.connected == True


def test_getPos():
    pos = lang_net.getPos()
    assert isinstance(pos, tuple)
    assert len(pos) == 3
    assert all(isinstance(p, float) for p in pos)

def test_moveRelFar():
    lang_net.moveRelFar(1.0, 2.0, 0)
    get_pos = lang_net.getPos()
    assert round(get_pos[0],1) == 1.0
    assert round(get_pos[1],1) == 2.0
    lang_net.goHome()

def test_moveRelZ():
    lang_net.moveRelZ(0.1)
    get_pos = lang_net.getPos()
    assert round(get_pos[2],1) == 0.1
    lang_net.goHome()

def test_moveRelXY():
    lang_net.moveRelXY(1.0, 2.0)
    get_pos = lang_net.getPos()
    assert round(get_pos[0],1) == 1.0
    assert round(get_pos[1],1) == 2.0
    lang_net.goHome()

def test_moveAbsXY():
    lang_net.moveAbsXY(1.0, 2.0)
    get_pos = lang_net.getPos()
    assert round(get_pos[0],1) == 1.0
    assert round(get_pos[1],1) == 2.0
    lang_net.goHome()

def test_moveAbsZ():
    lang_net.moveAbsZ(0.25)
    get_pos = lang_net.getPos()
    assert round(get_pos[2],2) == 0.25
    lang_net.goHome()


def test_moveAbsFar():
    lang_net.moveAbsFar(1.0, 2.0, 0.25)
    get_pos = lang_net.getPos()
    assert round(get_pos[0],1) == 1.0
    assert round(get_pos[1],1) == 2.0
    assert round(get_pos[2],2) == 0.25
    lang_net.goHome()

def test_disconnect():
    lang_net.disconnect()
    assert lang_net.connected == False

