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
u_{n+1}=u_{n}+h(-5u_{n})=(1-5h)u_{n}. -(\star)
$$

Result：  
[h=0.4](https://github.com/alexwei0408/ISC/blob/main/Week_5/result/fe_vs_true_h0_4.csv)  
[h=0.41](https://github.com/alexwei0408/ISC/blob/main/Week_5/result/fe_vs_true_h0_41.csv)  
[h=0.1](https://github.com/alexwei0408/ISC/blob/main/Week_5/result/fe_vs_true_h0_1.csv)  
<img width="900" height="700" alt="iteration_error_three_h" src="https://github.com/user-attachments/assets/75159016-2aeb-46ac-8b53-704d1bdfbf2f" />  
<img width="900" height="700" alt="convergence_Oh_from_h01" src="https://github.com/user-attachments/assets/87fbfd79-a0db-49d1-b9dd-2f250f58f0d9" />  

# Analysis  
Why numerical solution convergence only when $h=0.1$.  
Since by $\star$, we conclude that $u_{n}$ is only depends on h. Thus for $h=0.4$, we can see that numerical solution oscillation on -1 and 1. For $h=0.41$, $|1-5h|=1.05 > 1$, hence the numerical solution divergence.  
For $h=0.1$, numerical solution converges and we have truncation error,

$$
\begin{aligned}
\tau_{n+1}(h) &= \frac{u_{n+1}-u_{n}}{h}-f_{n} \\
&= \frac{u_{n}}{h}(e^{-5h}-1+5h) \\
\end{aligned}
$$

By Taylor series which gives us $\tau_{n+1}=u_{n}(\frac{25h}{2}+O(h^{2}))$. Hnece the global truncation error is $O(h)$.

---
# b) Use backward Euler method to solve the following problem
$$
y' = -5 y, \quad y(0)=1.
$$


___
## 2) Consider solving the following problem using forward Euler Method

$$
y' = y(1-y), \quad y(0)=y_0, \quad 0<y_0<1.
$$

Find the range of h such that the solution is qualitatively correct.

