function [OPT, ARG, TIME, ITER] = simulated_annealing(A, ...
                                                      b, ...
                                                      T)
    
	disp('solving using simulated annealing');
    n = length(b);
    x = ones(n,1);
    f_x = b'*x;
    ARG = x;
    OPT = b'*ARG;
    
    TIME = cputime;
    iter = 0;
    for i = 1:T
        iter = iter + 1;
        x_prop = x;
        for j = 1:n
            if rand < .5/(log10(i)+1);
                x_prop(j) = 1-x_prop(j);
            end
        end
        if constraint_SAT(x_prop, A, b)
            [f_prop, x_prop] = tighten(b'*x_prop, x_prop, A, b);
            disp(strcat(num2str(f_prop), ',', num2str(OPT)));
            if f_prop < OPT
                ITER = iter;
                ARG = x_prop;
                OPT = f_prop;
                x = x_prop;
                f_x = f_prop;
            elseif rand < f_x/f_prop
                x = x_prop;
                f_x = f_prop;
            end
        end
    end
    TIME = cputime - TIME;
end