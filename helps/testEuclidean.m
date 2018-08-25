function [Acc, best_k] = testEuclidean(used_asinh, k, XTr, YTr, XTe, YTe, X, Y)
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
        % this corresponds to the unsupervised cases.
        if (nargin > 6), X = asinh(X); end;
    end

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
        accuracy = mean(Y_hat==ytv);
        if accuracy > best_accuracy,
            best_accuracy = accuracy;
            best_k = k;
        end
        fprintf('.');
    end
    
    % compute the accuracy on the test set
    if nargin == 6,
        Y_hat = knnClassifier(XTr, YTr, best_k, XTe);        
    else
        Y_hat = knnClassifier(X, Y, best_k, XTe);        
    end
    
    Acc = mean(Y_hat==YTe)*100;    
    fprintf('\n--------------------------------------\n');
    fprintf('Euclidean accuracy=%.2f, k=%d\n', Acc, best_k);
    fprintf('--------------------------------------\n');
end
