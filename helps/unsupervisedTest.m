function Accuracies = unsupervisedTest(Data, partitions, Ebest_k, Mbest_k, used_asinh)
%  Perform an experiment on  unlabeled labeled examples

    number_of_tests = size(partitions,1);    
    % write all outputs to 'supervised.txt'
    ext = '';
    if used_asinh, ext = 'asinh_'; end;
    file = ['output/', ext , 'unsupervised.txt'];
    fclose(fopen(file, 'w'));

    % accuracies
    % Accuracies(1,:,i) accuracies of knn using the Euclidean distances
    % Accuracies(2,:,i) accuracies of knn using the DMLMJ
    Accuracies = zeros(2, 10, number_of_tests);
    
    file = 'output/unsupervised.txt';
    fclose(fopen(file, 'w'));
	
    for test_id=1:number_of_tests,
        clc; fprintf('Running on #test=%d\n',test_id);
        XTr = []; YTr = [];
        XTe = []; YTe = [];
        X   = []; Y   = [];
        
        % Build a test set containing a combination of 10 pieces
        for S=1:10,
            index = partitions(test_id,S);
            XTe   = [XTe  Data{index}.XTe];
            YTe   = [YTe; Data{index}.YTe];
            X     = [X    Data{index}.XTr]; 
            Y     = [Y;   Data{index}.YTr];
        end
        
        for S=11:20,
            index = partitions(test_id,S);
            XTr   = [XTr  Data{index}.XTr];
            YTr   = [YTr; Data{index}.YTr];
            if S > 11,               
               Accuracies(1,S,test_id) = testEuclidean(used_asinh, Ebest_k(test_id), XTr, YTr, XTe, YTe, X, Y);
               writeToFile(file, sprintf('%.2f, ', Accuracies(1,S,test_id)));

               Accuracies(2,S,test_id) = testDMLMJ(used_asinh, Mbest_k(test_id), XTr, YTr, XTe, YTe, X, Y);
               writeToFile(file, sprintf('%.2f\n', Accuracies(2,S,test_id)));
            end
        end
    end
end







