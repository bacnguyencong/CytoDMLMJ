function [XTr, YTr, XTe, YTe] = getCommunity(id_number)
% get data set from community number #num
% INPUT:
%   num: the number of community
% OUTPUT:
%   XTr: examples by columns  (normalized)
%   YTr: class labels
    
    % read data from two replicates
    data = [sprintf('data/%d',id_number) '_data.csv'];
    label = [sprintf('data/%d',id_number) '_label.csv'];
    
    num_samples = 10000;
    [X, Y] = importingData(data, label, num_samples);
    
    % get 5000 examples for training and other 5000 for testing
    XTr = X(1:num_samples/2,:)';
    YTr = Y(1:num_samples/2);
    
    XTe = X(num_samples/2+1:end, :)';
    YTe = Y(num_samples/2+1:end);
end

function [X, Y] = importingData(data, label, len)
% randomly subsampling the data
    rp = randperm(len);
    X  = importdata(data);
    X  = X(2:end,:); % delete the first row
    Y  = importdata(label);
    X  = X(rp(1:len), :);
    Y  = Y(rp(1:len));
end
