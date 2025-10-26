
Approximate the integral such that the error of approximation is less than $10^{-10}$.  
1.

$$
\int_{0}^{\infty} \frac{1}{1+25x^{2}}dx
$$

In calculus I, we have learned how to solve this improper integral.

$$
\begin{align}
\int_{0}^{\infty} \frac{1}{1+25x^{2}}dx &=\lim_{L\to\infty}\int_{0}^{L} \frac{1}{1+25x^{2}}dx \\
&=\frac{1}{5} \lim_{L\to\infty}\int_{0}^{L} \frac{1}{1+u^{2}}du\\
&=\frac{1}{5}\lim_{L\to\infty}\arctan(u)|_{0}^{L}\\
&=\frac{\pi}{10}\simeq0.31415926535.
\end{align}
$$

Now, we want to use Trapezoidal Rule to approximate this value.

Let $x=\frac{t}{1-t}, t\in[0,1), dx=\frac{1}{(1-t)^{2}dt}.$ Then $f(t)=\frac{1}{(1-t)^{2}+25t^{2}}.$  
Take a partition $P = \{ 0 = x_{0} \lt x_{1} \lt \cdots \lt x_{n-1} \lt x_{n} = 1 \}$.   
Formula: $I_{n}(f) \simeq h(\frac{1}{2}f(0)+f(x_{1})+\cdots+f(x_{n-1})+\frac{1}{2}f(1))\text{, where h}=\frac{1}{N-1}.$  


Result:  
<img width="831" height="218" alt="{EE90E235-8151-4262-A7BE-8014400C3064}" src="https://github.com/user-attachments/assets/d29f6740-fdff-4ae3-b7d0-bc85584f1007" />  
<img width="802" height="609" alt="{95BE0506-B496-4F10-8926-855CA1F64302}" src="https://github.com/user-attachments/assets/be515db7-c167-4e01-9dfb-49bdcbc6c2fa" />

# Remark: Why we don't use $f(x)=\frac{1}{1+25x^{2}}.$

By the error formula of trapezoidal rule

$$
\begin{align}
E(f) &\le \frac{b-a}{12}h^{2} \max_{[a,b]} |f''| \\
&= \lim_{L \to \infty} \frac{L}{12}h^{2} \cdot50 \\
&=\frac{25L^{3}}{6n^{2}}
\end{align}
$$

From the error formula , we can see that L become larger, n is also.(ex: if $L=4x10^{8},n=2.3x10^{18}$ )  

---

2.

$$
\int_{0}^{1}\frac{ln(x)}{1+25x^{2}}dx
$$

First, we use integration by part to vanish singularity pole.

$$
\begin{aligned}
I=\int_{0}^{1}\frac{\ln(x)}{1+25x^{2}}dx 
&= \ln(x)(\frac{\arctan(5x)}{5})|_{0}^{1} -\int_{0}^{1}\frac{\arctan(5x)}{5}d\ln(x) \\
&=0- \frac{1}{5} \lim_{a \to 0} \int_{a}^{1} \frac{\arctan(5x)}{x}dx \\
\end{aligned}
$$

Then, we define a smooth function $f(x)= \frac{\arctan(5x)}{5x},$ with $f(0)=\lim_{x \to 0} \frac{\arctan(5x)}{5x}=1$. So that $I=-\int_{0}^{1}f(x)dx$.  
Let N be the number of nodes with step size $h=\frac{1}{N-1}$ and $x_{i}=ih$, for $i=1,2,3,\cdots$. Then we use composite trapezoidal rule to approximate.  

```
pseudocode of composite trapezoidal rule
h = 1/(N-1)
sum = 0.5*phi(0) + 0.5*phi(1)
for i = 1 .. N-2:
    sum += phi(i*h)
I_h = - h * sum
```


Result:  
<img width="900" height="257" alt="{234F7469-2F1E-40AD-9853-C629F3A17CEC}" src="https://github.com/user-attachments/assets/c0fd4bb2-b24c-4b0e-9fcf-3f51b091d771" />  
<img width="900" height="827" alt="{4635E61D-448D-44B9-8A7D-0E8F814A1CCC}" src="https://github.com/user-attachments/assets/a65defc1-e469-4ab9-9ea3-8646aff0f190" />

---

Conclusion： Both problem1 and problem2 use trapezoidal rule to approximate function give $O(h^{2})$.

