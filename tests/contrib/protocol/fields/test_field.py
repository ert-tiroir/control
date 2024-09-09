
from control.contrib.protocol.fields.field import Field
from tests.decorator import wrap_test


@wrap_test
def test_field_parse():
    try:
        Field().parse( None, None )
    except Exception: return
    assert False
@wrap_test
def test_field_put():
    try:
        Field().put( None, None )
    except Exception: return
    assert False