import time
import threading
from utils import rng

class VirtualIonThruster:
	def __init__(self, tick_rate=0.1):
		self.lock = threading.Lock()
		self.tick_rate = tick_rate  # seconds between simulation steps

		# Component configuration
		self.config = {
			"ioniser_voltage": 0.0,
			"grid_anode_voltage": 0.0,
			"grid_cathode_voltage": 0.0,
			"propellant_flow_rate": 0.0,
		}

		# Simulation state
		self.power_draw = {
			"ioniser": 0.0,
			"accelerator_grid": 0.0,
			"controller": 0.0,
		}
		self.chamber_temperature = 20.0
		self.environment_pressure = 101.3
		self.output_enabled = False
		

	def update_config(self, **kwargs):
		"""Update one or more configuration parameters."""
		with self.lock:
			for key, value in kwargs.items():
				if key in self.config:
					self.config[key] = value
				else:
					raise KeyError(f"Invalid configuration key: {key}")

	def start(self):
		self.running = True
		threading.Thread(target=self._run_loop, daemon=True).start()

	def stop(self):
		self.running = False

	def _run_loop(self):
		while self.running:
			time.sleep(self.tick_rate)
			self._tick()

	def _tick(self):
		with self.lock:
			
			# Apply configurations
			flow = self.config["propellant_flow_rate"]
			ioniser_v = self.config["ioniser_voltage"]
			grid_anode_v = self.config["grid_anode_voltage"]
			grid_cathode_v = self.config["grid_cathode_voltage"]
			grid_v = grid_anode_v - grid_cathode_v

			# Simulate per-component power draw (W = V * I)
			self.ioniser_current = ioniser_v / 100.0 if self.output_enabled else 0.0
			self.grid_current = abs(grid_v) / 120.0 if self.output_enabled else 0.0

			self.ioniser_current += rng.noise(0, 0.02)
			self.grid_current += rng.noise(0, 0.01)

			self.power_draw = {
				"ioniser": ioniser_v * self.ioniser_current,
				"accelerator_grid": grid_v * self.grid_current,
				"controller": 2.0,  # constant draw
			}

			total_power = sum(self.power_draw.values())

			# Heat accumulation
			if self.output_enabled:
				self.chamber_temperature += total_power * 0.01
			else:
				self.chamber_temperature -= 0.3  # natural cooling

			self.chamber_temperature = self.chamber_temperature + rng.noise(0, 0.2)

			# Thrust generation
			if self.output_enabled and flow > 0 and ioniser_v > 0 and grid_v > 0:
				self.thrust = flow * (ioniser_v * 0.01 + grid_v * 0.01)
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
			
			self.log()

	def output_on(self):
		with self.lock:
			self.output_enabled = True

	def output_off(self):
		with self.lock:
			self.output_enabled = False

	def log(self):
		print(f"Ioniser Current: {self.ioniser_current:.2f}A | Grid Current: {self.grid_current:.2f}A | Thrust: {self.thrust:.2f}N | Temp: {self.chamber_temperature:.2f}°C | Pressure: {self.environment_pressure:.2f}kPa | Power Draw: {self.power_draw}")

	def read_telemetry(self):
		with self.lock:
			return {
				"config": self.config.copy(),
				"thrust": self.thrust,
				"chamber_temperature": self.chamber_temperature,
				"environment_pressure": self.environment_pressure,
				"power_draw": self.power_draw.copy(),
			}
