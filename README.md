> **Note**: This simulator is **not scientifically accurate**. It is a simplified and idealized model meant to act as a primitive data source and software test environment. Its purpose is to support early-stage automation, control logic development, and system integration—not to model real-world ion thruster physics.

# Demonstration of Ion Thruster Testing

This project is designed to demonstrate the testing of a modular hardware-in-the-loop (HIL) simulation of an ion propulsion system.

## Overview

Components of the ion propulsion system are simulated (not accurately) to provide a context for testing control software. The simulation includes:
- **Ioniser** – Simulates electron generation and ionisation power draw.
- **Accelerator Grid** – Simulates beam acceleration using anode and cathode grids.
- **Propellant Injector** – Simulates xenon injection and flow control.
- **Thrust Sensor** – Simulates thrust generation based on power and flow.
- **Environmental Sensors** – Track vacuum pressure and chamber temperature.


## Features

- Per-component power draw and thrust generation
- Realistic thermal behavior and pressure simulation
- Thread-safe simulation tick loop
- Extendable architecture for control software integration
- Ability to update thruster configuration and parameters during operation

## Usage

Create and install a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the simulation:
```bash
python main.py
```
