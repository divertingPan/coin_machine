function min_Hamming = Feature_matching(key, value, i, j)
% Feature matching
% key = keys(IND);
% value = uint32(cell2mat(values(IND)));

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
min_Hamming = min(DH2);


% min_Hamming = sub_regions;
% for li = 1:length_i_list
%     for lj = 1:length_j_list
%         t1 = cell2mat(RFR_i_list(li));
%         t2 = cell2mat(RFR_j_list(lj));
%         DH = dec2bin(bitxor(bin2dec(t1), bin2dec(t2)));
%         DH = sum(DH == '1');
%         if DH < min_Hamming
%             min_Hamming = DH;
%         end
%     end
% end