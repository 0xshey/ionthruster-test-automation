> **Note**: This simulator is **not scientifically accurate**. It is a simplified and idealized model meant to act as a primitive data source and software test environment. Its purpose is to support early-stage automation, control logic development, and system integration—not to model real-world ion thruster physics.

# Virtual Ion Thruster Simulator

A modular hardware-in-the-loop (HIL) simulation of an ion propulsion system, designed for software testing, control development, and telemetry monitoring in aerospace applications.

## Overview

This simulation models key components of a basic ion thruster:
- **Ioniser Cathode** – Simulates electron generation and ionisation power draw.
- **Accelerator Grid** – Simulates beam acceleration using anode and cathode grids.
- **Propellant Injector** – Simulates xenon injection and flow control.
- **Thrust Sensor** – Simulates thrust generation based on power and flow.
- **Environmental Sensors** – Track vacuum pressure and chamber temperature.

The simulation evolves in real time and supports configuration changes mid-flight.

## Features

- Per-component power draw and thrust generation
- Realistic thermal behavior and pressure simulation
- Thread-safe simulation tick loop
- Extendable architecture for control software integration

## Usage

Run the simulation:

```bash
python main.py
