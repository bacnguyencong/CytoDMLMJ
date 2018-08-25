function [XTr, YTr, XTe, YTe] = getCommunity(id_number)
% get data set from community number #num
% INPUT:
%   num: the number of community
% OUTPUT:
%   XTr: examples by columns  (normalized)
%   YTr: class labels
    
    % read data from two replicates
    fr = [sprintf('data/%02d',id_number) '_rep1HighQ.csv'];
    sc = [sprintf('data/%02d',id_number) '_rep2HighQ.csv'];
    
    X1  = importingData(fr,5000);
    X2  = importingData(sc,5000);
    
    % get 5000 examples for training and other 5000 for testing
    XTr = [X1(1:2500,  :); X2(1:2500,  :)]';
    XTe = [X1(2501:end,:); X2(2501:end,:)]';
    
    % add labels to the data
    YTr = repmat(id_number, 5000,1);
    YTe = repmat(id_number, 5000,1);
end

function X = importingData(name,len)
% randomly subsampling the data
    rp = randperm(len);
    X  = importdata(name);
    X  = X.data(rp(1:len),2:end-1);
end
