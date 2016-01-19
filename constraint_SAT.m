function SAT = constraint_SAT(x, ...
                              A, ...
                              b)
    
    SAT = 1;
    for i = 1:length(x)
        if ~x(i)
            if A(i, :)*x - b(i) < 0
                SAT = 0;
                break;
            end
        end
    end
    
end