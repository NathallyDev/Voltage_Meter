# Voltimeter Sensor - Data Acquisition and Plotting System

This project consists of a system to measure and record DC voltage data from 0-28V using an ARDUINO MEGA 2560 microcontroller. The Python script receives the data, plots graphs and generates a PDF with the relevant information.

## Progress

- Start: 03/07/2024
- Update: 09/28/2024
- Status: Complete

## Requirements

- Arduino 1.8.19
- Python 3.x
- Python libraries: pyserial, matplotlib, reportlab, time, io, tempfile, os, pdfkit

## Configuration and Usage

1. **Installing Dependencies:**
Make sure you have the necessary libraries installed. Run the following command to install them:

```bash
pip install pyserial matplotlib reportlab winshell

2. **Circuit**
Make sure you have the following components:

- Arduino MEGA 2560
- DC voltage sensor (Model0: 0V ~ 25V)
- Series resistors (1x 10K ohm)
