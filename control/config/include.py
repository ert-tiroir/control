
from control.config.manager import ConfigManager

def replace_globals ():
    dict = ConfigManager().get_config()
    glbl = globals()
    for key in list(glbl.keys()):
        del glbl[key]

    for key in dir(dict).copy():
        glbl[key] = getattr(dict, key)
    
replace_globals()
