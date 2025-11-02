# The AAA Algorithm for Rational Approximation

## 1）Motivation  
We want to approximate a function defined on a set Z $(ex:Z=\left[ -1,1\right])$ by finding a stable and high accuracy rational function.  

---
## 2）Purpose  
Given a function $f(z)$ which is defined on a set $S$, then AAA algorithm will compute a rational function $r(z)$ such that $r(z) \simeq f(z)$. 

---
## 3) Method  
i)Barycentric Rational Representation  
The barycentric formula takes the form of a quotient of two partial fractions. This representation is written as

$$
r(z)=\frac{n(z)}{d(z)}= \frac{\sum_{j=1}^{m}w_{j}f_{j}/(z-z_{j})}{\sum_{j=1}^{m}w_{j}/(z-z_j)}
$$

where $m \ge 1$ is an integer,    
$w_{j}$ are barycentric weights;  
$z_{j}$ is the support points selected from the discrete sample set;  
$f_{j}=f(z_{j})$ are the interpolating value.  

ii)Adaptive greedy selection of support points
The support point $z_{m}$ is chosen as a point $z \in Z^{(m-1)}$ where the nonlinear residual $f(z)-\frac{n(z)}{d(z)}$ at step $m-1$ takes its maximum absolute value. That is, we always select the point with the largest current approximation error (greedy choice).  

Remark: $Z^{(m)}$ is the set of all sample points with the first mm support points removed.

iii) Loewner Matrix and Weighted Least Squares Problem
After the point $z_{m}$ is selected, and we can compute the weights $w_{1},w_{2},\dots,w_{m}$ by solving a weighted least-squares problem over the the sample points. 

Hence by the residual form 

$$
\sum_{j=1}^{m}\frac{w_{j}F_{i}^{(m)}}{Z_{i}^{(m)}-z_{j}}-\sum_{j=1}^{m}\frac{w_{j}f_{j}}{Z^{(m)}_{i}-z_{j}}=\sum_{j=1}^{m}w_{j}(\frac{F_{i}^{(m)}-f_{j}}{Z_{i}^{(m)}-z_{j}}) -(\star)
$$

Remark  
- The first sum $\sum_{j=1}^{m}\frac{w_{j}F_{i}^{(m)}}{Z_{i}^{(m)}-z_{j}}$ represents the numerator $n(Z_i^{(m)})$ evaluated at the unused sample points.
- The second sum $\sum_{j=1}^{m}\frac{w_{j}f_{j}}{Z_{i}^{(m)}-z_{j}}$ represents the weighted numerator using function values at support points.
-  Their difference calls the linearized residual, and minimizing this residual ensures optimal weight selection for the rational approximation $r(z)=\frac{n(z)}{d(z)}$

Note that: $Z^{(m)}=(Z_{1}^{(m)},\dots,Z_{M-m}^{(m)})^{T}$; $F^{(m)}=f(Z^{(m)})$. 

We want the residual $(\star)$ close to zero at all $M-m$ sample points. \
That is the optimization problem can be written as 

$$
\left\|A^{(m)}w\right\|_{M-m}, \quad \left\| w\right\|_{m}=1
$$ 

where $w=(w_{1},w_{2},\dots,w^{m})^{T}$ is the barycentric weights and $A^{(m)}$ is the $(M-m)\times m$ is called Loewner matrix and can be written as

$$
A^{(m)}=
\begin{pmatrix}
\frac{F_{1}^{(m)}-f_{1}}{Z_{1}^{(m)}-z_{1}} \quad&\cdots \quad &\frac{F_{1}^{(m)}-f_{m}}{Z_{1}^{(m)}-z_{m}} \\
\vdots &\ddots & \vdots \\
\frac{F_{M-m}^{(m)}-f_{1}}{Z_{M-m}^{(m)}-z_{1}} &\cdots &\frac{F_{M-m}^{(m)}-f_{m}}{Z_{M-m}^{(m)}-z_{m}}
\end{pmatrix}
$$

iv) SVD for weight computation  
First, we want to construct a Cauchy matrix $C$ 

$$
C=
\begin{pmatrix}
\frac{1}{Z_{1}^{(m)}-z_{1}} &\cdots &\frac{1}{Z_{1}^{(m)}-z_{m}} \\
\vdots &\ddots & \vdots \\
\frac{1}{Z_{M-m}^{(m)}-z_{1}} &\cdots &\frac{1}{Z_{M-m}^{(m)}-z_{m}}
\end{pmatrix}
$$

