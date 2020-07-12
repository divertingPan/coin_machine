function distance = Hamming_distance(IND, key, value, I1, I2, rings, sub_regions, I_size)
RFR1 = RFR_GM(IND, I1, rings, sub_regions, I_size);
RFR2 = RFR_GM(IND, I2, rings, sub_regions, I_size);

[length, ~] = size(RFR1);
min_Hamming = zeros(length, 1);
for i = 1:length
    min_Hamming(i) = Feature_matching(key, value, RFR1(i), RFR2(i));
end

distance = sum(min_Hamming);