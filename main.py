from virtual_ion_thruster import VirtualIonThruster
import time

def main():
	thruster = VirtualIonThruster(tick_rate=0.1)

	# Configure the thruster
	thruster.update_config(
		ioniser_voltage=200.0,
		grid_anode_voltage=1200.0,
		grid_cathode_voltage=0.0,
		propellant_flow_rate=2.5,
	)

	# Enable output and start the simulation loop
	thruster.output_on()
	thruster.start()

	# Let the simulation run for a few seconds
	time.sleep(5)

	# Read and print telemetry
	telemetry = thruster.read_telemetry()
	print("Telemetry after 5s:")
	for key, value in telemetry.items():
		print(f"{key}: {value}")

	thruster.stop()

if __name__ == "__main__":
	main()
