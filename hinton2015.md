---
date: '2020-11-26'
tags: paper
---
# Distilling the Knowledge in a Neural Network

[Link to the paper](https://arxiv.org/abs/1503.02531)

**Geoffrey Hinton, Oriol Vinyals and Jeff Dean**

*Neural Information Processing Systems 2014*

Year: **2015**

This work presents a methodology to simplify models and even get better performance. They build this on top of the work of Rich Caruana, where they demonstrate that the knowledge of a large ensemble of neural networks can be transferred into a small single model.

All the work of this paper is done with the hypothesis that the probabilities of incorrect answers in classification algorithms gives a lot of information about how the large model tends to generalize. Building on that hypothesis, the authors suggest the following methodology: take a large model, increase the temperature of the softmax layer so that the model is not very "confident" in the output probabilities (soft target), and use the probabilities as target for teaching a smaller model. Once the small model is trained, decrease its softmax temperature.

The main difference between Caruana and Hinton's works relies in the fact that Caruana uses the logits and Hinton uses the probabilities with higher temperature. This last process is called "distillation".

The distillation can be done entirely on unlabelled data, although the authors remark that if labelled data is used, and a distillation loss (with soft-target labels) is combined with a cross-entropy loss (with hard-target labels), the training becomes much faster.

The temperature in the softmax layers is defined in the following equation, where $q$ represents the probabilities, $z$ the logits, and $T$ the temperature parameter.

$$q_i = \frac{e^{z_i/T}}{\sum_j{e^{z_j/T}}}$$

The authors recommend training distilled models with a weighted average between two loss functions: cross entropy with soft targets, and cross-entropy with hard targets (with output of the model at $T=1$). The authors highlighted that they found adding less weight to the second loss beneficial. Since the magnitudes of the gradients produced by the soft targets scale as $1/T^2$ it is important to multiply them by $T^2$ when using both targets combined.

It is shown in different experiments that the distilled model works even better than the cumbersome model, despite it's smaller capacity.

The soft-targets seem also to act as a regularizer, as the authors observed that the distilled models do not overfit, but just converge.

In the rest of the paper, the authors mention strategies of creating mixtures of experts and specialists models, assuming the problem of having a very big ensemble is circumvented by the distillation mechanism.
