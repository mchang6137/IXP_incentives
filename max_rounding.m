function [OPT, ARG] = max_rounding(x, ...
                                   A, ...
                                   b)

    n = length(x);
    ARG = zeros(n, 1);
    while ~constraint_SAT(ARG, A, b)
        [~, i] = max(x);
        ARG(i) = 1;
        x(i) = -1;
    end
    [OPT, ARG] = tighten(b'*ARG, ARG, A, b);
    
end 