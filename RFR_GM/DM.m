sub_regions = 20;
load('RFR_log/IND.mat')
%%

key = keys(IND);
value = uint32(cell2mat(values(IND)));
%%
i=2;
j=1546;

index_i = find(value==i);
RFR_i_list = key(index_i);
index_j = find(value==j);
RFR_j_list = key(index_j);

RFR_i_list_dec = bin2dec(RFR_i_list);
RFR_j_list_dec = bin2dec(RFR_j_list);

% reference: https://www.ilovematlab.cn/thread-321138-1-1.html
[m, n] = meshgrid(RFR_i_list_dec, RFR_j_list_dec');
[res(:,1), res(:,2)] = deal(reshape(m, [], 1), reshape(n, [], 1));

DH = dec2bin(bitxor(res(:,1), res(:,2)));

[length, ~] = size(DH);
DH2 = uint8(zeros(length, 1));
for i = 1:length
    DH2(i) = sum(DH(i,:)=='1');
end
min_Hamming = min(DH2)

