## 1）Prove that Heun's method has order 2 with respect to h.

$$
E_{1}=\int_{t_{n}}^{t_{n+1}}f(s,y(s))ds-\frac{h}{2}(f(t_{n},y_{n})+f(t_{n+1},y_{n+1}))
$$

and

$$
E_{2}= \frac{h}{2}(f(t_{n+1},y_{n+1})-f(t_{n+1},y_{n}+hf(t_{n},y_{n}))),
$$

where $E_{1}$ is the error due to numerical integration with the trapezoidal method and $E_{2}$ can be bounded by the error due to using forward Euler method. 

sol  
Let $g(t)=f(t,y(t))$. Then, the exact solution satisfies the integral form $y(t_{n+1}) = y(t_{n}) + \int_{t_{n}}^{t_n+1} g(\tau)d\tau.-(1)$  
Moreover, Heun's method can write in the form

$$
u_{n+1}=u_{n}+ \frac{h}{2}(g_{n}+\hat{g_{n}}), \text{where } \hat{g_{n}}=f(t_{n+1},u_{n}+hf(t_{n},u_{n}))-(2). 
$$

From $(1)-(2)$, we get

$$
\begin{aligned}
y(t_{n+1})-u_{n+1} &=(y(t_{n})-u_{n})+(\int_{t_{n}}^{t_n+1}g(\tau)\,d\tau-\frac{h}{2}(g_{n}+\hat{g_{n}})) \\
&=(\int_{t_{n}}^{t_{n+1}}g(\tau)\,d\tau-\frac{h}{2}(g_{n}+g_{n+1}))+\frac{h}{2}(g_{n+1}-\hat{g_{n}}) \\
&= E_{1}+E_{2}
\end{aligned}
$$

i)By the chain rule, 

$$
\begin{aligned}
g'(t)&=\frac{d}{dt}(f(t,y(t)))=f_{t}(t,y(t))+f_{y}(t,y(t))y'(t)=f_{t}+f_{y}f \\
g''&=\frac{d}{dt}(f_{t}+f_{y}f),
\end{aligned}
$$

we get g'' exists and bounded if $f \in C^{2}$. Then $g \in C^{2}$, and so the trapezoid error satisfy $E_{1}=-\frac{h^{3}}{12}g''(\xi_{n})$, for some $\xi \in (t_{n},t_{n+1})$. Therefore, $E_{1}=O(h^{3})$. 

ii) By Lipschitz continuity of f in y with constant L,

$$
|E_{2}|=\frac{h}{2}|f(t_{n+1},y(t_{n+1}))-f(t_{n+1},u_{n}+hf(t_{n},u_{n}))| 
\le \frac{h}{2}L|y(t_{n+1})-(u_{n}+hf(t_{n},u_{n}))|
$$

By Taylor expansion, we get

$$
\begin{aligned}
y(t_{n+1})&=y_{n}+hy'_{n}+\frac{h^{2}}{2}y''_{n}+O(h^{3}) \\
&= u_{n}+hf_{n}+\frac{h^{2}}{2}y''_{n}+O(h^{3})
\end{aligned}
$$

Hence $|y(t_{n+1})-(u_{n}+hf_{n})|=O(h^{2})$. Thus, $|E_{2} \le \frac{h}{2}LO(h^{2})|=O(h^{2})$ .
Therefore, we conclude that the local truncation error of Heun's method is $O(h^{3})$, which implies that the global error after $O(\frac{1}{h})$ is $O(h^{2})$, and so Heun's method has order 2.

---

## 2) Prove that the Crank-Nicolson(or trapezoidal) method has order 2 with respect to h.

sol
By Crank-Nicolson method, we have $u_{n+1}=u_{n}+\frac{h}{2}(f(t_{n},u_{n})+f(t_{n+1},u_{n+1}))$. 
By $y'=f(t,y(t))$, the exact solution can be written as $y(t_{n+1})=y(t_{n})+\int_{t_{n}}^{t_{n+1}}f(\tau,y(\tau))\,d\tau$ . By trapezoidal rule, we get

$$
\int_{t_{n}}^{t_{n+1}}f(\tau,y(\tau))d\tau=\frac{h}{2}(f_{n}+f_{n+1}) - \frac{h^{3}}{12}f''(\xi_{n},y(\xi_{n})),\text{ for some suitable } \xi_{n} \in (t_{n},t_{n+1}).
$$

By taking $y_{n}=u_{n}$

$$
\frac{y_{n+1}-y_{n}}{h}= \frac{1}{2}(f(t_{n},u_{n})+f(t_{n+1},u_{n+1}))- \frac{h^{2}}{12}f''(\xi_{n},y(\xi_{n}))
$$

Hence, the truncation error is $y(t_{n+1})-u_{n+1}=O(h^{3})$, which implies that the global error is $O(h^{2})$, and so Crank-Nicolson is a 2nd-order method with respect to h.
