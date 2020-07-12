function RFR = RFR_GM(IND, I, rings, sub_regions, I_size)

I = rgb2gray(I);
I = imresize(I, [I_size, I_size]);
I = double(I);


%% gradient magnitudes M(x,y)
% reference: Image-based coin recognition using rotation-invariant region binary patterns based on gradient magnitudes

% M = zeros(I_size - 2);
% for x = 2:I_size - 1
%     for y = 2:I_size - 1
%         M(x-1, y-1) = sqrt((I(x+1, y) - I(x-1, y))^2 + (I(x, y+1) - I(x, y-1))^2);
%     end
% end

w = [1, 2, 1;
     0, 0, 0;
     -1, -2, -1];
Mx = imfilter(I, w);
My = imfilter(I, w');
M = sqrt(Mx.^2 + My.^2);
M = M(2:I_size - 1, 2:I_size - 1);


%% RBP template and mean gradient magnitudes of each sub-region

r = (I_size - 2) / 2;
center_point = r;

axis_x = zeros(I_size - 2);
for row = 1:I_size - 2
    axis_x(row,:) = [1:I_size - 2];
end

axis_y = zeros(I_size - 2);
for column = 1:I_size - 2
    axis_y(:,column) = [1:I_size - 2];
end

condition_r = abs(sqrt((axis_x-center_point).^2 + (axis_y-center_point).^2));
condition_angle = atan2(axis_y-center_point, axis_x-center_point)/pi*180+180;

pic_num = 1;
m = zeros(rings, sub_regions);
for ring = 1:rings
    for region = 1:sub_regions
        area_r = condition_r < ring*(r/rings) & condition_r >= (ring-1)*(r/rings);
        area_angle = condition_angle < region*(360/sub_regions) & condition_angle >= (region-1)*(360/sub_regions);
        
        area_need = area_r .* area_angle;
        area_gradient = M .* area_need;
        
%         % save a gif to observe
%         imshow(area_gradient, [], 'border','tight', 'initialmagnification','fit');
%         F=getframe(gcf);
%         I=frame2im(F);
%         [I,map]=rgb2ind(I,256);
%         if pic_num == 1
%             imwrite(I,map,'RFR_log/area.gif','gif', 'Loopcount',inf,'DelayTime',0.1);
%         else
%             imwrite(I,map,'RFR_log/area.gif','gif','WriteMode','append','DelayTime',0.1);
%         end
%         pic_num = pic_num + 1;

        m(ring, region) = sum(area_gradient(:)) / sum(area_need(:));
    end
end


%% Preparation for RFR (formula 3, 4, 5)

M_mu = mean(m(:));
d = abs(m - M_mu);
D_mu = mean(d(:));


%% Get intra RBP and inter RBP

b_intra = d >= D_mu;

b_inter = logical(zeros(rings-1, sub_regions));

for n = 1:rings-1
    for s = 1:sub_regions
        b_inter(n, s) = m(n, s) >= m(n+1, s);
    end
end


%% b to RFR

[length_intra, ~] = size(b_intra);
[length_inter, ~] = size(b_inter);

RFR = zeros(length_intra+length_inter, 1);
for i = 1:length_intra
    RFR(i) = IND(num2str(b_intra(i,:),'%d'));
end
for i = 1:length_inter
    RFR(i+length_intra) = IND(num2str(b_inter(i,:),'%d'));
end