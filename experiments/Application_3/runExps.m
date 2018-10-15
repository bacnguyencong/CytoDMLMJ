function runExps()
%% Application 1: Synthetic microbial communities
%  Dataset 1: In Silico Bacterial Communities
    
    rng('default');
    % setup paths and helper functions
    setup();
    num_of_datasets = 14;
    used_asinh = 0;
    
    % load training and testing sets
    if ~exist('save/dataAll.mat','file'),
        fprintf('Reading data\n');
        Data = readAllDataSets(34:47);
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
            Ma(i, j) = testDMLMJ(used_asinh, -1, XTr, YTr, XTe, YTe, sprintf('%d.%d', i, j));
            Eu(i, j) = testEuclidean(used_asinh, -1, XTr, YTr, XTe, YTe, sprintf('%d.%d', i, j));
        end
    end
    dlmwrite('output/DMLMJ.txt', Ma, 'delimiter', ',', 'precision', 4);
    dlmwrite('output/Euclidean.txt', Eu, 'delimiter', ',', 'precision', 4);
end

function setup()
% setup the directories
    addpath(genpath('./helpers'));
    my_path = pwd;
    cd ../..
    addpath(genpath([pwd '/algorithms/']));
    addpath(genpath([pwd '/helps/']));
    cd(my_path);
end

function [Acc, best_k] = testDMLMJ(used_asinh, k, XTr, YTr, XTe, YTe, filename)
% perform experiments with knn using the Euclidean distances
% INPUT:
%   used_asinh: whether to use function f(x) = asinh(x) to transform the data
%   k: the nearest neighbors used in the k-nn classifier
%   XTr: the matrix of training examples (each example is represented as a column)
%   YTr: the training labels
%   XTe: the matrix of test examples (each example is represented as a column)
%   YTe: the test labels
%   X: the matrix of examples used to test the unsupervised cases.
%   Y: the labels of each examples in the matrix X
% OUTPUT:
%   Acc: the accuracies
%   best_k: the best number of nearest neighbors used in the k-nn
%       classfier.

    % transform the data using the asinh function
    if used_asinh,
        XTr = asinh(XTr);
        XTe = asinh(XTe);
    end
    
    % normalize the data
    [XTr, XTe] = normalizer(XTr, XTe);  
    
    % initial values
    best_accuracy = -Inf;
    best_d = -1;
    best_k = k; 
    min_k = k; 
    max_k = k;

    if k < 1,
        best_k = -1; min_k = 1; max_k = 21;
    end
    
    % cross-validation for k
    c   = cvpartition(YTr,'holdout', 0.3);
    xtr = XTr(:,c.training); ytr = YTr(c.training);
    xtv = XTr(:,c.test);     ytv = YTr(c.test); 
    
    % configuration
    params.dim = size(XTr,1);
    params.knn = k;
    
    for k=min_k:max_k,
        % learning a linear transformation       
        params.k1 = min(10, max(k, 5));
        params.k2 = min(10, max(k, 5));
        L = DMLMJ(xtr, ytr, params);
        
        for d=2:size(xtr,1),
            Y_hat = knnClassifier(L(:,1:d)'*xtr,ytr,k,L(:,1:d)'*xtv);
            accuracy = F1_score(ytv, Y_hat);
            % save the best parameters
            if accuracy > best_accuracy, 
                best_accuracy = accuracy;
                best_k = k;
                best_d = d;
            end;
            fprintf('.');
        end
    end
    
    % learn DMLMJ on the best parameters
    params = struct();
    params.knn = best_k;
    params.dim = best_d;
    params.k1 = min(10, max(best_k,5));
    params.k2 = min(10, max(best_k,5));
    L = DMLMJ(XTr, YTr, params);
    
    Y_hat = knnClassifier(L'*XTr,YTr,best_k,L'*XTe);
    
    Acc = F1_score(YTe, Y_hat); 
    fprintf('\n--------------------------------------\n');
    fprintf('DMLMJ Accuracy=%.2f, k = %d\n', Acc, best_k);
    fprintf('--------------------------------------\n');
    
    
    newSubFolder=sprintf('output/DMLMJ/');
    if ~exist(newSubFolder, 'dir')
        mkdir(newSubFolder);
    end

    % DMLMJ uses the set of features that provifes the best F1 score
    test_file = [newSubFolder  filename];
    label_file= [newSubFolder  filename '_preddiction'];
    csvwrite(test_file, [(L'*XTe)' YTe]);
    csvwrite(label_file, [YTe Y_hat]);

    % DMLMJ uses all features
    params.knn = best_k;
    params.dim = size(XTr,1);
    params.k1 = min(10, max(best_k,5));
    params.k2 = min(10, max(best_k,5));
    L = DMLMJ(XTr, YTr, params);

    test_all_file = [newSubFolder  filename '_test_all'];
    label_all_file = [newSubFolder  filename '_test_all_preddiction'];
    csvwrite(test_all_file, [(L'*XTe)' YTe]);
    Y_hat = knnClassifier(L'*XTr,YTr,best_k,L'*XTe);
    csvwrite(label_all_file, [YTe Y_hat]);
end


function [Acc, best_k] = testEuclidean(used_asinh, k, XTr, YTr, XTe, YTe, filename)
    % transform the data using the asinh function
    if used_asinh,
        XTr = asinh(XTr);
        XTe = asinh(XTe);
    end
    
    % normalize the data
    [XTr, XTe] = normalizer(XTr, XTe);

    best_accuracy = -Inf;
    best_k = k;
    min_k = k;
    max_k = k;
        
    % auto tune the number of nearest neighbors
    if k < 1,
        best_k = -1; min_k = 1; max_k = 21;
    end
    
    % cross validation for k
    COV = cvpartition(YTr,'holdout', 0.3);
    xtr = XTr(:,COV.training); ytr = YTr(COV.training);
    xtv = XTr(:,COV.test);     ytv = YTr(COV.test);
    
    for k=min_k:max_k,
        Y_hat = knnClassifier(xtr,ytr,k,xtv);
        accuracy = F1_score(ytv, Y_hat);
        if accuracy > best_accuracy,
            best_accuracy = accuracy;
            best_k = k;
        end
        fprintf('.');
    end
    
    % compute the accuracy on the test set
    Y_hat = knnClassifier(XTr, YTr, best_k, XTe);        

    
    Acc = F1_score(YTe, Y_hat);   
    fprintf('\n--------------------------------------\n');
    fprintf('Euclidean accuracy=%.2f, k=%d\n', Acc, best_k);
    fprintf('--------------------------------------\n');
    
    newSubFolder=sprintf('output/Euclidean/');
    if ~exist(newSubFolder, 'dir')
        mkdir(newSubFolder);
    end
    % save the output
    test_file = [newSubFolder  filename];
    csvwrite(test_file, [XTe' YTe]);
    label_file= [newSubFolder  filename '_preddiction'];
    csvwrite(label_file, [YTe Y_hat]);
end


