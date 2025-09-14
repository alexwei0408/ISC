Problem description  
1）Consider approximating $f(x)=1/(1+25x^{2}),x\in [-1,1].$ Let N+1 be the number of nodes.Using cubic spline interpolation, find 𝑁 such that the error of approximation is less than $10^{-10}$

i.Error formula  
For a uniform grid and natural cubic spline interpolation, The error bound is:

$$
\|f - S\|_\infty \le \frac{5}{384} \, h^4 \max_{x \in [a,b]} \big| f^{(4)}(x) \big|
$$  

ii.Observertion  
For N=2365, measured max error $\simeq 10^{-10}$.  
For N=23644, measure max error $\simeq 10^{-14}.$  


a)Natural spline: The boundary condition is $S{''}(-1)=S{''}(1)=0.$ For the Runge function, this does not match the true curvature at the endpoints, so the spline accumulates error near the boundaries.  

b)Clamped spline: The boundary condition uses the exact first derivatives $f^{'}(-1),f'(1).$ This enforces the correct slope at the endpoints and allows the spline to capture the function’s behavior more accurately. As $N$ increases, the advantage of using the correct derivative information becomes more pronounced

Problem description  
2）Using Chebyshev nodes, find $𝑁$ such that the error of approximation is less than $10^{-10}$  

i)Use Chebyshev polynomials of the second kind, we have $x_{k}=cos(\frac{k\displaystyle \pi }{n}),k=0,1,2,...,n$  
ii)Minimal number of nodes N=121, measure max error $\simeq 10^{-10}$.  


Code is designed by Chatgpt  
[cubic spline interpolation](https://github.com/alexwei0408/ISC/blob/main/week2/cubicSpline.py)  
[Chebyshev node of second kind](https://github.com/alexwei0408/ISC/blob/main/week2/Chebysehv.py)
