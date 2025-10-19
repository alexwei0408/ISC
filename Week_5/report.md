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
Since by $\star$, we conclude that $u_{n}$ is only depends on |1-5h|. Thus for $h=0.4$, $|1-5h|=1$, and so we can see that numerical solution oscillation on -1 and 1. For $h=0.41$, $|1-5h|=1.05 > 1$, hence the numerical solution divergence.  
For $h=0.1$, $|1-5h|<1$, the numerical solution converges and we have local truncation error,

$$
\tau_{n+1}=\frac{1}{h}(u(t_{n+1})-u(t_{n})-h(f(t_{n},u(t_{n})))=\mathbb{O}(h).
$$

Therefore, the global error satiefies $E(h)= \mathbb{O}(h)$, which is confirmed by the log–log convergence plot.

# b) Use backward Euler method to solve the following problem
$$
y' = -5 y, \quad y(0)=1.
$$

By backward Euler method, 

$$
\begin{aligned}
u_{n+1} &= u_{n}+hf_{n+1} \\
&=u_{n}+h(-5u_{n+1}) \Rightarrow u_{n+1}=\frac{u_{n}}{1+5h}
\end{aligned}
$$

Result:  
[h=0.1](https://github.com/alexwei0408/ISC/blob/main/Week_5/result/be_vs_true_h0_1.csv);  
[h=.4](https://github.com/alexwei0408/ISC/blob/main/Week_5/result/be_vs_true_h0_4.csv);  
[h=0.41](https://github.com/alexwei0408/ISC/blob/main/Week_5/result/be_vs_true_h0_41.csv);  
<img width="900" height="680" alt="iteration_error_BE" src="https://github.com/user-attachments/assets/7a5004be-d88a-4b32-ae5e-f66fbbaadae5" />  
<img width="900" height="680" alt="convergence_Oh_BE" src="https://github.com/user-attachments/assets/528e1d9a-e3ac-4df9-8704-e20af76f5b9e" />  

Analysis:  
Each iteration step depends on $(1+5h)^{-n}$, and $1+5h >1$. Therefore, numerical solution is convengent.

Conclusion: Forward Euler suffers from a strict stability condition $0<h<0.4$. When $h=0.41$, the numerical solution divergent.  
However, backward Euler method give a stable amplification factor $G(h)=\frac{1}{1+5h} <1$, for each steps. 
___
## 2) Consider solving the following problem using forward Euler Method

$$
y' = y(1-y), \quad y(0)=y_{0}, \quad 0 <y_{0} <1.
$$

Find the range of h such that the solution is qualitatively correct.

By using forward Euler method, we have $u_{n+1}=u_{n}+hf(t_{n},u_{n})=u_{n}+hu_{n}(1-u_{n})$. Since the solution is qualitatively correct which implies that 

$$
0 < u_{j} < 1, \text{ for any j}=0,1,\cdots
$$

Then, $u_{n+1}=u_{n}(1+h-hu_{n})$

