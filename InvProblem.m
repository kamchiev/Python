function [lambda_p,w,m] = InvProblem(A,p,z,m_max)

w = z/norm(z);
lambda_p(1) = p;
n=size(A);
[L,U,P] = lu(A-p*eye(n));

for m=1:m_max
    y = L\(P*w);
    z= U\y;
    lambda_p(m+1) = p + 1/(w'*z);
    w=z/(norm(z));

end

