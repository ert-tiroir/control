
from control.core.app import Application, ApplicationManager
from control.utils.singleton import Singleton

from tests.decorator import wrap_test

@wrap_test
def test_empty_manager ():
    assert ApplicationManager().applications == []
@wrap_test
def test_one_app_manager ():
    ApplicationManager().bind( "testing.A" )
    class A(Application): pass
    ApplicationManager().unbind()
    
    assert ApplicationManager().applications == [ A("Hi !") ]
@wrap_test
def test_app_singleton ():
    ApplicationManager().bind( "testing.A" )
    class A(Application): pass
    ApplicationManager().unbind()
    ApplicationManager().bind( "testing.B" )
    class B(Application): pass
    ApplicationManager().unbind()

    a1 = A( "a1" )
    a2 = A( "a2" )
    b1 = B( "b1" )
    b2 = B( "b2" )

    assert id(a1) == id(a2)
    assert id(b1) != id(a2)
    assert id(a1) != id(b2)
    assert id(b1) == id(b2)

    assert ApplicationManager().applications == [ a1, b1 ] == [ a2, b2 ]
