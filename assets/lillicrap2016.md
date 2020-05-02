# Continuous control with Deep Reinforcement Learning

[Link to the paper](https://arxiv.org/abs/1509.02971)

**Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, Daan Wierstra**

*International Conference of Learning Representations, 2016*

Year: **2016**

This paper presents consequent of the DQN algorithm which is applicable to problems with continuous action-spaces.

- DQN is not easy to implement in problems with continuous action spaces given that one of the pieces of the update rule consists of calculating the maximum of the estimated q-value function over all the actions. If the space is continuous this problem becomes an optimization problem at every update step.
- One potential solution is to discretize the action space but an important limitation arises: the course of dimensionality.
- The authors suggest a new algorithm by implementing the tricks that stabilized the Q-Learning algorithm when implemented with deep learning networks, into an actor-critic framework.
- More specifically, the new algorithm consists of simply using a target network and a replay buffer into the well known Deterministic Policy Gradient (DPG) (see the formula below, where $\mu$ is the notation referring to the deterministic policy, as opposed to the common $\pi$). It builds the new algorithm known as Deep Deterministic Policy Gradient (DDPG).

  ![](lillicrap2016/formula-dpg.png)
  ![](lillicrap2016/algorithm-ddpg.png)

- The authors suggest some additional enhancements: (1) batch normalization, (2) a new term in the policy function implementing a Ornstein-Uhlenbeck process to generate temporally correlated random perturbations to do exploration and (3) "soft" target updates using a simple exponential decay function.
- The algorithm has been tested over several MuJoCo physics-related environments with continuous actions, from low-dimensional features and from the raw pixels. The approach showed competitive results and enables the application of off-policy reinforcement learning to continuous environments.

![](lillicrap2016/curves-ddpg.png)
![](lillicrap2016/table-results-ddpg.png)