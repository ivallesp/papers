---
date: '2020-03-23'
tags: paper
---
# Neural Fitted Q Iteration - First Experiences with a Data Efficient Neural Reinforcement Learning Method

[Link to the paper](http://ml.informatik.uni-freiburg.de/former/_media/publications/rieecml05.pdf)

**Martin Riedmiller**

*Springer-Verlag Berlin Heidelberg 2005*

Year: **2005**

- **Objective**: using neural networks to approximate Q-value functions in RL while reducing the interaction with the plant.
  - **Advantages**: ability to approximate non-linear functions. It's a global representation algorithm and this provides the benefit of generalization.
  - **Drawbacks**: neural networks are global representation algorithms, and sometimes a weight change induced by an update in a part of the state space may destroy the learning in other parts of the state space (catastrophic forgetting), leading to long trainings or divergence.

- To **prevent catastrophic forgetting** it is proposed to provide previous experiences along with the new state-action results. For that, the author suggest to store all the state-action transitions in memory. (Similar to experience replay)

- The contribution of the author to the modeling approach consists of an enhancement of the weight update method, named **NFQ** (Neural Fitted Q Iteration).

- Although the author provides an example with immediate cost structure, they assure it works also with arbitrary cost structures.

- A useful technique named *hint-to-goal* is described, consisting of adding artificial experiences where the target is known to be zero. This helps the first stages of training.

- Very good **definition of episode**: An episode is a sequence of control cycles, that starts with an initial state and ends if the current state fulfills some termination condition (e.g. the system reached its goal state or a failure occured) or some maximum number of cycles has been reached.

- In the **results** section, the authors claim having achieved good policies with relatively small interaction with the plant (in the order of hundreds of episodes).
