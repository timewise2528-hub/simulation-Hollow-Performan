"""Run all four simulations from the paper and generate figures.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from src.hollow_performance import HollowPerformanceModel

# ------------------------------
# Simulation 1: Deterministic collapse (domain equilibrium)
# ------------------------------
def sim1_deterministic_collapse(model, blind_trust_vals, steps=200, A=0.9):
    K_eq = []
    for bt in blind_trust_vals:
        K = 0.8
        P = F = J = B = 1.0 - bt
        M = diff = load = 1.0
        S = 0.0
        Q = model.context_quality(M, diff, load)
        G = model.learning_loop_strength(P, F, J, B)
        ret = model.retention_factor(S)
        for _ in range(steps):
            L = model.durable_learning(K, Q, G, ret)
            off = model.offload_loss(A, P, B)
            forg = model.forget_loss(K)
            K = model.mastery_update(K, L, off, forg)
        K_eq.append(K)
    return np.array(K_eq)

# ------------------------------
# Simulation 2: Fixed blind trust
# ------------------------------
def sim2_fixed_blind_trust(model, blind_trust, T=220, A=0.9):
    K = 0.8
    P = F = J = B = 1.0 - blind_trust
    M = diff = load = 1.0
    S = 0.0
    Q = model.context_quality(M, diff, load)
    G = model.learning_loop_strength(P, F, J, B)
    ret = model.retention_factor(S)
    K_history = [K]
    Y_history = [model.observed_performance(K, A)]
    for _ in range(T):
        L = model.durable_learning(K, Q, G, ret)
        off = model.offload_loss(A, P, B)
        forg = model.forget_loss(K)
        K = model.mastery_update(K, L, off, forg)
        Y = model.observed_performance(K, A)
        K_history.append(K)
        Y_history.append(Y)
    return np.array(K_history), np.array(Y_history)

# ------------------------------
# Simulation 3: Random blind-trust agents
# ------------------------------
class Agent:
    def __init__(self, model, init_K=0.8, init_trust=0.2):
        self.model = model
        self.K = init_K
        self.trust = init_trust
        self.delegation = init_trust
        self.verification = 1.0 - init_trust
        self.unverified_delegation = self.delegation * (1.0 - self.verification)

    def update_trust(self, error_occurred, success_occurred, contagion_effect=0.05,
                     metacognition_strength=0.02):
        delta_contagion = contagion_effect * np.random.randn()
        delta_error = -0.1 if error_occurred else 0.0
        delta_success = 0.05 if success_occurred else 0.0
        delta_failure = -0.2 if error_occurred and np.random.rand() < 0.3 else 0.0
        delta_metacognition = metacognition_strength * self.trust
        delta = (delta_contagion + delta_error + delta_success +
                 delta_failure - delta_metacognition)
        self.trust = np.clip(self.trust + delta, 0.0, 1.0)
        self.delegation = self.trust
        self.verification = 1.0 - self.trust
        self.unverified_delegation = self.delegation * (1.0 - self.verification)

    def step(self, A=0.9, error_prob=0.05):
        P = F = J = B = self.verification
        M = diff = load = 1.0
        S = 0.0
        Q = self.model.context_quality(M, diff, load)
        G = self.model.learning_loop_strength(P, F, J, B)
        ret = self.model.retention_factor(S)
        L = self.model.durable_learning(self.K, Q, G, ret)
        off = self.model.offload_loss(A, P, B)
        forg = self.model.forget_loss(self.K)
        self.K = self.model.mastery_update(self.K, L, off, forg)
        error_occurred = np.random.rand() < (error_prob * self.unverified_delegation * 5)
        success_occurred = (not error_occurred) and (np.random.rand() < 0.2)
        self.update_trust(error_occurred, success_occurred)
        return self.K, self.unverified_delegation, error_occurred

def sim3_random_blind_trust(model, n_agents=900, T=220, A=0.9, init_trust=0.2):
    agents = [Agent(model, init_K=0.8, init_trust=init_trust) for _ in range(n_agents)]
    K_mean, Y_mean, r_mean, trust_mean = [], [], [], []
    for _ in range(T):
        k_vals, y_vals, r_vals, t_vals = [], [], [], []
        for ag in agents:
            K, r, _ = ag.step(A=A)
            Y = model.observed_performance(K, A)
            k_vals.append(K)
            y_vals.append(Y)
            r_vals.append(r)
            t_vals.append(ag.trust)
        K_mean.append(np.mean(k_vals))
        Y_mean.append(np.mean(y_vals))
        r_mean.append(np.mean(r_vals))
        trust_mean.append(np.mean(t_vals))
    return np.array(K_mean), np.array(Y_mean), np.array(r_mean), np.array(trust_mean)

# ------------------------------
# Simulation 4: Stochastic learning-loop
# ------------------------------
def sim4_stochastic_learning_loop(model, n_agents=900, T=220, A=0.9, hollow_drive=0.008):
    Ks = np.random.beta(5, 2, n_agents)
    K_history, Y_history, L_history = [], [], []
    for t in range(T):
        baseline = max(0.9 - hollow_drive * t, 0.1)
        P = np.random.beta(2, 2, n_agents) * baseline
        F = np.random.beta(2, 2, n_agents) * baseline
        J = np.random.beta(2, 2, n_agents) * baseline
        B = np.random.beta(2, 2, n_agents) * baseline
        M = np.random.beta(2, 2, n_agents) * baseline
        diff = np.random.beta(2, 2, n_agents) * baseline
        load = np.random.beta(2, 2, n_agents) * baseline
        S = np.random.beta(2, 5, n_agents) * baseline
        Q = model.context_quality(M, diff, load)
        G = model.learning_loop_strength(P, F, J, B)
        ret = model.retention_factor(S)
        L = model.durable_learning(Ks, Q, G, ret)
        off = model.offload_loss(A, P, B)
        forg = model.forget_loss(Ks)
        Ks_new = model.mastery_update(Ks, L, off, forg)
        Ks = Ks_new
        Y = model.observed_performance(Ks, A)
        K_history.append(np.mean(Ks))
        Y_history.append(np.mean(Y))
        L_history.append(np.mean(L))
        if np.mean(Ks) < 0.01:
            Ks = np.clip(Ks + 0.001 * np.random.randn(n_agents), 0.0, 1.0)
    return np.array(K_history), np.array(Y_history), np.array(L_history)

# ------------------------------
# Main runner
# ------------------------------
def main():
    model = HollowPerformanceModel()
    os.makedirs('../figures', exist_ok=True)
    os.makedirs('../simulations/data', exist_ok=True)

    # Sim 1
    bt_vals = np.linspace(0, 1, 50)
    K_eq = sim1_deterministic_collapse(model, bt_vals)
    plt.figure()
    plt.plot(bt_vals, K_eq, 'b-')
    plt.axhline(0.1, color='r', linestyle='--', label='Collapse threshold (K=0.1)')
    plt.xlabel('Blind trust')
    plt.ylabel('Equilibrium mastery K*')
    plt.title('Sim 1: Deterministic collapse')
    plt.legend()
    plt.savefig('../figures/sim1_deterministic.png')
    plt.close()

    # Sim 2
    K2, Y2 = sim2_fixed_blind_trust(model, blind_trust=0.075)
    plt.figure()
    plt.plot(K2, label='Mastery K')
    plt.plot(Y2, '--', label='Performance Y')
    plt.axhline(0.1, color='r', linestyle=':')
    plt.xlabel('Time step')
    plt.ylabel('Value')
    plt.title('Sim 2: Fixed blind trust = 7.5%')
    plt.legend()
    plt.savefig('../figures/sim2_fixed_trust.png')
    plt.close()

    # Sim 3
    K3, Y3, r3, trust3 = sim3_random_blind_trust(model)
    plt.figure()
    plt.plot(K3, label='Mean mastery K')
    plt.plot(Y3, '--', label='Mean performance Y')
    collapse_idx = np.where(K3 < 0.1)[0]
    if len(collapse_idx) > 0:
        plt.axvline(collapse_idx[0], color='red', linestyle='--')
    plt.xlabel('Time step')
    plt.ylabel('Value')
    plt.title('Sim 3: Random blind-trust agents')
    plt.legend()
    plt.savefig('../figures/sim3_random_trust.png')
    plt.close()

    # Sim 4
    K4, Y4, _ = sim4_stochastic_learning_loop(model)
    plt.figure()
    plt.plot(K4, label='Mean mastery K')
    plt.plot(Y4, '--', label='Mean performance Y')
    plt.xlabel('Time step')
    plt.ylabel('Value')
    plt.title('Sim 4: Stochastic learning-loop (hollow performance)')
    plt.legend()
    plt.savefig('../figures/sim4_stochastic.png')
    plt.close()

    # Print results
    print("\n=== Simulation Results Summary ===")
    collapse_bt = bt_vals[np.where(K_eq < 0.1)[0][0]]
    print(f"Sim 1: Collapse occurs at blind trust ≈ {collapse_bt:.3f}")
    print(f"Sim 2: Final K = {K2[-1]:.3f}, Final Y = {Y2[-1]:.3f}")
    if len(collapse_idx) > 0:
        print(f"Sim 3: First collapse at t={collapse_idx[0]}, mean trust={trust3[collapse_idx[0]]:.3f}, r={r3[collapse_idx[0]]:.3f}")
    print(f"Sim 4: Final K = {K4[-1]:.3f}, Final Y = {Y4[-1]:.3f}, gap = {Y4[-1]-K4[-1]:.3f}")
    print("\nAll figures saved to ../figures/")

if __name__ == "__main__":
    main()
