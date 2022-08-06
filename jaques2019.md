---
date: '2020-03-23'
tags: paper
---
# Way Off-Policy Batch Reinforcement Learning of Implicit Human Preferences in Dialog

[Link to the paper](https://arxiv.org/abs/1907.00456)

**Natasha Jaques, Asma Ghandeharioun, Judy Hanwen Shen, Craig Ferguson, Agata Lapedriza, Noah Jones, Shixiang Gu, Rosalind Picard**

*Cambridge, preprint. Under review*

Year: **2019**

Implementation: https://github.com/natashamjaques/neural_chat/tree/master/rl

Motivation: Off-policy as a mechanism to solve situations where (1) collecting data is costly and time consuming, (2) test before real world deployment is required

Batch RL often fails due to learning from data not heavily correlated with the current policy.
- These algorithms are inherently **optimistic in the face of uncertainty**. i.e. when taking the maximum over estimates of future reward, high variability estimates lead to overestimation bias.
- In normal RL settings, *optimism in the face of uncertainty*¡ is desired, given that it leads to exploration of highly variable spaces.
- In offline + off-policy RL *optimism in the face of uncertainty*, as exploration is not an option, the model is driven to parts of the state-action pair where there is little or no data to learn a good policy.

The paper proposes three techniques of addressing the problem:
- Penalize the KL divergence from batch data and current policy data to decrease the covariance shift. They enforce it by adding a KL term in the loss function of the Q-Learning algorithm, as follows $Q^\pi(s_t, a_t) = \mathbb{E}_\pi\left( \sum_{t'=t}^T r(s_{t'}, a_{t'})/c + \log p(a_{t'}|s_{t'}) - \log \pi(a_{t'}|s_{t'})\right)$. Where $p(a_{t'}|s_{t'})$ represents the prior distribution and $\pi(a_{t'}|s_{t'})$ the policy one.
- Use of dropout at training and inference phase to implement **pessimism in the face of uncertainty**. The way they enforce this effect is by calculating the minimum of each Q-value over a bunch of generated candidates using Monte Carlo. $Q(a_{t+1}, s_{t+1}) = min_i(Q_\theta(a_{t+1}, s_{t+1}; d_i))$. This will reduce the overestimation bias in the highly variable regions of the state-action space.
- They train a prior-based generative model using MLE from which the actions given a state are sampled $p(a|s)$. This way the priors of the batch are enforced in the action selection of the Q-learning procedure.

The authors apply these techniques to the dialog generation domain (details not covered in this notes), showing that both, the KL-control and the MC dropout bias reduction have a great impact in the stability of the final model. They highlight the importance of KL-control given that without it, the algorithm didn't converge on their application.