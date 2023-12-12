scp logger/* pi@192.168.0.201:/home/pi/cpdrillsensor/logger
ssh pi@192.168.0.201 "cd /home/pi/cpdrillsensor; python logger -d 2"
