from virtual_ion_thruster import VirtualIonThruster
import time

def main():
	thruster = VirtualIonThruster()
	thruster.update_config(
		ioniser_voltage=120.0,
		grid_anode_voltage=200.0,
		grid_cathode_voltage=50.0,
		propellant_flow_rate=3.0
	)

	thruster.start()

	# Let it run a bit...
	time.sleep(2)

	thruster.update_config(grid_anode_voltage=400.0)  # Live update

	# More runtime
	time.sleep(3)

	thruster.stop()


if __name__ == "__main__":
	main()