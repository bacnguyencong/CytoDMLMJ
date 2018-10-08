function runExps()
%% Application 1: Synthetic microbial communities
%  Dataset 1: In Silico Bacterial Communities
    
    rng('default');
    % setup paths and helper functions
    setup();
    num_of_datasets = 2;
    used_asinh = 0;
    
    % load training and testing sets
    if ~exist('save/dataAll.mat','file'),
        fprintf('Reading data\n');
        Data = readAllDataSets(1:16);
        % save for the reproducibility
        save(fullfile('save/dataAll.mat'),'Data','-v7.3');
    else
        % these are patitions used in our experiments
        fprintf('Loading all data sets...\n');
        load(fullfile('save/dataAll.mat'));
    end
    
    Eu = zeros(num_of_datasets, num_of_datasets);
    Ma = zeros(num_of_datasets, num_of_datasets);
    
    for i=1:num_of_datasets,
        for j=1:num_of_datasets,
            XTr = Data{i}.XTr;
            YTr = Data{i}.YTr;
            XTe = Data{j}.XTe;
            YTe = Data{j}.YTe;
            Ma(i, j) = testDMLMJ(used_asinh, -1, XTr, YTr, XTe, YTe);
            Eu(i, j) = testEuclidean(used_asinh, -1, XTr, YTr, XTe, YTe);
        end
    end
    dlmwrite('output/DMLMJ.txt', Ma, 'delimiter', ',', 'precision', 4);
    dlmwrite('output/Euclidean.txt', Eu, 'delimiter', ',', 'precision', 4);
end

function setup()
% setup the directories
    addpath(genpath('helpers'));
    my_path = pwd;
    cd ../..
    addpath(genpath([pwd '/algorithms/']));
    addpath(genpath([pwd '/helps/']));
    cd(my_path);
end

