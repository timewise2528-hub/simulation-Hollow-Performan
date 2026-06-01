"""Run a dynamic simulation with user‑specified parameters.
Usage: python dynamic_run.py --blind-trust 0.1 --steps 300 --ai-assistance 0.9
"""

import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from src.hollow_performance import HollowPerformanceModel

def dynamic_simulation(model, blind_trust, T, A, use_stochastic=False):
    K = 0.8
    P = F = J = B = 1.0 - blind_trust
    M = diff = load = 1.0
    S = 0.0
    Q = model.context_quality(M, diff, load)
    G = model.learning_loop_strength(P, F, J, B)
    ret = model.retention_factor(S)
    K_history = [K]
    Y_history = [model.observed_performance(K, A)]

    for t in range(T):
        if use_stochastic:
            noise = np.clip(np.random.normal(0, 0.05), -0.1, 0.1)
            Pc = np.clip(P + noise, 0, 1)
            Fc = np.clip(F + noise, 0, 1)
            Jc = np.clip(J + noise, 0, 1)
            Bc = np.clip(B + noise, 0, 1)
            Gc = model.learning_loop_strength(Pc, Fc, Jc, Bc)
        else:
            Gc = G

        L = model.durable_learning(K, Q, Gc, ret)
        off = model.offload_loss(A, P, B)
        forg = model.forget_loss(K)
        K = model.mastery_update(K, L, off, forg)
        Y = model.observed_performance(K, A)
        K_history.append(K)
        Y_history.append(Y)

    return np.array(K_history), np.array(Y_history)

def main():
    parser = argparse.ArgumentParser(description='Hollow Performance dynamic simulation')
    parser.add_argument('--blind-trust', type=float, default=0.1, help='Blind trust (1 - verification)')
    parser.add_argument('--steps', type=int, default=200, help='Number of time steps')
    parser.add_argument('--ai-assistance', type=float, default=0.9, help='AI assistance level A')
    parser.add_argument('--stochastic', action='store_true', help='Add stochastic noise each step')
    parser.add_argument('--eta', type=float, default=0.3, help='Learning rate η')
    parser.add_argument('--phi', type=float, default=0.4, help='Offload coefficient φ')
    args = parser.parse_args()

    model = HollowPerformanceModel(eta=args.eta, phi=args.phi)
    K, Y = dynamic_simulation(model, args.blind_trust, args.steps, args.ai_assistance,
                              use_stochastic=args.stochastic)

    plt.figure(figsize=(10,5))
    plt.plot(K, label='Mastery K(t)', linewidth=2)
    plt.plot(Y, '--', label='Performance Y(t)', linewidth=2)
    plt.xlabel('Time step')
    plt.ylabel('Value')
    plt.title(f'Dynamic Simulation | Blind trust = {args.blind_trust}, A={args.ai_assistance}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('dynamic_simulation.png')
    plt.show()
    print(f'Final K = {K[-1]:.3f}, Final Y = {Y[-1]:.3f}')

if __name__ == '__main__':
    main()
