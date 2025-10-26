## 7) Prove that the gamma function 

$$
\Gamma(z)=\int_{0}^{\infty}e^{-t}t^{z-1} dt, \quad z\in\mathbb{C},\quad Rez>0,
$$

is the solution of the difference equation $\Gamma(z+1)=z\Gamma(z)$.

sol:
Goal: We want to show $\Gamma(z+1)=\int_{0}^{\infty} e^{-t}t^{(z+1)-1}dt=z\int_{0}^{\infty}e^{-t}t^{z-1}dt=z\Gamma(z)$.

By using integration by parts, then we have 

$$
\begin{aligned}
\int_{0}^{\infty} e^{-t}t^{(z+1)-1}dt&=-\lim_{L\to\infty}\int_{0}^{L}t^{z}de^{-t} \\
&=\lim_{L\to\infty}(-e^{-t}t^{z}|_{t=0}^{t=L}+\int_{0}^{L}ze^{t}t^{z-1}dt) \\
&=0+z\Gamma(z).
\end{aligned}
$$

---

## 9) Consider the following family of one-step method depending on the real parameter $\alpha$

$$
u_{n+1}=u_{n}+h\left[ (1-\frac{\alpha}{2}\right)f(x_{n},u_{n})+ \frac{\alpha}{2}f(x_{n+1},u_{n+1})] 
$$

Study their consistency as a function of $\alpha$; then, take $\alpha=1$ and use the corresponding method to solve the Cauchy problem

$$
\begin{cases}
y'(0)=-10y(x), \quad x>0 \\
y(0)=1.
\end{cases}
$$

Determine the values of h in correspondence of which the method is absolutely stable.

sol:

Take $y'(x_{n})=f(x_{n},y_{n})$, then by Taylor expansion, we get 

$$
\begin{aligned}
y(x_{n+1})&=y(x_{n})+hy'(x_{n})+\frac{h^{2}}{2}y''(x_{n})+\cdots \\
&=y(x_{n})+hf(x_{n})+\frac{h^{2}}{2}\frac{d}{dt}f(x_{n})+ O(h^{3}) \\
&=y(x_{n})+hf(x_{n})+\frac{h^{2}}{2}(\partial_{t}f+f\partial_{u}u)(x_{n},u_{n})+O(h^{3})\quad -(\star)
\end{aligned}
$$

Take $u_{n}=y(x_{n}),u_{n+1}=y(x_{n+1})$, then we have 

$$
\begin{aligned}
f(x_{n+1},{u_{n+1}})&=f(x_{n}+h,u_{n}+(u_{n+1}-u_{n})) \\
&=f(x_{n},u_{n})+hf_{x}(x_{n},u_{n})+ (u_{n+1}-u_{n})f_{u}(x_{n},u_{n})+O(h^{2})\\
by (\star) \Rightarrow\quad&=f(x_{n})+hf_{x}(x_{n})+\left[ hf(x_{n})+\frac{h^{2}}{2}(\partial_{t}f+f\partial_{u}u)(x_{n},u_{n})\right]f_{u}+O(h^{3}) \\
&=f+h_{x}+hff_{y}+O(h^{2})
\end{aligned}
$$
