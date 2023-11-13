import time
import sys
import traceback
from datetime import date
from oclock import Timer

from lsm6ds3 import LSM6DS3

# setup for IMU
imu = LSM6DS3(ACC_ODR=LSM6DS3.ACC_ODR_6_66_KHZ,
              GYRO_ODR=LSM6DS3.GYRO_ODR_1_66_KHZ,
              enable_acc=LSM6DS3.ENABLE_ACC_ALL_AXIS,
              # enable_acc=ENABLE_ACC_X_AXIS,
              # enable_gyro=LSM6DS3.ENABLE_GYRO_NONE_AXIS,
              enable_gyro=LSM6DS3.ENABLE_GYRO_ALL_AXIS,
              acc_interrupt=False,
              gyro_interrupt=False,
              acc_scale=LSM6DS3.ACC_SCALE_16G,
              gyro_scale=LSM6DS3.GYRO_SCALE_2000DPS)

logFrequency = 500  # Hz
logCount = 2000


def main():
    global imu
    global f

    # file stup
    datetime = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "sensorlog_" + datetime + ".csv"
    f = open("output/" + filename, "x")
    print("logging to file:\n" + filename)
    # header
    f.write("time, aquisitionDuration, accX, accY, accZ, gyroX, gyroY, gyroZ\n")
    # the second the file was created
    file_startsecond = time.time()

    # loop timer
    timer = Timer(interval=1 / logFrequency)
    for i in range(logCount):
        # timer to measure the duration of the data aquisition
        startTime = time.perf_counter()

        # how many seconds have passed since the file was created
        loopsecond = time.time() - file_startsecond
        try:
            # get sensor data
            accData = imu.getAccData()
            accString = "%.6f,%.6f,%.6f" % (accData[0], accData[1], accData[2])
            gyroData = imu.getGyroData()
            gyroString = "%.6f,%.6f,%.6f" % (gyroData[0], gyroData[1], gyroData[2])

            # Duration the data aquisition took
            aqTime = time.perf_counter() - startTime

            # Write data to file
            f.write("%.3f,%.6f,%s,%s\n" %
                    (loopsecond, aqTime, accString, gyroString))

            # display once every 2 seconds how much data has been logged
            if (i % (logFrequency * 2) == 0):
                print("logging: %d of %d" % (i, logCount))

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
    global imu
    global f

    del (imu)
    f.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
