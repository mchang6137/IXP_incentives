function [OPT, ITER, TIME, METHOD, ROUNDING] = test_prefixes(prefixes)
 
    n = length(prefixes);
    Z = (1.1-1)/(1-.05);
    C = (log(prefixes)+1)/mean(prefixes);
    T_RR = n^2;
    T_SA = n^2;
    tol = 1E-10;
    
    OPT = zeros(5,5); EXP = zeros(5,1);
    ITER = zeros(5,1); TIME = zeros(5,1);
    METHOD = ['brute_force'; 'qclp_sdprel'; 'qclp_reflin'; 'qclp_itrlin'; 's_annealing'];
    ROUNDING = ['non_round'; 'rlx_round'; 'max_round'; 'rnd_round'; 'exp_round'];

    W = zeros(n);
    for i = 1:n
        for j = 1:n
            W(i,j) = prefixes(i) * (prefixes(i)~=prefixes(j)) / (sum(prefixes(1:j)+sum(prefixes(j+1:n))));
        end
    end
    M = .95*max(W, W');
    E = eye(length(prefixes));
    q_0 = C;
    P = zeros(n, n, n);
    q = zeros(n);
    for i = 1:n
        P(:,:,i) = Z*(E(:,i)*M(:,i)'+M(:,i)*E(:,i)');
        q(:,i) = -2*(Z*M(:,i) - C(i)*E(:,i));
    end
    r = 2*C;

%     if n <= 24
%         [OPT(1,1), ~, TIME(1)] = brute_force(prefixes, Z*M, C);
%     end
% 
%     [OPT(2,2), ARG_sdr, ~, TIME(2)] = qclp_sdr(q_0, P, q, r);
%     if -Inf < OPT(2,2) < Inf
%         OPT(2,3) = max_rounding(ARG_sdr, Z*M, C);
%         [OPT(2,4), ~, OPT(2,5)] = randomized_rounding(ARG_sdr, Z*M, C, T_RR);
%     end
% 
%     
%     [OPT(3,2), ARG_rlt, ~, TIME(3)] = qclp_rlt(q_0, P, q, r);
%     if -Inf < OPT(3,2) < Inf
%         OPT(3,3) = max_rounding(ARG_rlt, Z*M, C);
%         [OPT(3,4), ~, OPT(3,5)] = randomized_rounding(ARG_rlt, Z*M, C, T_RR);
%     end
%     
%     [OPT(4,2), ARG_ilcr, TIME(4), ITER(4)] = qclp_ilcr(q_0, P, q, r, tol);
%     if -Inf < OPT(4,2) < Inf
%         OPT(4,3) = max_rounding(ARG_ilcr, Z*M, C);
%         [OPT(4,4), ~, OPT(4,5)] = randomized_rounding(ARG_ilcr, Z*M, C, T_RR);
%     end
    
    [OPT(5,1), arg, TIME(5), ITER(5)] = simulated_annealing(Z*M, C, T_SA);
end