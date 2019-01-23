function Data = readAllDataSets(list)
    num_com = length(list);
    Data    = cell(num_com,1);
    for i=1:num_com,
        fprintf('Reading data set (%d)\n', list(i));
        %----------------------------------------------%
        [Data{i}.XTr, Data{i}.YTr, Data{i}.XTe, Data{i}.YTe] ...
                     = getData(list(i));
        Data{i}.name = list(i); % the community name
        %----------------------------------------------%
    end
end


