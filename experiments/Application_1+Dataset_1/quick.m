% configure the paths
clear all
addpath(genpath('helpers'));
my_path = pwd;
cd ../..
addpath(genpath([pwd '/algorithms/']));
addpath(genpath([pwd '/helps/']));
cd(my_path);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
populations = [5, 8, 12, 20];
% build training and test sets by joining populations
X_train = []; Y_train = [];
X_test = []; Y_test = [];
for p = populations,
    [XTr, YTr, XTe, YTe] = getCommunity(p);
    X_train = [X_train XTr];
    Y_train = [Y_train; YTr];
    X_test = [X_test XTe];
    Y_test = [Y_test; YTe];
end

% configure parameters for DMLMJ
params = struct();
params.dim = 10; % the desired number of features in the transformed space.
params.k1 = 5; % positive neighbors
params.k2 = 5; % negative neighbors

% learn a linear transformation using DMLMJ
L = DMLMJ(X_train, Y_train, params);

% Use k=3 to test the performance of knn and DMLMJ
% knn classification using Euclidean
E_Y_hat = knnClassifier(X_train, Y_train, 3, X_test);

% knn classification using DMLMJ
fprintf('Classification accuracies of k-nearest-neighbor using\n');
M_Y_hat = knnClassifier(L'*X_train,Y_train, 3, L'*X_test);
fprintf('1) Supervised settings:\n');
fprintf('Euclidean = %.2f\n', mean(E_Y_hat==Y_test)*100);
fprintf('DMLMJ = %.2f\n\n', mean(M_Y_hat==Y_test)*100);

% Transfer setting.
% Once the linear transformation L is learned,we can use it for other tasks as
% well, for which the source and target tasks are related and share some common structure.
target_populations = [23, 13];
X = []; Y = [];
X_te = []; Y_te = [];
for p = target_populations,
    [XTr, YTr, XTe, YTe] = getCommunity(p);
    X = [X XTr];
    Y = [Y; YTr];
    X_te = [X_te XTe];
    Y_te = [Y_te; YTe];
end

% Use k=3 to test the performance of knn and DMLMJ
% knn classification using Euclidean
E_Y_hat = knnClassifier(X, Y, 3, X_te);

% knn classification using DMLMJ
M_Y_hat = knnClassifier(L'*X, Y, 3, L'*X_te);
fprintf('2) Transfer settings:\n');
fprintf('Euclidean = %.2f\n', mean(E_Y_hat==Y_te)*100);
fprintf('DMLMJ = %.2f\n', mean(M_Y_hat==Y_te)*100);