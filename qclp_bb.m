function [OPT, ARG, u, l] = qclp_bb(q_0, ...
                                    P, ...
                                    q, ...
                                    r, ...
                                    u, ...
                                    l, ...
                                    tol, ...
                                    OPT, ...
                                    ARG)
    
	n = length(q_0);
    disp(u');
    disp(l');
    
    cvx_begin quiet
        variable x(n);
        variable X(n,n);
        minimize(q_0'*x)
        subject to
            for i = 1:n
                sum(sum(P(:, :, i).*X)) + q(:, i)'*x + r(i) <= 0;
                for j = 1:n
                    X(i,j) - u(j)*x(i) - u(i)*x(j) >= -u(i)*u(j);
                    X(i,j) - l(j)*x(i) - u(i)*x(j) <= -u(i)*l(j);
                    X(i,j) - u(j)*x(i) - l(i)*x(j) <= -l(i)*u(j);
                    X(i,j) - l(j)*x(i) - l(i)*x(j) >= -l(i)*l(j);
                end
            end
    cvx_end
    
    if cvx_optval < OPT
        OPT = cvx_optval; ARG = x;
        exclude = zeros(n,1);
        while 1
            index = argmax_diff(x, X, tol, exclude);
            if index
                exclude(index) = 1;
                u_split = u; l_split = l;
                u_split(index) = (u_split(index) + l_split(index)) / 2;
                l_split(index) = u_split(index);
                [OPT_u, ARG_u] = qclp_bb(q_0, P, q, r, u_split, l, tol, OPT, ARG);
                [OPT_l, ARG_l] = qclp_bb(q_0, P, q, r, u, l_split, tol, OPT_u, ARG);
                if OPT_u <= OPT_l
                    OPT = OPT_u; ARG = ARG_u;
                else
                    OPT = OPT_l; ARG = ARG_l;
                end
            else
                break
            end
        end
    end
end        