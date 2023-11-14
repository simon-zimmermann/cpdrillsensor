% Execute data aquisition python script on raspi
shellCommand = 'ssh pi@192.168.1.201 "cd /home/pi/cpdrillsensor; python logger -c 200 -f 500"';
[~, cmdout] = system(shellCommand);

% get third line of output log
% this is the filename of the newly created logfile
newDatalogFile = splitlines(cmdout);
newDatalogFile = newDatalogFile{3};

% Copy newly created file to local machine
% Collect all output files in output folder; save most recent file separately
disp("Gathering file " + newDatalogFile)
shellCommand = sprintf("scp pi@192.168.1.201:/home/pi/cpdrillsensor/output/%s output/%s", newDatalogFile, newDatalogFile);
[~, cmdout] = system(shellCommand);
copyfile("output/" + newDatalogFile, "datalog_current.csv")
