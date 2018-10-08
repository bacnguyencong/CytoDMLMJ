function [Acc, best_k] = testDMLMJ(used_asinh, k, XTr, YTr, XTe, YTe, X, Y)
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
        if (nargin > 6),
            X = asinh(X);
            [~, X] = normalizer(XTr, X);
        end;
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
            accuracy = mean(Y_hat==ytv);
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
    
    % test
    if nargin == 6,
        Y_hat = knnClassifier(L'*XTr,YTr,best_k,L'*XTe);
    else
        Y_hat = knnClassifier(L'*X, Y, best_k, L'*XTe);        
    end
    
    Acc = mean(Y_hat==YTe)*100;
    fprintf('\n--------------------------------------\n');
    fprintf('DMLMJ Accuracy=%.2f, k = %d\n', Acc, best_k);
    fprintf('--------------------------------------\n');
end
