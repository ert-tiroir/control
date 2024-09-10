
from control.core import start_control

import importlib

from control.utils.singleton import Singleton
from tests.decorator import wrap_test

@wrap_test
def test_include ():
    start_control ( "tests.config.sample.sample_config__test_include", True )
    
    m1 = importlib.import_module( "tests.config.sample.sample_config__test_include" )
    m2 = importlib.import_module( "control.config" ).settings
    valid = True

    for key in dir(m1):
        if getattr(m2, key) != getattr(m1, key):
            assert False