%p = [4234; 1603; 9; 5; 1; 28; 1; 1; 59; 17; 9; 1; 81; 288; 1607; 2; 1; 13; 139; 90; 78; 164; 35];
p = [4234; 9; 1; 1; 59; 9; 81; 1607; 1; 139; 78; 35];
%p = [4234; 1; 59; 81; 1; 78];

n = length(p);
Z = (1.1-1)/(1-.05);
C = (log(p)+1)/mean(p);
T_RR = n^2;
T_SA = n^2;
tol = 1E-10;

W = zeros(n);
for i = 1:n
    for j = 1:n
        W(i,j) = p(i) * (p(i)~=p(j)) / (sum(p(1:j)+sum(p(j+1:n))));
    end
end
M = .95*max(W, W');
E = eye(length(p));
q_0 = C;
P = zeros(n, n, n);
q = zeros(n);
for i = 1:n
    P(:,:,i) = Z*(E(:,i)*M(:,i)'+M(:,i)*E(:,i)');
    q(:,i) = -2*(Z*M(:,i) - C(i)*E(:,i));
end
r = 2*C;

% if n <= 25
%     [opt_bf, arg_bf] = brute_force(p, Z*M, C);
% end

% [~, ARG_sdr] = qclp_sdr(q_0, P, q, r);
% [opt_sdr_mr, arg_sdr_mr] = max_rounding(ARG_sdr, Z*M, C);
% [opt_sdr_rr, arg_sdr_rr, exp_sdr_rr] = randomized_rounding(ARG_sdr, Z*M, C, T_RR);

[~, ARG_rlt] = qclp_rlt(q_0, P, q, r);
[opt_rlt_mr, arg_rlt_mr] = max_rounding(ARG_rlt, Z*M, C);
[opt_rlt_rr, arg_rlt_rr, exp_rlt_rr] = randomized_rounding(ARG_rlt, Z*M, C, T_RR);
% 
% [~, ARG_ilcr] = qclp_ilcr(q_0, P, q, r, tol);
% [opt_ilcr_mr, arg_ilcr_mr] = max_rounding(ARG_ilcr, Z*M, C);
% [opt_ilcr_rr, arg_ilcr_rr, exp_ilcr_rr] = randomized_rounding(ARG_ilcr, Z*M, C, T_RR);
%
% [opt_sa, arg_sa] = simulated_annealing(Z*M, C, T_SA);