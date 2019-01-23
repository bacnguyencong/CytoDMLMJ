function [XTr, YTr, XTe, YTe] = getCommunity(id_number)
% get data set from community number #num
% INPUT:
%   num: the number of community
% OUTPUT:
%   XTr: examples by columns  (normalized)
%   YTr: class labels
    
    % read data from two replicates
    data = [sprintf('data/Samples/Samples%d',id_number) '_CD.csv'];
    label = [sprintf('data/Labels/Labels%d',id_number) '_label.csv'];
    
    num_samples = 40000;
    [X, Y, num_samples] = importingData(data, label, num_samples);
    

    % get 20000 examples for training and other 20000 for testing
    XTr = X(1:ceil(num_samples/2),:)';
    YTr = Y(1:ceil(num_samples/2));
    
    XTe = X(ceil(num_samples/2)+1:end, :)';
    YTe = Y(ceil(num_samples/2)+1:end);
end

function [X, Y, len] = importingData(data, label, len)
% randomly subsampling the data
    X  = importdata(data);
    Y  = importdata(label);
    Y = Y.data;
    len = min(len, length(Y));    
    rp = randperm(len);
    X  = X(rp(1:len), :);
    Y  = Y(rp(1:len));
end
