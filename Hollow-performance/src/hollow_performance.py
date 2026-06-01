"""Core implementation of the Hollow Performance mathematical model.
"""

import numpy as np


class HollowPerformanceModel:
    """
    Implements the first‑principles model:
    - Y = 1 - (1-K)*(1-A)
    - L = η*(1-K)*Q*G*exp(-λτ/(1+ρS))
    - K_{t+1} = K + L - offload - forget - social
    """

    def __init__(self, eta=0.3, lam=0.15, phi=0.4, rho=0.5,
                 alpha=1.0, beta=0.0, forget_rate=0.05,
                 social_loss=0.0, tau=1.0):
        self.eta = eta
        self.lam = lam
        self.phi = phi
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.forget_rate = forget_rate
        self.social_loss = social_loss
        self.tau = tau

    def observed_performance(self, K, A):
        """Y = 1 - (1-K)*(1-A)"""
        return 1.0 - (1.0 - K) * (1.0 - A)

    def learning_loop_strength(self, P, F, J, B):
        """G = α·P·F·J·B + β"""
        return self.alpha * P * F * J * B + self.beta

    def context_quality(self, M, difficulty_fit, load_fit):
        """Q = M * difficulty_fit * load_fit"""
        return M * difficulty_fit * load_fit

    def retention_factor(self, S):
        """exp(-λτ/(1+ρS))"""
        exp_arg = -self.lam * self.tau / (1.0 + self.rho * S)
        return np.exp(exp_arg)

    def durable_learning(self, K, Q, G, retention):
        """L = η·(1-K)·Q·G·retention"""
        return self.eta * (1.0 - K) * Q * G * retention

    def offload_loss(self, A, P, B):
        """δ_off = φ·A·(1-P)·(1-B)"""
        return self.phi * A * (1.0 - P) * (1.0 - B)

    def forget_loss(self, K):
        """δ_forget = forget_rate * K"""
        return self.forget_rate * K

    def mastery_update(self, K, L, offload, forget, social=0.0):
        """K_{t+1} = K + L - offload - forget - social, clipped to [0,1]"""
        new_K = K + L - offload - forget - social
        return np.clip(new_K, 0.0, 1.0)

    @staticmethod
    def risk_boundary(kappa):
        """Safe region: D(1-V) < 1/(1+κ)"""
        return 1.0 / (1.0 + kappa)


__all__ = ["HollowPerformanceModel"]
