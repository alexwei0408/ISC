# 1.Given the following set of data 

$$
\{ f_{0}=f(-1)=1,f_{1}=f'(-1)=1,f_{2}=f'(1)=2,f_{3}=f(2)=1\}
$$
## prove that the Hermite-Birkoff interpolating polynomial $H_{3}$ does not exist for them.

sol
Let $H_{3}(x)=a_{3}x^{3}+a_{2}x^{2}+a_{1}x+a_{0}$. Then $H'_{3}(x)=3a_{3}x^{2}+2a_{2}x+a_{1}$.  
Therefore,

$$
\left\{
\begin{aligned}
a_{0} &= 1 \\
-b_{2} + a_{2} &= -\tfrac{1}{2} \\
b_{2} + 2a_{4} &= -\tfrac{1}{12} \\
b_{2} &= -\tfrac{1}{30}
\end{aligned}
\right.
$$

From $(4)-(1)$, then we get  a linear system, that is

$$
B\overrightarrow{a}=
\begin{pmatrix}
3&1&1 \\
3&-2&1\\
3&2&1\\
\end{pmatrix}
\begin{pmatrix}
a_{3}\\
a_{2}\\
a_{1}
\end{pmatrix}
=
\begin{pmatrix}
0\\
1\\
2\\
\end{pmatrix}.
$$

By reduce row echelon form , we get

$$
\begin{bmatrix}
3&1&1 |0\\
3&-2&1|1\\
3&2&1|2\\
\end{bmatrix}
\xrightarrow{R_{3}-R_{1},R_{2}-R_{1}}
\begin{bmatrix}
3&1&1|0\\
0&-3&0|1\\
0&1&0|2\\
\end{bmatrix},
$$

which implies that $a_{2}=2,-\frac{1}{3}$. Therefore $H_{3}$ does not exist.

---

# 2. Let $f(x)=\cos(x)=1-\frac{x^{2}}{2!}+\frac{x^{4}}{4!}-\frac{x^{6}}{6!}+\cdots$; then, consider the following rational approximation

$$
r(x)=\frac{a_{0}+a_{2}x^{2}+a_{4}x^{4}}{1+b_{2}x^{2}}
$$

## call the Pade approximation. Determine the coefficient of r in such a way that 

$$
f(x)-r(x)=\gamma_{8}x^{8}+\gamma_{10}x^{10}+\cdots
$$

sol

$$
\begin{aligned}
&f(x)(1+b_{2}x^{2})-(a_{0}+a_{2}x^{2}+a_{4}x^{4})&=O(x^{8}) \\
&(1-\frac{x^{2}}{2!}+\frac{x^{4}}{4!}-\frac{x^{6}}{6!}+\cdots)(1+b_{2}x^{2})-(a_{0}+a_{2}x^{2}+a_{4}x^{4})&=O(x^{8}) \\
&1+(b_{2}-\frac{1}{2})x^{2}+(-\frac{b_{2}}{2}+\frac{1}{24})x^{4}+(\frac{b_{2}}{24}-\frac{1}{720})x^{6}-(a_{0}+a_{2}x^{2}+a_{4}x^{4})&=O(x^{8}) \\
\end{aligned}
$$

Therefore, we have

$$
\left\{
\begin{aligned}
a_{0}&=1 \\
-b_{2}+a_{2}&=-\frac{1}{2} \\
b_{2}+2a_{4}&=\frac{1}{12} \\
b_{2}=\frac{1}{30}
\end{aligned}
\right .
$$

Hence, we conclude that $a_{0}=1,a_{2}=-\frac{7}{15},a_{4}=\frac{1}{40},b_{2}=\frac{1}{30}$.

