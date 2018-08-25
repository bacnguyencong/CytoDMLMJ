function [Accuracies, Ebest_k, Mbest_k] = supervisedTest(Data, partitions, used_asinh)
%  Perform experiments on labeled examples

    number_of_tests = size(partitions, 1);
    
    % write all outputs to 'supervised.txt'
    ext = '';
    if used_asinh, ext = 'asinh_'; end;
    file = ['output/', ext , 'supervised.txt'];
    fclose(fopen(file, 'w'));
    
    % accuracies
    %   Accuracies(1,:,i) accuracies of knn using the Euclidean distances
    %   Accuracies(2,:,i) accuracies of knn using the DMLMJ
    Accuracies = zeros(2, 10, number_of_tests);
    
    Ebest_k = zeros(10, 1); % best values of k for Euclidean
    Mbest_k = zeros(10, 1); % best values of k for Mahalanobis

    for test_id=1:number_of_tests,
        XTr = []; YTr = [];
        XTe = []; YTe = [];
        clc; fprintf('Running on #test=%d\n',test_id);
        for S=1:10,
            % build training and testing data sets
            index = partitions(test_id, S);
            XTr   = [XTr Data{index}.XTr];
            YTr   = [YTr;Data{index}.YTr];
            XTe   = [XTe Data{index}.XTe];
            YTe   = [YTe;Data{index}.YTe];            
            % S is the species richness.
            if S > 1,
                % perform knn on the Euclidean distance
                [acc, k1] = testEuclidean(used_asinh, -1, XTr, YTr, XTe, YTe);
                Accuracies(1, S, test_id) = acc;
                writeToFile(file, sprintf('%.2f, ', acc));
                
                % perform knn on the DMLMJ distance
                [acc, k2] = testDMLMJ(used_asinh, -1, XTr, YTr, XTe, YTe);
                Accuracies(2, S, test_id) = acc;
                writeToFile(file, sprintf('%.2f\n', acc));
            end
        end
        % saving the best number of nearest neighbors used in kNN.
        Ebest_k(test_id) = k1;
        Mbest_k(test_id) = k2;
    end
end

