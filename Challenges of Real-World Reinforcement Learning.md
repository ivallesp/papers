# Challenges of Real-World Reinforcement Learning

**Gabriel Dulac-Arnold, Daniel Mankowitz, Todd Hester**

*ICML 2019*

The overall purpose of the paper is to claim that RL in real world is much more difficult than RL in research. 9 challenges that must be addressed to productionize RL on real world problems are presented. The main problems are that in real world, there is rarely a good simulator, the systems are stochastic and non-stationary, they have safety constraints and running them can be expensive and slow.

In most of the cases, the existing system is controlled by an existing policy (human or black-box). This policy is denoted as behavior policy $π_B$

## 1. Training off-line from fixed logs of an external behavior policy
This challenge applies often when we are planning to deploy an RL approach to replace a previous control system and we have logs of that system available. This setup is off-line and off-policy, the policy needs to be trained on batches of data (batch RL).

$D_{\pi B}$  is the set of experiences produced by policy $\pi_B$. We use $D_{\pi B}$ to train $\pi_0$. Then we use that policy to collect $D_{\pi 0}$, that we use to train $\pi_1$, and so on.

![](Challenges&#32;of&#32;Real-World&#32;Reinforcement&#32;Learning/batchrl.png)

It may also be need to estimate the performance of the policy offline, before deploying it. There are several techniques like importance sampling, MAGIC or MRDR. Sometimes, the most important policy to evaluate is the initial one (trained from the $\pi_B$), given that it would provide the warm-start performance which would dictate whether access to the system will be granted.

## 2. Learning on the real system from limited samples
Depending on the system, the exploration must be limited; hence the resulting data will be low variance. It may happen that the logs of the behavioral policy cover very little of the state space.

Learning iterations on a real system may take a long time due to slow iterations. Also long reward horizons may appear.

For that reasons, we aim for sample-efficient and performant algorithms.

Several efforts in this direction have been made.
- MAML: distributional switch through few shot learning
- Bootstrap DQN: Q-net ensemble with Thompson Sampling for efficient exploration
- Expert demonstrations
- Modeling transitions

## 3. High dimensional continuous state and action spaces
State and action spaces may be huge: think of a recommender system.

Embedding the action space, Action Elimination through Contextual Bandits and Deep Reinforcement Relevant Networks are some potential workarounds for this challenge.

The authors propose choosing methods that exploit contextual information that generalizes over unseen actions (e.g. embedding the actions or using them as input).

## 4. Satisfying safety constraints
Sometimes, several constraints need to be satisfied to prevent the system to harm itself. Constraint violations will likely be very rare in the logs of the system.

There have been some works focused on constraining the MDP.

## 5. Partial observability and Non-Stationarity
Almost all the real cases are partially observable. E.g. if we run a recommender system, we have no observations of the mental state of the users.

These problems are usually formulated as Partially Observable Markov Decision Processes (POMDP). The key difference from the MDP and POMDP formulations is that in the latter the observation $x$ is separated from the state $s$ through an observation function $O(x|s)$.

To deal with this situation, some authors recommend incorporatin history in the observation of the agent (e.g. add several frames together to solve Atari Breakout). Others, generalize even more the problem and use RNN within the agent.

This problem also appears when a trained policy over a simulation needs to be deployed into the real system, as the difference between the systems are not observable. Most of the work discusses around adding perturbations in the simulation training environment to achieve a more robust policy: these strategies are known as Domain Randomization. Other work focuses on a Robust MDP definition, based in learning policies that maximize the worst case.

## 6. Unspecified and Multi-Objective reward functions
In most of the real use cases it is not clear what we need to optimize. Several systems have multi-dimensional costs and when an agent is trained to optimize one metric, the other metrics may be degraded. A lot of the work needed to be done lays in the reward function definition.

It is highly recommended to monitor each of the individual objectives separately in order to better understand the policy's tradeoffs.

Sometimes it may be desired to move away for an expectation maximization. An example could be a robotized manufacturing company where we need a minimum level of performance in all the robots, not on average. To achieve that, the authors recommend optimizing percentiles instead of expectations. Pointers: CVaR objective (Conditional Value at Risk) and distributional RL (to model distributions instead of expectations).

The paradigm of inverse RL, where we try to recover an underlying reward function from demonstrations, is also relevant here.

The authors recommend designing multi-objective global reward functions as a linear combination of sub-rewards. This way tracking each sub-reward is straightforward. It is also recommended to analyze the performance of the RL agent in the different co-existing populations. A possible procedure is to determine if rare catastrophic rewards are minimized over time.

## 7. Explainability
It must be also taken into account given that stakeholders need to be reassured about the agent intentions and they may need insights regarding failure cases. Being able to understand errors *a-posteriori* is fundamental.

There are some works where the policy is translated into a domain-specific programming language for enhancing human interpretation.

## 8. Real-time inference
Some systems need high speed of response. It might be taken into account at inference time.

## 9. System delays
There might be delays in several parts of the system (e.g. state, actuators, reward feedback, etc.)

It is important to study the source of delay.

Depending on the source and location of the delays, there are several methods pointed in the paper that can be of help.