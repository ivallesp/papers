---
date: '2022-04-23'
tags: paper
---
# Gaussian Error Linear Units (GELUs)

[Link to the paper](https://arxiv.org/abs/1606.08415)

**Dan Hendrycks, Kevin Gimpel**

*arXiv Preprint*

Year: **2016**

This paper introduces GELUs, a new activation function for neural networks.

This new activation function is based on the CDF of the Gaussian distribution, as follows.

$$GELU(x) = x P(X \leq x)$$

To avoid the integral, it can also be approximated as follows.

$$GELU(x) \approx 0.5x(1+\tanh(\sqrt{2/x}(x+0.044715x^3))) \approx x\sigma(1.702x)$$

The authors assure that this function is more robust to noise than ReLU and ELU. Additionally, as $\mu$ and $\sigma$ of the Gaussian PDF approach $(0, 0)$, the activation becomes a ReLU. That is why GELU can be seen as a soft approximation to ReLU. 

In the paper there are many experiments showing that GELU performs better than ReLU and ELU, converging faster and to a better optimum.