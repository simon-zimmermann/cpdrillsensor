import time
import sys
import traceback
import argparse
from oclock import Timer
from grove.adc import ADC
from ina219 import INA219
from thermistor_utils import SH_converter

from lsm6ds3 import LSM6DS3

# setup for LSM (accelerometer)
ACC_rate = LSM6DS3.ACC_ODR_26_HZ

lsm1 = LSM6DS3(ACC_ODR=ACC_rate,
               GYRO_ODR=LSM6DS3.GYRO_ODR_POWER_DOWN,
               enable_acc=LSM6DS3.ENABLE_ACC_ALL_AXIS,
               enable_gyro=LSM6DS3.ENABLE_GYRO_NONE_AXIS,
               acc_interrupt=False,
               acc_scale=LSM6DS3.ACC_SCALE_16G,
               pin_SAD_level=0)

lsm2 = LSM6DS3(ACC_ODR=ACC_rate,
               GYRO_ODR=LSM6DS3.GYRO_ODR_POWER_DOWN,
               enable_acc=LSM6DS3.ENABLE_ACC_ALL_AXIS,
               enable_gyro=LSM6DS3.ENABLE_GYRO_NONE_AXIS,
               acc_interrupt=False,
               acc_scale=LSM6DS3.ACC_SCALE_16G,
               pin_SAD_level=1)


def main():
    global lsm1, lsm2, f

    # parse command line arguments
    parser = argparse.ArgumentParser(prog='datalogger',
                                     description='Reads data of attached sensors, and writes them to a .csv file. \
                                     Can only run on a Raspi')
    parser.add_argument('-d', '--duration', type=int, help='Logging duration in seconds', default=2)
    parser.add_argument('-f', '--frequency', type=int,
                        help='How many data points should be logged per second', default=26)
    args = parser.parse_args()
    print("Logging for a total of %d seconds, with a frequency of %d per second" % (args.duration, args.frequency))
    logFrequency = args.frequency  # Hz
    logDuration = args.duration

    # ADC setup (for NTC probes)
    adc = ADC()

    # amp meter (see https://pypi.org/project/pi-ina219/)
    SHUNT_OHMS = 0.1
    ampMeter1 = INA219(SHUNT_OHMS, address=0x40)
    ampMeter1.configure(voltage_range=INA219.RANGE_32V)
    ampMeter2 = INA219(SHUNT_OHMS, address=0x41)
    ampMeter2.configure(voltage_range=INA219.RANGE_32V)

    # file stup
    datetime = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "sensorlog_" + datetime + ".csv"
    f = open("output/" + filename, "x")
    print("logging to file:\n" + filename)
    # header
    f.write("time, aquisitionDuration, remainingTime, \
            imu1_accX, imu1_accY, imu1_accZ, \
            imu2_accX, imu2_accY, imu2_accZ, \
            temp0, temp1,temp2,temp3, \
            power1Volt, power1MilliAmp, power1MilliWatt, power1ShuntMilliVolt,\
            power2Volt, power2MilliAmp, power2MilliWatt, power2ShuntMilliVolt\n")

    # the second the file was created
    file_startsecond = time.time()
    loopsecond = 0
    logCount = 0

    # steinhart-hart converter (see ntc datasheet)
    readings = (
        (0, 32650),
        (25, 10000),
        (50, 3603),
    )
    conv = SH_converter.from_points(readings)

    # loop timer
    timer = Timer(interval=1 / logFrequency)
    while (loopsecond < logDuration):
        # timer to measure the duration of the data aquisition
        startTime = time.perf_counter()

        # how many seconds have passed since the file was created
        loopsecond = time.time() - file_startsecond
        try:
            # get acc sensor data
            accData1 = lsm1.getAccData()
            accString1 = "%.6f,%.6f,%.6f" % (accData1[0], accData1[1], accData1[2])
            accData2 = lsm2.getAccData()
            accString2 = "%.6f,%.6f,%.6f" % (accData2[0], accData2[1], accData2[2])

            # get temperature  resistance value
            # 10kOhm NTC probe; 10kOhm resistor as voltage divider
            # rntc = (10000 * uread) / (uref - uread)
            uref = adc.read_voltage(9)  # ADC supply voltage
            uread0 = adc.read_voltage(0)  # ADC reading
            uread1 = adc.read_voltage(1)
            uread2 = adc.read_voltage(2)
            uread3 = adc.read_voltage(3)
            rntc0 = (10000 * uread0) / (uref - uread0)
            rntc1 = (10000 * uread1) / (uref - uread1)
            rntc2 = (10000 * uread2) / (uref - uread2)
            rntc3 = (10000 * uread3) / (uref - uread3)
            temp0 = conv.temperature(rntc0)
            temp1 = conv.temperature(rntc1)
            temp2 = conv.temperature(rntc2)
            temp3 = conv.temperature(rntc3)

            tempString = "%.1f,%.1f,%.1f,%.1f" % (temp0, temp1, temp2, temp3)

            # get power meter
            powerString1 = "%.3f,%.3f,%.3f,%.3f" % (
                ampMeter1.voltage(), ampMeter1.current(), ampMeter1.power(), ampMeter1.shunt_voltage())
            powerString2 = "%.3f,%.3f,%.3f,%.3f" % (
                ampMeter2.voltage(), ampMeter2.current(), ampMeter2.power(), ampMeter2.shunt_voltage())

            # Duration the data aquisition took
            aqTime = time.perf_counter() - startTime
            # Time remaining before next loop
            remainingTime = (1 / logFrequency) - aqTime

            # Write data to file
            f.write("%.3f,%.6f,%.6f,%s,%s,%s,%s,%s\n" %
                    (loopsecond, aqTime, remainingTime,
                     accString1,
                     accString2,
                     tempString,
                     powerString1, powerString2))

            # display once every 2 seconds how much data has been logged
            logCount = logCount + 1
            if (logCount % (logFrequency * 2) == 0):
                print("logging: %d at t=%fs" % (logCount, loopsecond))

            timer.checkpt()

        except KeyboardInterrupt:
            cleanup_close()
        except Exception as e:
            print('Caught exception %s' % e)
            traceback.print_exc()
            cleanup_close()

    print("Logging finished")
    cleanup_close()


def cleanup_close():
    global lsm1, lsm2, f
    del (lsm1)
    del (lsm2)
    f.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
