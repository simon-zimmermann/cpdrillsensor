close all

% use only the file datalog_current.csv or all data
use_only_current = false;

output_folder = "../output/";


%% determine which files to load
if use_only_current
    files = "datalog_current.csv";
else
    files = {dir(fullfile(output_folder + "*.csv")).name};
    files = output_folder + convertCharsToStrings(files);
end

%% load files into concat_data
concat_data = [];
lastABSTime = 0;
for fileID = 1:length(files)
    loaded = readtable(files(fileID));
    loaded.fileID = repmat(fileID, height(loaded), 1);
    loaded.absTime = repmat(lastABSTime, height(loaded), 1);
    loaded.absTime = loaded.absTime + loaded.time;
    lastABSTime = loaded.absTime(end);
    concat_data = [concat_data; loaded];
end

%fix name of first column
concat_data.Properties.VariableNames(1) = "relativeTime";

% add trigger to end simulation: fileID = -1
concat_data.fileID(end) = -1;

%% setup simulink bus object
clear sensorData
clear sensorDataType
clear elems

for i = 1:(width(concat_data) - 1) % ignore last column, this is the absolute time
    elems(i) = Simulink.BusElement;
    colname = concat_data.Properties.VariableNames{i};
    elems(i).Name = colname;
    sensorData.(colname) = timeseries(concat_data.(colname),concat_data.absTime);
end
sensorDataType = Simulink.Bus;
sensorDataType.Elements = elems;


