## 1）a) Use forward Euler method to solve the following problem

$$
y'=-5y, \quad y(0)=1.
$$
# Solve the problem for $t\in[0, 10]$ with $h=0.4$, $h=0.41$, $h=0.1$.

Take $y'=f(t,y)$.
Solve exact function,

$$
\begin{aligned}
y' &=-5y \\
\frac{y'}{y}&=-5 \\
\ln y &=-5t+c \Rightarrow \quad y=Ce^{-5t}. \\
\end{aligned}
$$

By $y(0)=1$, which implies that $y=e^{-5t}$.
By forward Euler method, we have $u_{n+1}=u_{n}+hf(t_{n},{u_{n}})$, where $t_{n}=t_{0}+nh$. By using $t_{0}=0$, then

$$
u_{n+1}=u_{n}+h(-5u_{n})=(1-5h)u_{n}.
$$

Result：
![[fe_vs_true_h0_1 1.csv]] # b) Use backward Euler method to solve the following problem
$$
y' = -5 y, \quad y(0)=1.
$$


___
## 2) Consider solving the following problem using forward Euler Method

$$
y' = y(1-y), \quad y(0)=y_0, \quad 0<y_0<1.
$$

Find the range of h such that the solution is qualitatively correct.

