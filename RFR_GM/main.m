rings = 12;
sub_regions = 20;
I_size = 256;

IND = IND(sub_regions);
load('RFR_log/IND.mat')
disp('IND loaded');

test_namelist = dir('testing_img_seg');
std_namelist = dir('standard_img');

evaluate(test_namelist, std_namelist, IND, rings, sub_regions, I_size);
