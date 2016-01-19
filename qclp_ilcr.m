function [OPT, ARG, TIME, ITER] = qclp_ilcr(q_0, ...
                                            P, ...
                                            q, ...
                                            r, ...
                                            tol)

    disp('solving using iterative linearization');
    n = length(q_0);
    Pp = zeros(size(P));
    Pm = zeros(size(P));
    for i = 1:n
        [Pp(:, :, i), Pm(:, :, i)] = matrix_decomposition(P(:, :, i));
    end
    
    x_0 = ones(n,1);
    OPT = q_0'*x_0;
    converged = 0;
    
    TIME = cputime;
    ITER = 0;
    while ~converged
        ITER = ITER + 1;
        constraint = zeros(n,1);
        for i = 1:n
            constraint(i) = max(0, x_0'*Pp(:,:,i)'*x_0 + q(:,i)'*x_0 + r(i) - x_0'*Pm(:, :, i)*x_0);
        end
        cvx_begin quiet
            variable x(n);
            minimize(q_0'*x)
            subject to
                x <= 1;
                x >= 0;
                for i = 1:n
                    x'*Pp(:,:,i)*x + q(:,i)'*x + r(i) <= x_0'*Pm(:, :, i)*x_0+2*x_0'*Pm(:, :, i)*(x-x_0) + constraint(i);
                end
         cvx_end
         
         if OPT-cvx_optval < tol
             converged = 1;
         end
         OPT = cvx_optval;
         ARG = x;
         x_0 = x; 
    end
    TIME = cputime - TIME;
    ITER = ITER - 1;
end