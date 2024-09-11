
from control.contrib.netc.app import NetControllerApplication
from control.contrib.protocol.fields.field import Field
from control.contrib.protocol.fields.packet import MultiField

import json

def compute_fields (field: Field):
    pass

def create_manifest (target = "json"):
    application = NetControllerApplication()
    protocol = application.protocol.protocol

    _json = []

    for index, (name, cls, handler) in enumerate(protocol):
        _json.append({
            "index":  index,
            "target": name,
            "packet": cls().manifest()
        })
    print(json.dumps({
        "payload": _json,
        "pid_sze": application.protocol.pid_field.length
    }, indent=4))
