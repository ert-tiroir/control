
from control.core import stop_control
from control.utils.singleton import Singleton

import sys
import time

def wrap_test (f):
    def reset ():
        stop_control()
        
        Singleton._instances = {}

        if "control.config.include" in sys.modules:
            del sys.modules[ "control.config.include" ]
    def wrapped ():
        try:
            f()
        except Exception as ex:
            reset()
            raise ex
        reset()
        
    wrapped.__name__ = f.__name__
    return wrapped

def should_be_fast (mdt = 1):
    def decorator(func):
        def wrapper (*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            assert end - start <= mdt, f"Took time {end - start}"
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
