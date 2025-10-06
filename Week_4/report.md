
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
Take a partition $P=\left\{ 0=x_{0} < x_{1}< \cdots < x_{n-1}< x_{n} =1 \right\}$
Formula: $I_{n}(f) \simeq h(\frac{1}{2}f(0)+f(x_{1})+\cdots+f(x_{n-1})+\frac{1}{2}f(1))\text{, where h}=\frac{1}{n}.$  
Calculate the number of n.

$$
\begin{aligned}
|E_{n}| &\le \frac{1}{12}h^{2}\max_{[0,1]}|f''(t)| \\
\Rightarrow n^{2}&\ge \frac{\max_{[0,1]}|f''(t)|}{12|E_{n}|}\simeq 216544\\
\end{aligned}.
$$
Result:
![[{D012FB4A-548C-4934-992E-829642AFC127}.png]]

#Remark: Why we don't use $f(x)=\frac{1}{1+25x^{2}}.$ By the error formula of trapezoidal rule

$$
\begin{align}
E(f) &\le \frac{b-a}{12}h^{2} \max_{[a,b]} |f''| \\
&= \lim_{L \to \infty} \frac{L}{12}h^{2} \cdot50 \\
&=\frac{25L^{3}}{6n^{2}}
\end{align}
$$
From the error formula , we can see that L become larger, n is also.(ex: if $L=4x10^{8},n=2.3x10^{18}$ )
2.

$$
\int_{0}^{1}\frac{ln(x)}{1+25x^{2}}dx
$$
First, we use integration by part to vanish singularity pole.

$$
\begin{aligned}
\int_{0}^{1}\frac{\ln(x)}{1+25x^{2}}dx 
&= \ln(x)(\frac{\arctan(5x)}{5})|_{0}^{1} -\int_{0}^{1}\frac{\arctan(5x)}{5}d\ln(x) \\
&=0- \frac{1}{5} \lim_{a \to 0} \int_{a}^{1} \frac{\arctan(5x)}{x}dx \\
\end{aligned}
$$
Thus, we want to approximate $f(x)= \frac{\arctan(5x)}{x}.$ Cleary $f(0)=-1$
Method:
