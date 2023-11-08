from lsm6ds3 import *
import time
import sys
import traceback

# setup for IMU
imu = LSM6DS3(ACC_ODR=ACC_ODR_1_66_KHZ,
              GYRO_ODR=GYRO_ODR_1_66_KHZ,
              enable_acc=ENABLE_ACC_ALL_AXIS,
              enable_gyro=ENABLE_GYRO_ALL_AXIS,
              acc_interrupt=False,
              gyro_interrupt=False,
              acc_scale=ACC_SCALE_16G,
              gyro_scale=GYRO_SCALE_2000DPS)

def main():
    global imu
    while 1:
        try:
            accData = imu.getAccData()
            gyroData = imu.getGyroData()
            print("acc: x:%.2f y:%.2f z:%.2f    gyro: x:%.2f y:%.2f z:%.2f" % (accData[0], accData[1], accData[2], gyroData[0], gyroData[1], gyroData[2]))
#            print("acc: x:%.2f" % (accData[1]))
#            print('Accelerometer data [X, Y, Z]: %s' % imu.getAccData()) # for raw data, imu.getAccData(raw=True)
#            print('Gyroscope data [X, Y, Z]: %s' % imu.getGyroData()) # for raw data, imu.getGyroData(raw=True)
#            time.sleep(0.1)
        except KeyboardInterrupt:
            del(imu)
            sys.exit(0)
        except Exception as e:
            print('Caught exception %s' % e)
            traceback.print_exc()
            del(imu)
            sys.exit(0)

if __name__ == '__main__':
    main()

