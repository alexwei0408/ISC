Problem description
Consider approximating $f(x)=1/(1+25x^{2}),x\in [-1,1].$ Let N+1 be the number of nodes.Using cubic spline interpolation, find 𝑁 such that the error of approximation is less than $10^{-10}$

1.Error formula
For a uniform grid and natural cubic spline interpolation, The error bound is:

$$
\|f - S\|_\infty \le \frac{5}{384} \, h^4 \max_{x \in [a,b]} \big| f^{(4)}(x) \big|
$$
