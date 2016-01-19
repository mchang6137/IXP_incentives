function index = argmax_diff(x, ...
                             X, ...
                             tol, ...
                             exclude)

	n = length(x);
    max_diff = 0;
    index = 0;
    for i = 1:n
        for j = 1:n
            test_diff = abs(X(i,j)-x(i)*x(j));
            if test_diff > max(tol, max_diff)
                if x(i) > x(j) && ~exclude(i)
                    max_diff = test_diff;
                    index = i;
                elseif ~ exclude(j)
                    max_diff = test_diff;
                    index = j;
                end
            end
        end
    end
end