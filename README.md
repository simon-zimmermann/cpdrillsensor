# cpdrillsensor

data aquisition of sensors connected to the drill modules on the cp factory

## I2C Adresses

| Adress | Sensor |
| --- | --- |
| 0x6A | Accelerometer 1 |
| 0x6B | Accelerometer 2 |
| 0x40 | Power meter 1 |
| 0x41 | Power meter 2 |

## python libraries

- pi-ina219
    Power sensor library. Implments the I2C registers for the INA219 sensor.
- thermistor-utils
    Thermistor calculation helper. Implements the Steinhart-Hart equation.
- grove\.py
    Library of the Grove ecosystem. Only used to query the ADC on the Raspi shield, which connects to the NTCs.
- lsm6ds3
    Accelerometer library. Implements the I2C registers for the LSM6DS3 sensor. Originally created by William Harrington (wrh2.github.io), modified to work with grove modules. Loose file, not installed via pip.


## Software details

Aquisition frequency: 26 Hz. This matches up with the measurement frequency of the accelerometer. Any faster and the I2C bus of the RaspberryPI will be overloaded.
