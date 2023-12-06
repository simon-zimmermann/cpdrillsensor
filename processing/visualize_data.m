close all
data_raw = readtable("datalog_current.csv");
 
figure()
plot(data_raw, "time", {'aquisitionDuration', 'remainingTime'})
title("aquisitionDuration, remainingTime")

figure()
s = stackedplot(data_raw,["acc1X","acc1Y","acc1Z"],"XVariable","time");
title("Acceleration data IMU1")

figure()
stackedplot(data_raw,["acc2X","acc2Y","acc2Z"],"XVariable","time")
title("Acceleration data IMU2")

figure()
stackedplot(data_raw,["temp0","temp1", "temp2", "temp3"],"XVariable","time")
title("Temperature")

figure()
stackedplot(data_raw,["power1MilliWatt","power2MilliWatt"],"XVariable","time")
title("Power Meter")

