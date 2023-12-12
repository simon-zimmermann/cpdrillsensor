scp logger/* pi@192.168.0.201:/home/pi/cpdrillsensor/logger
ssh pi@192.168.0.201 "cd /home/pi/cpdrillsensor; python logger -d 2" | Tee-Object -Variable cmdOut
$filename = $cmdOut.split("`r?`n")[2]
Write-Output "Retrieving logfile $filename"
scp pi@192.168.0.201:/home/pi/cpdrillsensor/output/$filename output/$filename
Copy-Item output/$filename processing/datalog_current.csv
