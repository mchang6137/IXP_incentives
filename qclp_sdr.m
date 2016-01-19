function [OPT, ARG, X, TIME] = qclp_sdr(q_0, ...
                                        P, ...
                                        q, ...
                                        r)

    disp('solving using SDR');
    n = length(q_0);
    
    TIME = cputime;
    cvx_begin sdp quiet
        variable X(n,n) symmetric
        variable x(n)
        minimize(q_0'*x)
        subject to
            x <= 1;
            x >= 0;
            [[X, x]; [x', 1]] >= semidefinite(n+1);
            for i = 1:n
                trace(P(:,:,i)*X) + q(:,i)'*x + r(i) <= 0;
            end
    cvx_end
    TIME = cputime - TIME;
    
    OPT = cvx_optval;
    ARG = x;
end