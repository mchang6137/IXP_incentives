function [OPT, ARG, TIME] = brute_force(p, ...
                                        A, ...
                                        b)

    disp('solving using brute force');
    n = length(p);
    OPT = Inf;
    TIME = cputime;
    
    x = zeros(n, 1);
    for i = 1:2^n-1
%         if floor(log2(i)) == log2(i)
%             disp(i);
%         end
        binary = de2bi(i);
        x(1:length(binary)) = binary;
        if constraint_SAT(x, A, b)
            TEST_OPT = b'*x;
            if TEST_OPT < OPT
                OPT = TEST_OPT;
                ARG = x;
            end
        end
    end
    TIME = cputime - TIME;
end