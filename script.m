p = [4234; 1603; 9; 5; 1; 28; 1; 1; 59; 17; 9; 1; 81; 288; 1607; 2; 1; 13; 139; 90; 78; 164; 35];
% %p = [4234; 9; 1; 1; 59; 9; 81; 1607; 1; 139; 78; 35];
% %p = [4234; 1; 59; 81; 1; 78];
[opt, iter, time, method, rounding] = test_prefixes(p);

% OPT = zeros(5,5,5,10);
% ITER = zeros(1,5,5,10);
% TIME = zeros(1,5,5,10);

% for i = 5:5
%     n = 5*2^(i-1);
%     for t = 1:10
%         disp(strcat(num2str(n),',',num2str(t)));
%         prefixes = zeros(n, 1);
%         for j = 1:3*n/5
%             prefixes(j) = unidrnd(100);
%         end
%         for j = 3*n/5+1:4*n/5
%             prefixes(j) = unidrnd(400) + 100;
%         end
%         for j = 4*n/5+1:n
%             prefixes(j) = unidrnd(1500) + 500;
%         end 
%         [OPT(:,:,i,t), ITER(:,:,i,t), TIME(:,:,i,t), METHOD, ROUNDING] = test_prefixes(prefixes);
%     end
% end
