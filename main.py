import time
from virtual_ion_thruster import VirtualIonThruster

def main():
    # Instantiate the virtual thruster
    thruster = VirtualIonThruster(tick_rate=0.5)

    print("=== TEST: Starting thruster ===")
    thruster.start()

    # Let it idle briefly
    time.sleep(2)

    print("=== TEST: Applying configuration ===")
    thruster.update_config(
        ioniser_voltage=120.0,
        grid_anode_voltage=100.0,
        grid_cathode_voltage=30.0,
        propellant_flow_rate=5.0
    )

    # Run for a few ticks
    time.sleep(5)

    print("=== TEST: Changing config mid-run ===")
    thruster.update_config(
        ioniser_voltage=150.0,
        grid_anode_voltage=130.0,
        grid_cathode_voltage=40.0,
        propellant_flow_rate=7.5
    )

    time.sleep(5)

    print("=== TEST: Stopping thruster ===")
    thruster.stop()

    print("=== TEST COMPLETE ===")

if __name__ == "__main__":
    main()
