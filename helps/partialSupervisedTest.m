function Acc = partialSupervisedTest(Data, partitions, Ebest_k, Mbest_k, used_asinh)
%  Perform an experiment on  partial labeled examples

    number_of_tests = size(partitions, 1);
    
    % write all outputs to 'supervised.txt'
    ext = '';
    if used_asinh, ext = 'asinh_'; end;
    file = ['output/', ext , 'partialsupervised.txt'];
    fclose(fopen(file, 'w'));
    
    % accuracies
    %   Acc(1,:,i) accuracies of knn using the Euclidean distances
    %   Acc(2,:,i) accuracies of knn using the DMLMJ
    Acc = zeros(2, 10, number_of_tests); 
	
    for test_id=1:number_of_tests,
        
        clc; fprintf('Running on #test=%d\n',test_id);
        XTr = []; YTr = [];
        XTe = []; YTe = [];
        X   = []; Y   = [];
        
        % Build a test set containing a combination of 10 pieces
        for S=1:10,
            index = partitions(test_id,S);
            XTe   = [XTe Data{index}.XTe];
            YTe   = [YTe;Data{index}.YTe];
            X     = [X  Data{index}.XTr]; 
            Y     = [Y; Data{index}.YTr];
        end
        
        for S=1:10,
            index = partitions(test_id,S);
            XTr   = [XTr Data{index}.XTr];
            YTr   = [YTr;Data{index}.YTr];
            if S > 1,                
               % perform knn on the Euclidean distance
               Acc(1,S,test_id) = testEuclidean(used_asinh,Ebest_k(test_id),XTr,YTr,XTe,YTe,X,Y);
               writeToFile(file, sprintf('%.2f, ', Acc(1,S,test_id)));
               
               % perform knn on the DMLMJ distance
               Acc(2,S,test_id) = testDMLMJ(used_asinh,Mbest_k(test_id), XTr,YTr,XTe,YTe,X,Y); 
               writeToFile(file, sprintf('%.2f\n', Acc(2,S,test_id)));
            end
        end
    end
end
