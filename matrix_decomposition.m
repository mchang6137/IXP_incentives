function [Pp, Pm] = matrix_decomposition(M)

    [V, L] = eig(M);
    Pp = V*(L.*(L>0))*inv(V);
    Pm = -V*(L.*(L<0))*inv(V);
    
end