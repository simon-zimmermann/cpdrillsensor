#!/bin/bash
pi_shell_log=pi_output.log
ssh -t pi@192.168.1.201 "cd /home/pi/cpdrillsensor; python datalogger -c 1000 -f 500" | tee ${pi_shell_log}

# get second line of output log, and remove special characters
# this is the filename of the newly created logfile
newDatalog=`sed '2q;d' ${pi_shell_log}`
newDatalog=${newDatalog//[$'\r\n']} 

echo "Gathering file ${newDatalog}"
scp pi@192.168.1.201:/home/pi/cpdrillsensor/output/${newDatalog} datalog_current.csv