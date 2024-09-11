
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
    print(json.dumps(_json, indent=4))
