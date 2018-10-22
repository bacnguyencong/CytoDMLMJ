function ret = F1_score(y_true, y_pred, measure_type)
    stats = confusionmatStats(y_true, y_pred);
    labels = stats.groupOrder;
    
    if (~exist('measure_type', 'var'))
        measure_type = 'macro';
    end
        
    if strcmp(measure_type, 'micro'),
        ret = 0;
        tot = 0;
        for i = 1:length(labels),
            cnt = sum(labels(i) == y_true);
            ret = ret + cnt * stats.Fscore(i);
            tot = tot + cnt;
        end    
        ret = ret / tot;
    elseif strcmp(measure_type, 'macro'),
        ret = mean(stats.Fscore);
    else
        error('Not supported');
    end
end



