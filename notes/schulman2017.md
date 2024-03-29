---
date: '2020-04-27'
tags: paper, ppo, rl
---
# Proximal Policy Optimization Algorithms

[Link to the paper](https://arxiv.org/abs/1707.06347)

**John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov**

*OpenAI Report*

Year: **2017**

The current work follows up from the TRPO development. The authors suggest an alternative to TRPO which is much simpler to implement. The algorithm is called PPO (Proximal Policy Optimization) and showed to perform very well and in a stable way.

The new objective function proposed in the current work relies on clipped probability ratios, as we will describe later.

First, the authors introduce the policy gradient methods, where the objective function is defined as follows. The gradient can be obtained by deriving the objective.

$$L^{PG}(\theta) = \hat{\mathbb{E}}_t \left[\log\pi_\theta(a_t|s_t)\hat{A_t}\right]$$


Secondly, the authors summarize the TRPO objective as follows, where $\delta$ is a hyperparameter.

$$\argmax_\theta \quad \hat{\mathbb{E}}_t \left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat{A}_t\right]$$

$$\text{subject to }\quad \hat{\mathbb{E}}_t \left[KL[\pi_{\theta_{old}}(a_t|s_t), \pi_\theta(a_t|s_t) ]   \right]\leq \delta$$

Although the theory justifies the use of the KL divergence term as a penalty, the authors suggested to use it as a constraint to allow bigger updates of the parameters.

## Proposal
PPO Starts from the unconstrained objective of the TRPO algorithm (known here as conservative policy iteration, CPI hereafter), and redefine the probability ratio as $r_t({\theta})=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$. Then, the CPI loss has this form.

$$L^{CPI}(\theta) = \hat{\mathbb{E}}_t\left[ \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}   \hat{A}_t \right] = \hat{\mathbb{E}}_t\left[ r_t({\theta})   \hat{A}_t \right]$$

Without a constraint, the algorithm easily diverges due to too large and destructive policy updates. The authors suggest solving that problem by redefining the objective as follows:

$$L^{CLIP} (\theta) = \hat{\mathbb{E}}_t\left[ \min \left(r_t({\theta})   \hat{A}_t,\quad \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right) \right]$$

Some considerations:
- The first term is the $L^{CPI}(\theta)$ objective
- The second term is the $L^{CPI}(\theta)$ with the $r_t(\theta)$ value clipped to $[1-\epsilon, 1+\epsilon]$. This, in the words of tha authors, removes the inventive of moving $r_t(\theta)$ outside that interval.
- $\epsilon$ is a hyperparameter; the authors recommend using $\epsilon=0.2$.
- The final objective $L^{CLIP}$ is a lower bound on the unclipped objective, as it is calculated as the minimum between the unclipped onbjective and the clipped one.
- With the clipping, we only limit the change in the policy when it makes the objective worse.
- The probability ratio is clipped on the left or on the right side depending on the sign of the advantage value.

The following diagram shows how the probability ratio $r_t(\theta)$ is clipped depending on the sign of the advantage value.

![](assets/schulman2017/ppo-cases.png)

Here we see that the new objective clips the probability ratio in the following cases:
- The advantage function shows a positive surprise and the probability of the new policy is more than $1+\epsilon$ times the old probability (i.e. $r_t(\theta)\geq 1+\epsilon$)
- The advantage function shows a negative surprise and the probability of the new policy is less than $1-\epsilon$ times the old probability (i.e. $r_t(\theta)\geq 1+\epsilon$)

In the rest of the cases, $L^{CLIP}(\theta) = L^{CPI}(\theta)$

The following figure gives intuition on how different objective functions vary as we interpolate along the new policy direction. The new policy has been chosen so that the KL divergence with the old policy is 0.2.

![](assets/schulman2017/ppo-interpolation.png)

The authors also suggest other approach consisting on implementing the $L^{CPI}$ loss with an adaptive penalty in the KL divergence coefficient. However, they report that the previous formulation showed better results in practice.

![](assets/schulman2017/adaptive-kl-penalty.png)

## Implementation notes
- The proposed algorithm is very similar to the vanilla policy gradient
- If a value function estimation is chosen to share parameters with the actor network, then it must be added as an extra component to the network loss.
- Usually, an additional term referred as entropy bonus is added in order to automatically handle exploration.
![](assets/schulman2017/full-ppo-loss.png)

The algorithm is very simple to implement.
![](assets/schulman2017/algorithm-ppo.png)

## Results
In the following table, the authors compare three versions of the current algorithm averaged over 21 runs (3 runs x 7 MuJoCo tasks), and also against other algorithms.

![](assets/schulman2017/ppo-variants-results.png)

![](assets/schulman2017/variants-ppo-comparison.png)

![](assets/schulman2017/ppo-and-others-curves.png)

Finally, the authors share a table with the results over all the Atari games and compare them with A2C and ACER algorithms.

![](assets/schulman2017/atari-games-results-ppo.png)


## Intuition
- In RL, the data on which the neural network learns depends on the current policy, rather than relying in a static dataset as is the case in supervised learning.
- The Advantage function is calculated as Return - Baseline_estimate. It quantifies how much better was the action that the agent chose based on the expectation of what it would normally happen in the state the agent was. Was the agent action better or worse than expected?
- Clipping the policy objective can be justified because the advantage function is nothing but a noisy estimate. We cannot fully 0trust a noisy estimate and hence we have to limit the updates.

|                      | $\pi>>>\pi_{old}$ ($r$ is large) | $\pi<<<\pi_{old}$ ($r$ is small) |
| :------------------: | :------------------------------: | :------------------------------: |
| A>0 (action is good) |               CLIP               |             NO CLIP              |
| A<0 (action is bad)  |             NO CLIP              |               CLIP               |

Notice that we are clipping in the cases in which the agent found a good action and is increasing the probability and when the agent found a bad action and is decreasing the probability. We are limiting the updates that seem consistent with the advantage function. In other words, the current policy is pessimistic and conservative, it doesn't fully rely on the advantage function. The cases where we don't clip $r$ correspond to the situations where the agent is correcting it's own overshoots.


## Additional references
- PG methods and PPO (video from Arxiv Insights): https://www.youtube.com/watch?v=5P7I-xPq8u8
- PPO clean implementation: https://github.com/higgsfield/RL-Adventure-2/blob/master/3.ppo.ipynb
- PPO official OpenAI blog post: https://blog.openai.com/openai-baselines-ppo/
- OpenAI baselines PPO implementations: https://github.com/openai/baselines/tree/master/baselines/ppo2 and https://github.com/openai/baselines/tree/master/baselines/ppo1