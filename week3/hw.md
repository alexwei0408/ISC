---
## 1. Let $E_{0}\left(f\right)$ and $E_{1}\left(f\right)$ be the quadrature errors in $\left(9.6\right)$ </span> and $\left(9.12\right)$. Prove that $\left| E_{1}\left(f\right) \right|\simeq 2\left| E_{0}\left(f\right) \right|$.
---
$$
(9.6)E_{0}(f)=\frac{h^{3}}{3}f^{''}(\xi),h=\frac{b-a}{2};
(9.12)E_{1}(f)=-\frac{h^{3}}{12}f^{''}(\xi), h=b-a
$$  

Define $h^{'}=\frac{b-a}{2}=\frac{h}{2}$.Then $E_{0}(f)=\frac{h'^{3}}{3}f^{''}(\xi)= \frac{(b-a)^{3}}{24}f^{''}(\xi)=\frac{h^{3}}{24} f^{''}(\xi)$.  
Therefore, $|E_{1}(f)|\simeq2 |(\frac{h^{3}}{24})f^{''}(\xi)|=2|E_{0}(f)|$.  

---
## 3. Let $I_{n}\left(f\right)=\sum_{k=0}^{n}\alpha_{k}f\left(x_{k}\right)$ be a Lagrange quadrature formula on n+1 nodes. Compute the degree of exactness r  of the formula.  
a) $I_{2}\left( f \right)=\left( \frac{2}{3} \right)\left( 2f\left( -\frac{1}{2} \right) -f(0)+2f(\frac{1}{2})\right)$ ,  
b) $I_{4}\left( f \right)=\left( \frac{1}{4} \right)\left(f(-1)+3f\left( -\frac{1}{3} \right) +3f(\frac{1}{3})+2f(1)\right)$.  
---
a)Define $Q(f)=\int_{-1}^{1}x^{m}dx$, for $m \in\mathbb{N}$, such that $Q(f)-I_{n}(f)\simeq \mathcal{O}(h^{p})$.
Node that both $Q(f), I_{2}$ and $I_{4}$ are symmertric. Then, $Q(f)=I_{2}=I_{4}=0$, for all $m=1,3,5,...$  
Hence we only need to check for $r=0,2,4,..$  
When $m=0$, $\int_{-1}^{1}1dx=2$, $I_{2}=(\frac{2}{3})[2f(-\frac{1}{2})-f(0)+2f(\frac{1}{2})]$
                                              $=(\frac{2}{3})[2-1+2]$
                                              $=2$.  
When $m=2$, $\int_{-1}^{1}x^{2}dx=\frac{2}{3}$, $I_{2}=(\frac{2}{3})[2(-\frac{1}{2})^{2}-0+2(\frac{1}{2})^{2}]=\frac{2}{3}$.  
When $m=4$, $\int_{-1}^{1}x^{4}dx=\frac{2}{5}$, $I_{2}=\frac{1}{6}\neq Q(f)$.  
Threrfore the degree of exactness r is 3, the order of infintesimal p is 5.  
b)When $m=0$, $I_{4}(1)=(\frac{1}{4})(1+3+3+1)=2=Q(1)$.  
  When $m=2$, $I_{4}(x^{2})=(\frac{1}{4})(1+\frac{1}{3}+\frac{1}{3}+1)$.  
  When $m=4$, $I_{4}(x^{4})=(\frac{1}{4})(1+\frac{1}{27}+\frac{1}{27}+1)=\frac{14}{27}\neq Q(x^{4})$.  
Therefore the degree of exactness r is 3, the order of infintesimal p is 5.  

---
## 5. Let $I_{w}(f)=\int_{0}^{1}w(x)f(x)dx$ with $w(x)=\sqrt{x}$, and consider the quadrature formula $Q(f)=af(x_{1})$. Find a and $x_{1}$ in such a way that Q has maximum degree of exactness r.  
---
sol:  
Takes $f(x)=1$.Then, $Q(f)=a=\int_{0}^{1}\sqrt{x}dx=\frac{2}{3}$.  
Takes $f(x)=x$. Then, $ax_{1}=\int_{0}^{1}x\sqrt{x}dx=\frac{2}{5}$, which implies that $x_{1}=\frac{3}{5}.$  
Take $r=2$, then $f(x)=x^{2}$. Thus, $\int_{0}^{1}\sqrt{x}x^{2}dx=\frac{2}{7}$. However, $ax^{2}_{1}=\frac{2}{3}(\frac{3}{5})^{2}=\frac{6}{25}\neq Q(f)$ .  
Therefore, we get maximum degree $r=1$, for $a=\tfrac{2}{3},\; x_1=\tfrac{3}{5}$.

---
## 7. Let us consider the quadrature formula $Q(f)=\alpha_{1}f(0)+\alpha_{2}f(1)+\alpha_{3}f^{'}(0)$ for the approximation of $I(f)=\int_{0}^{1}f(x)dx$, where $f\in C^{1}([0,1])$. Determine the coefficient $\alpha_{j}$, for $j=1,2,3$ in such a way that Q has degree of exactness $r=2$.  
Since Q has degree of exactness $r=2$. Then, we have $Q(f)=I(f)=\int_{0}^{1}x^{m}dx$, for $m=0,1,2$.  
Take $f(x)=1$. Then $I(1)=\int_{0}^{1}1dx=1$,  $Q(1)=\alpha_{1}+\alpha_{2}$.---(i)  
Take $f(x)=x$. Then $I(x)=\int_{0}^{1}xdx=\frac{1}{2}$,  $Q(x)=\alpha_{2}+\alpha_{3}$.---(ii)  
Take $f(x)=x^{2}$. Then $I(x^{2})=\int_{0}^{1}x^{2}dx=\frac{1}{3}$,  $Q(x^{2})=\alpha_{2}$. ---(iii)  
From (i),(ii) and (iii), we conclude that $\alpha_{1}=\frac{2}{3}; \alpha_{2}=\frac{1}{3}; \alpha_{3}= \frac{1}{6}$.  

