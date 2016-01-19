function [OPT, ARG] = tighten(OPT, ...
                              ARG, ...
                              A, ...
                              b)

	n = length(ARG);
	while 1
        max_diff = 0;
        index = 0;
        for i = 1:n
            if ARG(i)
                y = ARG;
                y(i) = 0;
                if constraint_SAT(y, A, b) && OPT - b'*y > max_diff
                    max_diff = OPT - b'*y;
                    index = i;
                    OPT = b'*y;
                end
            end
        end
        if index
            ARG(index) = 0;
        else
            break
        end
    end
end