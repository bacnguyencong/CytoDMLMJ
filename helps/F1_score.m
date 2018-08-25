function ret = F1_score(y_true, y_pred)
    stats = confusionmatStats(y_true, y_pred);
    labels = stats.groupOrder;
    
    ret = 0;
    tot = 0;
    for i = 1:length(labels),
        cnt = sum(labels(i) == y_true);
        ret = ret + cnt * stats.Fscore(i);
        tot = tot + cnt;
    end    
    ret = ret / tot;
end

