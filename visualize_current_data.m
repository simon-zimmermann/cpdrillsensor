close all
data_raw = readtable("output\datalog_current.csv");

figure()
plot(data_raw, "time", {'aquisitionDuration'})
title("aquisitionDuration")

figure()
stackedplot(data_raw,["imu1_accX","imu1_accY","imu1_accZ"],"XVariable","time")
title("Acceleration data IMU1")

figure()
stackedplot(data_raw,["imu2_accX","imu2_accY","imu2_accZ"],"XVariable","time")
title("Acceleration data IMU2")

figure()
stackedplot(data_raw,["temp0","temp1", "temp2", "temp3"],"XVariable","time")
title("Temperature")

figure()
stackedplot(data_raw,["power1Volt","power1MilliAmp","power1MilliWatt","power1ShuntMilliVolt"],"XVariable","time")
title("Power Meter 1")

figure()
stackedplot(data_raw,["power2Volt","power2MilliAmp","power2MilliWatt","power2ShuntMilliVolt"],"XVariable","time")
title("Power Meter 2")

