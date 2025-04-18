import time
import pytest
from virtual_ion_thruster import VirtualIonThruster

@pytest.fixture
def thruster():
    t = VirtualIonThruster(tick_rate=0.1)
    yield t
    t.stop()  # Ensure clean shutdown after test

def test_initial_config(thruster):
    assert thruster.config == {
        "ioniser_voltage": 0.0,
        "grid_anode_voltage": 0.0,
        "grid_cathode_voltage": 0.0,
        "propellant_flow_rate": 0.0,
    }
    assert thruster.running is False

def test_update_config(thruster):
    thruster.update_config(ioniser_voltage=50.0)
    assert thruster.config["ioniser_voltage"] == 50.0

    with pytest.raises(KeyError):
        thruster.update_config(invalid_key=123)

def test_start_and_stop(thruster):
    thruster.start()
    time.sleep(0.3)
    assert thruster.running is True

    thruster.stop()
    assert thruster.running is False

def test_tick_changes_state(thruster):
    thruster.update_config(
        ioniser_voltage=100.0,
        grid_anode_voltage=80.0,
        grid_cathode_voltage=20.0,
        propellant_flow_rate=5.0
    )
    thruster.start()
    time.sleep(0.3)  # Let it tick a few times

    assert thruster.ioniser_voltage > 0.0
    assert thruster.thrust >= 0.0
    assert thruster.chamber_temperature != 20.0

    thruster.stop()

def test_output_on_off(thruster):
    thruster.output_on()
    assert thruster.output_enabled is True

    thruster.output_off()
    assert thruster.output_enabled is False