from unitree_sdk2py.actions import Go2Actions


def test_simulate_basic():
    a = Go2Actions(simulate=True)
    assert a.stand() == 0
    assert a.sit() == 0
    assert a.move(0.1, 0.0, 0.0, duration=0.1) == 0
    assert a.trot(duration=0.1) == 0
    assert a.turn(0.3, 0.1) == 0
    assert a.stop() == 0
