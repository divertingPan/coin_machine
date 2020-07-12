function evaluate(test_namelist, std_namelist, IND, rings, sub_regions, I_size)

[test_length, ~] = size(test_namelist);
[std_length, ~] = size(std_namelist);

key = keys(IND);
value = uint32(cell2mat(values(IND)));
fid = fopen('RFR_log/result.csv','a');
fprintf(fid, '%s,%s,%s\n', 'test_file', 'similar_coin', 'score');

for i_test = 3:test_length
    min_distance = 10*sub_regions*rings*sub_regions;
    I1 = imread(['testing_img_seg/', test_namelist(i_test).name]);
    for i_std = 3:std_length
        
        disp([num2str(i_test-2), '/', num2str(i_std-2), '  ', num2str(test_length-2), '-', num2str(std_length-2)]);
        
        I2 = imread(['standard_img/', std_namelist(i_std).name]);
        distance = Hamming_distance(IND, key, value, I1, I2, rings, sub_regions, I_size);
        
        if distance < min_distance
            min_distance = distance;
            STD = std_namelist(i_std).name;
            TEST = test_namelist(i_test).name;
        end
    end
    fprintf(fid, '%s,%s,%d\n', TEST, STD, min_distance);
end
fclose(fid);