Define diagonal left and right scaling matrices by $S_{F}=diag(F_{1}^{(m)},\dots,F_{M−m}^{(m)}),S_{f}=diag(f_{1},\dots,f_{m})$. Then we can construct 

$$
A^{(m)}=S_{F}C-CS_{f}
$$

Second, write $A^{(m)}=U\sum V^{\star}$. Take barycentric weight vector w, and so we can compute $(M-m)$ vectors N and D with $N=C(wf)$, $D=Cw$.  
Remark: The minimum singular value is not unique, we just need to find a w such that $\left\|A^{m}w\right\|_{M-m}$ is minimum.  

Third, we take w as the right singular vector corresponding to the smallest singular value. This ensures $||A^{(m)}w||$ is minimized subject to $\left\| w\right\|_{m}=1$.  
Finally, the rational approximation at the unused points is computed as $r(Z^{(m)})=\frac{N}{D}=\frac{C(wf)}{Cw}$.

v) Convergence criterion  
AAA-algorithm breaks when 

$$
\max_{z\in Z^{(m)}}\left| f(z)-r(z)\right| \le tol \cdot \max_{z\in Z} \left| f(z)\right|
$$

where tol is a default tolerance $(10^{-13})$, if not satisfied, the algorithm will returns to step ii) to select the next support points.

---
## 4) Pseudocode
```
pseudocode
Input:
  F   = function or data vector, sampled at points Z (|Z| = M)
  Z   = complex or real sample points
  tol = desired relative tolerance (default 1e-13)
  mmax= maximum number of support points (default 100)

Output:
  r      = rational approximation (in barycentric form)
  poles  = vector of poles
  zeros  = vector of zeros
  z, f, w= support points, function values at support points, barycentric weights

Algorithm:
  Initialize:
    J = {1,2,...,M}             // unused indices
    z = []                      // support points
    f = []                      // function values at support points
    C = []                      // Cauchy matrix columns
    errvec = []                 // errors at each iteration
    R = mean(F)                 // initial approximation
    
  For m = 1 to mmax:
    1. Select next support point (greedy):
       Find j in J such that |F(J) - R(J)| is maximized
       Append Z(j) to z, F(j) to f
       Remove j from J
    
    2. Build Cauchy matrix:
       Append new column: 1 / (Z(J) - Z(j)) // Only use unused points
    
    3. Build Loewner matrix:
       SF = diag(F(J))
       Sf = diag(f)
       A = SF * C - C * Sf      // (M-m) x m matrix
    
    4. Solve for weights using SVD:
       Compute the smallest singular vector w of A
       
    5. Form rational approximant:
       Numerator N = C * (w .* f)
       Denominator D = C * w
       R(J) = N(J) ./ D(J)
    
    6. Evaluate error:
       err = max(|F - R|)
       Append err to errvec
    
    7. Check convergence:
       If err ≤ tol * max(|F|), terminate loop

  EndFor

  // Postprocess: compute poles, zeros, optionally remove Froissart doublets if needed

Return r, poles, zeros, z, f, w, errvec

```

## 5) Example
We try to approximate a Runge function $f(x)=\frac{1}{1+25x^{2}}$, for $x \in \left[ -1,1\right]$, by using i) Taylor series; ii) AAA algorithm, and compare the absolute error among of them.  

Here is the result of the approximation
<img width="900" height="506" alt="{EEC5BD54-C652-4018-AF50-D9ED65BB086E}" src="https://github.com/user-attachments/assets/76728eec-843b-4b7c-b38d-9ee833ad56f2" />
<img width="900" height="298" alt="{8003363A-6ED8-483F-9089-6C4356F00BF4}" src="https://github.com/user-attachments/assets/e676c69d-5d5d-4bf1-bd34-aa5e3175aaa0" />  

From the result, we can conclude that, 
- We approximate the runge function by using Taylor series will fail. This is becasue the runge function has complex poles at $z = \pm \frac{1}{5}i$, and so there have radius of convergence $|z|<\frac{1}{5}$. When the point z is outside this radius, Taylor series will diverge exponentially.  
- Approximate Runge function by using AAA-algorithm, it will give a nice approximate and also just use only 3 support points. For the whole domain, it still can be work.  

[Here is sample code for the result.](https://github.com/alexwei0408/ISC/blob/main/Midterm%20report/aaa.py)

---

## 6) Conclusion
The AAA-algorithm is a fully automatic method for rational function approximation that combines three key innovations: barycentric representation, greedy support point selection, and SVD-based weight computation.
