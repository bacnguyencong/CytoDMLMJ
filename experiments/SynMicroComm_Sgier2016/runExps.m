function runExps(used_asinh)
%% Application 1: Synthetic microbial communities
%  Dataset 2: In Silico Autofluorescent Microbial Communities
    
    rng('default');
    
    % setup paths and helper functions
    setup();
    
    % run experiment
    number_of_tests = 10;
    list_of_datasets  = [1 2 3 4 5 6 7 9 10 11 12 13 14 15 16 17 18  21 22 23 24 27 28 30 31 32 33 34 35];
    number_of_communities = length(list_of_datasets);

    % load training and testing sets
    if ~exist('save/dataAll.mat','file'),
        fprintf('Reading data\n');
        
        % take randomly combinations of commnities
        rp = zeros(number_of_tests, number_of_communities);
        for i = 1:number_of_tests,
            rp(i,:) = randperm(number_of_communities);
        end
        
        Data = readAllDataSets(list_of_datasets);
        
        % save for the reproducibility
        save(fullfile('save/dataAll.mat'),'Data','-v7.3');
        save(fullfile('save/order.mat'),'rp','-v7.3');
    else
        % these are patitions used in our experiments
        fprintf('Loading all data sets...\n');
        load(fullfile('save/dataAll.mat'));
        load(fullfile('save/order.mat'));
    end

    % supervised test
    [Ebest_k, Mbest_k] = supervisedTest(Data, rp, used_asinh);
    fprintf('Finishing supervised test\n'); clc;
    
    % partial supervised test
    partialSupervisedTest(Data, rp, Ebest_k, Mbest_k, used_asinh);
    fprintf('Finishing partial supervised test\n'); clc;

    % unsupervised test
    unsupervisedTest(Data, rp, Ebest_k, Mbest_k, used_asinh);
    fprintf('Finishing unsupervised test\n'); clc;
end

function setup()
    addpath(genpath('helpers'));
    my_path = pwd;
    cd ../..
    addpath(genpath([pwd '/algorithms/']));
    addpath(genpath([pwd '/helps/']));
    cd(my_path);
end

