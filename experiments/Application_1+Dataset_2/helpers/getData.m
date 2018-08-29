function [XTr, YTr, XTe, YTe] = getData(num)
    listing = dir(['data/' sprintf('%02d', num) '*.csv']);    
    XTr = [];  XTe = [];
    
    for i = 1:length(listing),
        X   = importdata(['data/' listing(i).name]);
        n   = size(X.data, 1);
        rp  = randperm(n);
        cant = ceil(n/2);
        XTr = [XTr; X.data(rp(1:cant), 2:end-1)];
        XTe = [XTe; X.data(rp(cant+1:end), 2:end-1)];
    end
    
    rp = randperm(size(XTr, 1));
    XTr = XTr(rp(1:1000),:);
    
    rp = randperm(size(XTe, 1));
    XTe = XTe(rp(1:1000),:);
    
    YTr = repmat(num, size(XTr, 1), 1);
    YTe = repmat(num, size(XTe, 1), 1);
    XTr = XTr';
    XTe = XTe';
end