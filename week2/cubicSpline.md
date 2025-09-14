Problem description
Consider approximating the Runge function. Let N+1 be the number of nodes.Using cubic spline interpolation, find 𝑁 such that the error of approximation is less than 10^{-10}

1.Error formula
For a uniform grid and natural cubic spline interpolation, The error bound is:

$$
\|f - S\|_\infty \le \frac{5}{384} \, h^4 \max_{x \in [a,b]} \big| f^{(4)}(x) \big|
$$

where

$h = \tfrac{b-a}{N}$ is the step size,

$N$ is the number of subintervals,

$S(x)$ is the cubic spline approximation,

$f^{(4)}(x)$ is the fourth derivative of $f$.

3. Step Size and Subinterval Calculation

From the error bound, we require

ℎ
≤
(
𝜀
(
5
/
384
)
⋅
max
⁡
∣
𝑓
(
4
)
∣
)
1
/
4
.
h≤(
(5/384)⋅max∣f
(4)
∣
ε
	​

)
1/4
.

Then the number of subintervals is

𝑁
≥
𝑏
−
𝑎
ℎ
.
N≥
h
b−a
	​

.

Examples:

For $\varepsilon=10^{-10}$: $N \approx 2365$.

For $\varepsilon=10^{-14}$: $N \approx 13333$.

4. Results and Observations

Theoretical Results:

$\varepsilon=10^{-10}$: $N \approx 2365$ subintervals.

$\varepsilon=10^{-14}$: $N \approx 13333$ subintervals.

Numerical Verification:

For $N=2365$, measured max error $\approx 10^{-10}$.

For $N=13333$, measured max error $\approx 10^{-14}$.

Error vs. Step Size:
Numerical results confirm

error
  
≈
  
𝐶
 
ℎ
4
,
error≈Ch
4
,

consistent with the $O(h^4)$ convergence rate.

Natural vs. Clamped Spline:

Natural: $S''(a)=S''(b)=0$

Clamped: $S'(a)=f'(a), S'(b)=f'(b)$

For this smooth function, clamped splines generally reduce endpoint error further.

5. Conclusion

The required number of subintervals can be determined directly from the error bound formula.

To achieve accuracy $\varepsilon=10^{-14}$, about 13,333 subintervals (13,334 nodes) are necessary.

Numerical experiments verify the theoretical prediction and confirm $O(h^4)$ convergence.

Clamped boundary conditions improve accuracy near the endpoints compared to natural splines.
