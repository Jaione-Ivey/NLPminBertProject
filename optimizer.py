# -*- coding: utf-8 -*-
"""optimizer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZVcA4CZasqFeVsjEHinx2dvXNYr8TmQu
"""

from typing import Callable, Iterable, Tuple
import math

import torch
from torch.optim import Optimizer


class AdamW(Optimizer):
    def __init__(
            self,
            params: Iterable[torch.nn.parameter.Parameter],
            lr: float = 1e-3,
            betas: Tuple[float, float] = (0.9, 0.999),
            eps: float = 1e-6,
            weight_decay: float = 0.0,
            correct_bias: bool = True,
    ):
        if lr < 0.0:
            raise ValueError("Invalid learning rate: {} - should be >= 0.0".format(lr))
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError("Invalid beta parameter: {} - should be in [0.0, 1.0[".format(betas[0]))
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError("Invalid beta parameter: {} - should be in [0.0, 1.0[".format(betas[1]))
        if not 0.0 <= eps:
            raise ValueError("Invalid epsilon value: {} - should be >= 0.0".format(eps))
        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay, correct_bias=correct_bias)
        super().__init__(params, defaults)

    def step(self, closure: Callable = None):
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None:
                    continue
                grad = p.grad.data
                if grad.is_sparse:
                    raise RuntimeError("Adam does not support sparse gradients, please consider SparseAdam instead")

                # State should be stored in this dictionary
                state = self.state[p]

                # Access hyperparameters from the `group` dictionary
                alpha = group["lr"]

                # Complete the implementation of AdamW here, reading and saving
                # your state in the `state` dictionary above.
                # The hyperparameters can be read from the `group` dictionary
                # (they are lr, betas, eps, weight_decay, as saved in the constructor).
                #
                # 1- Update first and second moments of the gradients
                # 2- Apply bias correction
                #    (using the "efficient version" given in https://arxiv.org/abs/1412.6980;
                #     also given in the pseudo-code in the project description).
                # 3- Update parameters (p.data).
                # 4- After that main gradient-based update, update again using weight decay
                #    (incorporating the learning rate again).

                ### TODO
                # state initialization
                if len(state) == 0:
                    state["step"] = 0
                    # Initialize first and second moments
                    state["exp_avg"] = torch.zeros_like(p.data)
                    state["exp_avg_sq"] = torch.zeros_like(p.data)

                exp_avg, exp_avg_sq = state["exp_avg"], state["exp_avg_sq"]

                beta1, beta2 = group["betas"]
                state["step"] += 1
                # 1. Compute first and second moments of the gradients
                #beta1, beta2 = group["betas"]
                #eps = group["eps"]

                # Retrieve the first and second moments from the state dictionary
                #m = state.get("m", torch.zeros_like(p.data))
                #v = state.get("v", torch.zeros_like(p.data))

                # Update moments
                #m.mul_(beta1).add_(grad, alpha=1 - beta1)
                #v.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

                # 2. Apply bias correction
                #m_hat = m / (1 - beta1)
                #v_hat = v / (1 - beta2)
                bias_correction1 = 1 - beta1 ** state["step"]
                bias_correction2 = 1 - beta2 ** state["step"]

                # 3. Update parameters
                #p.data.addcdiv_(m_hat, (v_hat.sqrt() + eps), value=-alpha)
                step_size = group["lr"] / bias_correction1
                denom = (exp_avg_sq.sqrt() / math.sqrt(bias_correction2)).add_(group["eps"])
                p.data.addcdiv_(exp_avg, denom, value=-step_size)

                # 4. Apply weight decay
                #if group["weight_decay"] != 0:
                    #p.data.mul_(1 - alpha * group["weight_decay"])
                if group["weight_decay"] != 0:
                    p.data.mul_(1 - group["lr"] * group["weight_decay"])
                #raise NotImplementedError

                # Debugging output
                print("Parameter Update:")
                print(p.data)
                print("First Moment (exp_avg):")
                print(exp_avg)
                print("Second Moment (exp_avg_sq):")
                print(exp_avg_sq)


        return loss