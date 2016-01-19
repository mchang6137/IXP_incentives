function [OPT, ARG] = qclp_ilsdr(q_0, ...
                                 P, ...
                                 q, ...
                                 r, ...
                                 tol)

    n = length(q_0);
    Pp = zeros(size(P));
    Pm = zeros(size(P));
    for i = 1:n
        [Pp(:, :, i), Pm(:, :, i)] = matrix_decomposition(P(:, :, i));
    end
    
    x_0 = ones(n,1);
    OPT = q_0'*x_0;
    converged = 0;
    
    while ~converged
        X_0 = x_0*x_0';
        constraint = zeros(n,1);
        for i = 1:n
            constraint(i) = max(0, trace(Pp(:,:,i)'*X_0) + q(:,i)'*x_0 + r(i) - trace(Pm(:, :, i)'*X_0));
        end
        cvx_begin sdp
            variable X(n,n);
            variable x(n);
            minimize(q_0'*x)
            subject to
                x <= 1;
                x >= 0;
                [[X, x]; [x', 1]] >= semidefinite(n+1);
                for i = 1:n
                    trace(Pp(:,:,i)'*X) + q(:,i)'*x + r(i) <= trace(Pm(:, :, i)*X_0)+2*x_0'*Pm(:, :, i)*(x-x_0) + constraint(i);
                end
         cvx_end
         
         if OPT-cvx_optval < tol
             converged = 1;
         end
         OPT = cvx_optval;
         ARG = x;
         x_0 = x; 
    end
end