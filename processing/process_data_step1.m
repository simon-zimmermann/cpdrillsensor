close all
clear

% use only the file datalog_current.csv or all data
use_only_current = false;

output_folder = "../output/";
concat_data = [];

if use_only_current
    loaded = readtable("datalog_current.csv");
    loaded.fileID = ones(height(loaded), 1);
    concat_data = [concat_data loaded];
else
    files = {dir(fullfile(output_folder + "*.csv")).name};
    files = convertCharsToStrings(files);
    lastABSTime = 0;
    for fileID = 1:length(files)
        loaded = readtable(output_folder + files(fileID));
        loaded.fileID = repmat(fileID, height(loaded), 1);
        loaded.absTime = repmat(lastABSTime, height(loaded), 1);
        loaded.absTime = loaded.absTime + loaded.time;
        lastABSTime = loaded.absTime(end);
        concat_data = [concat_data; loaded];
    end
end

%sensordata_TT = table2timetable(concat_data,'RowTimes','absTime');

%sensordata_struct = table2struct(timetable2table(sensordata_TT), 'ToScalar', true);

%s.time = concat_data.absTime
%s.signals.values.aq = concat_data.aquisitionDuration
elems(1) = Simulink.BusElement;
elems(1).Name = 'Sine';
elems(2) = Simulink.BusElement;
elems(2).Name = 'BigSine';
SineBus = Simulink.Bus;
SineBus.Elements = elems;
clear elems;
elems(1) = Simulink.BusElement;
elems(1).Name = 'SineBus';
elems(1).DataType = 'Bus: SineBus';
elems(2) = Simulink.BusElement;
elems(2).Name = 'Cosine';
SinusoidBus = Simulink.Bus;
SinusoidBus.Elements = elems;
sampleTime = 0.01;
numSteps = 1001;
time = sampleTime*(0:numSteps-1);
time = time';

data = sin(2*pi/3*time);
cosdata = cos(2*pi/3*time);
ampdata = 2*data;

clear busin;
busin.Cosine = timeseries(cosdata,time);
busin.SineBus.Sine = timeseries(data,time);
busin.SineBus.BigSine = timeseries(ampdata,time);

