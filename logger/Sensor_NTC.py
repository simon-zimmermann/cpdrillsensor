from thermistor_utils import SH_converter
from grove.adc import ADC


class Sensor_NTC():
    def __init__(self):
        # steinhart-hart converter
        # use readings from ntc datasheet to get the coefficients
        readings = (
            (0, 32650),
            (25, 10000),
            (50, 3603),
        )
        self.converter = SH_converter.from_points(readings)

        # Grove ADC library
        self.adc = ADC()

    def get_csv_header(self):
        return "temp0, temp1,temp2,temp3"

    def get_data(self):
        # get temperature from resistance value
        # 10kOhm NTC probe; 10kOhm resistor as voltage divider
        # rntc = (10000 * uread) / (uref - uread)
        uref = self.adc.read_voltage(9)  # ADC supply voltage
        uread0 = self.adc.read_voltage(0)  # ADC reading
        uread1 = self.adc.read_voltage(1)
        uread2 = self.adc.read_voltage(2)
        uread3 = self.adc.read_voltage(3)
        rntc0 = (10000 * uread0) / (uref - uread0)
        rntc1 = (10000 * uread1) / (uref - uread1)
        rntc2 = (10000 * uread2) / (uref - uread2)
        rntc3 = (10000 * uread3) / (uref - uread3)
        temp0 = self.converter.temperature(rntc0)
        temp1 = self.converter.temperature(rntc1)
        temp2 = self.converter.temperature(rntc2)
        temp3 = self.converter.temperature(rntc3)

        tempString = "%.1f,%.1f,%.1f,%.1f" % (temp0, temp1, temp2, temp3)
        return tempString
