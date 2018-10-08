function Data = readAllDataSets(list_of_datasets)
%% Load data sets to the  matlab cells
    num_com = length(list_of_datasets);
    Data    = cell(num_com,1);
    for i=1:num_com,
        fprintf('Reading data set (%d)\n', list_of_datasets(i));
        %----------------------------------------------%
        [Data{i}.XTr, Data{i}.YTr, Data{i}.XTe, Data{i}.YTe] ...
                     = getCommunity(list_of_datasets(i));
        Data{i}.name = list_of_datasets(i); % the community name
        %----------------------------------------------%
    end
end