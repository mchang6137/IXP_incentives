p = [4234; 1603; 9; 5; 1; 28; 1; 1; 59; 17; 9; 1; ...
     81; 288; 1607; 2; 1; 13; 139; 90; 78; 164; 35];
n = length(p);
Z = (1.1-1)/(1-.05);
C = log(p)+1;
W = zeros(n);
for i = 1:n
    for j = 1:n
        W(i,j) = p(i) * (p(i)~=p(j)) / (sum(p(1:j)+sum(p(j+1:n))));
    end
end
M = .95*max(W, W');
E = eye(length(p));
P = zeros(n, n, n);
q = zeros(n);
for i = 1:n
    P(:,:,i) = Z*E(:,i)*M(:,i)';
    q(:,i) = -Z*M(:,i) - C(i)*E(:,i);
end
cvx_begin sdp
    variable X(n,n) symmetric
    variable x(n)
    minimize(C'*x)
    subject to
    x <= 1;
    x >= 0;
    sum(x) >= 1;
    [[X, x]; [x', 1]] >= semidefinite(n+1);
    for i = 1:n
        trace((P(:,:,i)+P(:,:,i)')'*X) + 2*q(:,i)'*x + 2*C(i) <= 0;
    end
cvx_end