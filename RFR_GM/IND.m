function IND = IND(sub_regions)
% Use IND to convert RBP to RFR
% reference: Rotation and flipping robust region binary patterns for video copy detection
% algorithm 2

IND = containers.Map;
ind = 1;

for x = 1:2^sub_regions
    if mod(x, 100) == 0
        disp([num2str(x), '/', num2str(2^sub_regions)]);
    end
    b = dec2bin(x-1, sub_regions);
    for i_cp = 1:sub_regions
        b = circshift(b, 1);
        CP(i_cp, :) = b;
    end
    FP = fliplr(CP);
    CP_FP = cat(1, CP, FP);
    CP_FP_dec = unique(uint32(bin2dec(CP_FP)));
    [length, ~] = size(CP_FP_dec);
    
    if ~isKey(IND, dec2bin(CP_FP_dec(1), sub_regions))
        for index_map = 1:length    
            IND(dec2bin(CP_FP_dec(index_map), sub_regions)) = ind;
        end
        ind = ind + 1;
    end
end

save('RFR_log/IND.mat', 'IND');

