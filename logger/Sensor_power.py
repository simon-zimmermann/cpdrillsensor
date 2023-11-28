from ina219 import INA219


class Sensor_power:
    def __init__(self):
        # amp meter (see https://pypi.org/project/pi-ina219/)
        SHUNT_OHMS = 0.1
        self.sensor1 = INA219(SHUNT_OHMS, address=0x40)
        self.sensor1.configure(voltage_range=INA219.RANGE_32V)
        self.sensor2 = INA219(SHUNT_OHMS, address=0x41)
        self.sensor2.configure(voltage_range=INA219.RANGE_32V)

    def get_csv_header(self):
        return "power1MilliWatt,power2MilliWatt"

    def get_data(self):
        voltage = 24  # always 24V
        power1 = self.sensor1.current() * voltage
        power2 = self.sensor2.current() * voltage
        # powerString1 = "%.3f,%.3f,%.3f,%.3f" % (
        #    self.sensor1.voltage(), self.sensor1.current(), self.sensor1.power(), self.sensor1.shunt_voltage())
        # powerString2 = "%.3f,%.3f,%.3f,%.3f" % (
        #    self.sensor2.voltage(), self.sensor2.current(), self.sensor2.power(), self.sensor2.shunt_voltage())
        return "%d,%d" % (power1, power2)

    def is_triggered(self):
        sensor1_triggered = self.sensor1.current() > 10
        sensor2_triggered = self.sensor2.current() > 10
        if (sensor1_triggered):
            print("Power Sensor 1 triggered")
        if (sensor2_triggered):
            print("Power Sensor 2 triggered")
        return sensor1_triggered or sensor2_triggered
