import time
import threading
from utils import rng

class VirtualIonThruster:
	def __init__(self, tick_rate=0.1):
		self.tick_rate = tick_rate
		self.running = False
		self.lock = threading.Lock()
		self.thread = None # TODO: Change this to be running as long as the object is alive
		self._stop_event = threading.Event()

		# Configuration set by the oeprator
		self.config = {
			"ioniser_voltage": 0.0,
			"grid_anode_voltage": 0.0,
			"grid_cathode_voltage": 0.0,
			"propellant_flow_rate": 0.0,
		}

		# Actual state of the thruster
		self.output_enabled = False

		self.ioniser_voltage = 0.0
		self.grid_anode_voltage = 0.0
		self.grid_cathode_voltage = 0.0
		self.propellant_flow_rate = 0.0

		self.ioniser_current = 0.0
		self.grid_current = 0.0

		self.power_draw = {
			"ioniser": 0.0,
			"accelerator_grid": 0.0,
			"controller": 0.0,
		}

		self.thrust = 0.0

		# Actual state of the environment
		self.chamber_temperature = 20.0
		self.environment_pressure = 101.3
		

	def update_config(self, **kwargs):
		with self.lock:
			for key, value in kwargs.items():
				if key in self.config:
					self.config[key] = value
				else:
					raise KeyError(f"Invalid configuration key: {key}")

	def start(self):
		with self.lock:
			if self.running:
				print("Simulation is already running.")
				return

			self.output_enabled = True # Enable thruster output
			self.running = True # "Ignition"

			# Start the simulation thread
			self._stop_event.clear() 
			self.thread = threading.Thread(target=self._run_loop, daemon=True)
			self.thread.start()

	def stop(self):
		with self.lock:
			if not self.running:
				print("Simulation is not running.")
				return

			self.output_enabled = False
			self.running = False
			self._stop_event.set()  # Signal thread to stop

		if self.thread:
			self.thread.join(timeout=2.0) # Avoid hanging indefinitely

	def _run_loop(self):
		while not self._stop_event.is_set():
			if self._stop_event.wait(timeout=self.tick_rate):
				break
			self._tick()

	def _tick(self):
		with self.lock:
			
			# Adjust state to current config
			self.propellant_flow_rate = self.config["propellant_flow_rate"]
			self.ioniser_voltage = self.config["ioniser_voltage"]
			self.grid_anode_voltage = self.config["grid_anode_voltage"]
			self.grid_cathode_voltage = self.config["grid_cathode_voltage"]

			# Update power-draw from the current state (W = V * I) - add noise for testing realism
			self.ioniser_current = (self.ioniser_voltage / 100.0 if self.output_enabled else 0.0) + rng.noise(0, 0.02)
			grid_voltage = self.grid_anode_voltage - self.grid_cathode_voltage
			self.grid_current = (abs(grid_voltage) / 120.0 if self.output_enabled else 0.0) + rng.noise(0, 0.01)

			self.power_draw = {
				"ioniser": self.ioniser_voltage * self.ioniser_current,
				"accelerator_grid": grid_voltage * self.grid_current,
				"controller": 2.0,  # constant draw
			}

			total_power = sum(self.power_draw.values())

			# Heat accumulation
			if self.output_enabled:
				self.chamber_temperature += total_power * 0.01 # Here 1% of the power draw is converted to heat
			else:
				self.chamber_temperature -= 1.2  # natural cooling

			self.chamber_temperature = self.chamber_temperature + rng.noise(0, 0.2)

			# Thrust generation
			if self.output_enabled and self.propellant_flow_rate > 0 and self.ioniser_voltage > 0 and (self.grid_anode_voltage - self.grid_cathode_voltage) > 0:
				self.thrust = self.propellant_flow_rate * (self.ioniser_voltage * 0.01 + (self.grid_anode_voltage - self.grid_cathode_voltage) * 0.01)
				self.thrust += rng.noise(0, 0.05)
			else:
				self.thrust = 0.0

			# TODO: Pressure sim (maybe in a different file)
			"""
				# Vacuum chamber pressure simulation
				if not hasattr(self, 'environment_pressure'):
					self.environment_pressure = 101.3  # initialize on first tick

				if self.output_enabled and flow > 0:
					self.environment_pressure -= 0.2 * (flow / 10)
				else:
					self.environment_pressure += 0.1

				self.environment_pressure = max(0.001, min(101.3, self.environment_pressure + noise(0, 0.01)))
			"""
			
			self._log()

	def output_on(self):
		with self.lock:
			self.output_enabled = True

	def output_off(self):
		with self.lock:
			self.output_enabled = False

	def _log(self):
		print(f"Ioniser Current: {self.ioniser_current:.2f}A | Grid Current: {self.grid_current:.2f}A | Thrust: {self.thrust:.2f}N | Temp: {self.chamber_temperature:.2f}°C | Pressure: {self.environment_pressure:.2f}kPa | Power Draw: {self.power_draw}")