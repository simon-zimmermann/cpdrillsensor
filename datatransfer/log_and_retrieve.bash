#!/bin/bash
pi_shell_log=pi_output.log
ssh -t pi@192.168.1.201 "cd /home/pi/cpdrillsensor; python datalogger" | tee ${pi_shell_log}
newDatalog=`sed '2q;d' ${pi_shell_log}`
newDatalog=${newDatalog//[$'\r\n']} # remove special characters
echo "Gathering file ${newDatalog}"
scp pi@192.168.1.201:/home/pi/cpdrillsensor/output/${newDatalog} datalog_current.csv