function [XTr, XTe] = normalizer(XTr, XTe)
end

function [XTr, XTe] = normalizer1(XTr, XTe)
%% Normalize data so that std=1 and m=0
% INPUT
%   XTr: (d x n) training examples
%   XTe: (d x m) test examples
% OUTPUT
%   XTr and XTe are normalized
    m = mean(XTr,2);
    s = std(XTr,0,2);
    s(abs(s)<eps) = 1e-9;    
    XTr = bsxfun(@rdivide,bsxfun(@minus,XTr,m),s);    
    if nargin == 2 && ~isempty(XTe);
        XTe = bsxfun(@rdivide,bsxfun(@minus,XTe,m),s);    
    end
end