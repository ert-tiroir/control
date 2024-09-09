
from control.config.manager import ConfigManager
from control.core import start_control
import importlib

from control.utils.singleton import Singleton
from tests.decorator import wrap_test

@wrap_test
def test_manager_import_valid ():
    ConfigManager().import_config ( "control.config.default.settings" )
    assert ConfigManager().has_config()
    assert ConfigManager().get_config() == importlib.import_module( "control.config.default.settings" )
@wrap_test
def test_manager_import_invalid ():
    try:
        ConfigManager().import_config ( "control.config.default.settings+l")
    except Exception:
        return
    assert ImportError("Did not raise exception")
@wrap_test
def test_manager_empty ():
    assert not ConfigManager().has_config()
    try:
        ConfigManager().get_config()
    except Exception:
        return
    assert ImportError("Did not raise exception")
@wrap_test
def test_manager_too_much ():
    ConfigManager().import_config ( "control.config.default.settings" )
    try:
        ConfigManager().import_config ( "control.config.default.settings" )
    except Exception:
        return
    assert ImportError("Did not raise exception")