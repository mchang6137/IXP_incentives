function [OPT, ARG, X, TIME] = qclp_rlt(q_0, ...
                                        P, ...
                                        q, ...
                                        r)

    disp('solving using RLT');
    n = length(q_0);

    TIME = cputime;
    constraint = zeros(n,1);
    y = ones(n,1);
    for i = 1:n
        constraint(i) = max(0, norm((P(:, :, i)*eye(n)), 'fro') + q(:, i)'*y + r(i));
    end
    cvx_begin quiet
        variable x(n);
        variable X(n,n);
        minimize(q_0'*x)
        subject to
            for i = 1:n
                norm((P(:, :, i).*X), 'fro') + q(:, i)'*x + r(i) <= constraint(i);
                for j = 1:n
                    X(i,j) - x(i) - x(j) >= -1;
                    X(i,j) - x(j) <= 0;
                    X(i,j) - x(i) <= 0;
                    X(i,j) >= 0;
                end
            end
    cvx_end
    TIME = cputime - TIME;
         
    OPT = cvx_optval;
    ARG = x;
end