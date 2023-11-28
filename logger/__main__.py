import time
import sys
import traceback
import argparse
from oclock import Timer

from Sensor_accel import Sensor_accel
from Sensor_NTC import Sensor_NTC
from Sensor_power import Sensor_power


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(prog='datalogger',
                                     description='Reads data of attached sensors, and writes them to a .csv file. \
                                     Can only run on a Raspi')
    parser.add_argument('-d', '--duration', type=int,
                        help='Logging duration in seconds',
                        default=2)
    parser.add_argument('-f', '--frequency', type=int,
                        help='How many data points should be logged per second',
                        default=52)
    parser.add_argument('-t', '--trigger', action="store_true",
                        help='Wait with file creation and logging until the trigger condition has been met.',
                        default=False)
    args = parser.parse_args()

    logFrequency = args.frequency  # Hz
    logDuration = args.duration
    waitTrigger = args.trigger
    print("Logging for a total of %d seconds, with a frequency of %d per second. Waiting for trigger is %s." %
          (logDuration, logFrequency, "enabled" if waitTrigger else "disabled"))

    # initialize sensors
    accelerator = Sensor_accel()
    ntc = Sensor_NTC()
    power = Sensor_power()

    # determine filename before waiting for trigger to make analysis of stout easier
    filename = "sensorlog_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    print("logging to file:\n" + filename)

    # wait for trigger if requested
    if (waitTrigger):
        print("Waiting for trigger condition")
        sys.stdout.flush()
        while (not power.is_triggered()):
            time.sleep(1)
        print("Trigger condition met")

    # file setup
    f = open("output/" + filename, "x")
    f.write("time, aquisitionDuration, remainingTime,%s,%s,%s\n" %
            (accelerator.get_csv_header(),
             ntc.get_csv_header(),
             power.get_csv_header()))

    # the second the file was created
    time_absolute_start = time.time()
    time_since_start = 0
    logCount = 0

    # loop timer
    timer = Timer(interval=1 / logFrequency)
    while (time_since_start < logDuration):
        # save exact (but not absolute) time of loop start
        perfcounter_loopstart = time.perf_counter()

        try:
            # grab data from sensors
            accData = accelerator.get_data()
            ntcData = ntc.get_data()
            powerData = power.get_data()

            # Calculate aquisition duration
            aquisitionDuration = time.perf_counter() - perfcounter_loopstart

            # refresh elapsed time since logging started
            time_since_start = time.time() - time_absolute_start

            # Roughly calculate remaining time until next loop.
            # Not used for loop timing; only for analysis
            remainingTime = (1 / logFrequency) - aquisitionDuration

            # Write data to file
            f.write("%.3f,%.6f,%.6f,%s,%s,%s\n" %
                    (time_since_start, aquisitionDuration, remainingTime,
                     accData,
                     ntcData,
                     powerData))

            # print to stdout once every 2 seconds how much data has been logged
            logCount = logCount + 1
            if (logCount % (logFrequency * 2) == 0):
                print("logging: entry #%d at t=%fs" % (logCount, time_since_start))

            # actual loop timing function
            timer.checkpt()

        except Exception as e:
            print('Caught exception %s' % e)
            traceback.print_exc()
            f.close()
            sys.exit(0)

    print("Logging finished")
    f.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
