function [OPT, ARG, EXP] = randomized_rounding(x, ...
                                               A, ...
                                               b, ...
                                               T)

    n = length(x);
    ARG = zeros(n, 1);
    OPT = Inf;
    EXP = 0;
    for t = 1:T
        y = zeros(n, 1);
        z = x;
        while ~constraint_SAT(y, A, b)
            z = z / sum(z);
            r = rand;
            d = 0;
            for i = 1:n
                d = d + z(i);
                if r < d
                    y(i) = 1;
                    z(i) = 0;
                    break
                end
            end
        end
        
        f_y = b'*y;
        [f_y, y] = tighten(f_y, y, A, b);
        if f_y < OPT
            OPT = f_y;
            ARG = y;
        end
        EXP = EXP + f_y;
    end
    
    EXP = EXP/T;
end 