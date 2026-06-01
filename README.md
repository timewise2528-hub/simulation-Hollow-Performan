# Hollow Performance: A Closed-Loop Learning Theory of Human–AI Dependence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Authors**: Ramesh Neupane  
**Repository**: [https://github.com/timewise2528-hub/simulation-Hollow-Performan]  
**ORCID**:  0000-0001-5275-8735

This repository contains the complete mathematical models, synthetic simulations, and visualisation code for the paper:

> *Hollow Performance: A Closed-Loop Learning Theory of Human–AI Dependence*  
> *Mathematical Models, Synthetic Simulations, and Implications for Education, Health, Knowledge Work, and Society*

## Abstract

Large language models (LLMs) can raise visible task performance while weakening durable human mastery – a phenomenon we call **hollow performance**. This paper formalises two linked models:

1. **Simple risk model** of unverified delegation:  
   $r = D(1-V)$, with safety boundary $D(1-V) < \frac{1}{1+\kappa}$.

2. **First‑principles dynamic model** separating observed performance $Y_t$ from human mastery $K_t$:  
   $Y_t = 1-(1-K_t)(1-A_t)$,  
   and durable learning  
   $L_t = \eta(1-K_t)Q_t\,G(P_t,F_t,J_t,B_t)\exp\!\left(-\frac{\lambda\tau}{1+\rho S_t}\right)$.

Synthetic simulations show that blind AI substitution can keep $Y_t \approx 0.97$ while $K_t \to 0$. The code reproduces all simulations and figures from the paper.

## Mathematical Models & Code Mapping

All equations are implemented in [`src/hollow_performance.py`](src/hollow_performance.py). The table below maps each mathematical component to the corresponding method.

| Mathematical symbol | Description | Code method |
|---------------------|-------------|--------------|
| $Y_t = 1-(1-K_t)(1-A_t)$ | Observed performance | `observed_performance(K, A)` |
| $L_t = \eta(1-K_t)Q_t G \exp\!\left(-\frac{\lambda\tau}{1+\rho S_t}\right)$ | Durable learning | `durable_learning(K, Q, G, retention)` |
| $G(P,F,J,B) = \alpha P F J B + \beta$ | Learning‑loop strength | `learning_loop_strength(P, F, J, B)` |
| $Q_t = M_t \cdot \text{difficulty}_t \cdot \text{load}_t$ | Context quality | `context_quality(M, diff, load)` |
| $\exp\!\left(-\frac{\lambda\tau}{1+\rho S_t}\right)$ | Retention factor | `retention_factor(S)` |
| $\delta_{\text{off}} = \phi A_t (1-P_t)(1-B_t)$ | Passive offloading loss | `offload_loss(A, P, B)` |
| $\delta_{\text{forget}} = \delta_{\text{forget}} \cdot K_t$ | Forgetting | `forget_loss(K)` |
| $K_{t+1} = K_t + L_t - \delta_{\text{off}} - \delta_{\text{forget}}$ | Mastery update | `mastery_update(K, L, off, forget)` |
| $D(1-V) < \frac{1}{1+\kappa}$ | Safe risk boundary | `risk_boundary(kappa)` (static) |

### Simple Risk Model

- **Delegation** $D \in [0,1]$: degree of AI reliance  
- **Verification** $V \in [0,1]$: human verification / ownership  
- **Unverified delegation**: $r = D(1-V)$  
- **Risk weight** $\kappa \ge 0$ (domain‑specific)  
- **Safe region**: $D(1-V) < \frac{1}{1+\kappa}$

### First‑Principles Dynamic Model

- **Human mastery** $K_t \in [0,1]$: unaided capability  
- **AI assistance** $A_t \in [0,1]$  
- **Observed performance**: $Y_t = 1 - (1-K_t)(1-A_t)$  
- **Durable learning** $L_t$ (after delay $\tau$) uses four key learning‑loop components:  
  - $P_t$: prediction ownership  
  - $F_t$: feedback visibility  
  - $J_t$: judgment correction  
  - $B_t$: rebuild practice  
- **Context quality** $Q_t = M_t \cdot D_t \cdot C^{\text{load}}_t$  
- **Spaced practice** $S_t$ slows forgetting: $\exp(-\lambda\tau/(1+\rho S_t))$  
- **Passive offloading** loss: $\phi A_t (1-P_t)(1-B_t)$

## Repository Structure
hollow-performance/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── src/
│   └── hollow_performance.py    # Core model class
├── simulations/
│   ├── run_all.py               # Reproduce all four simulations + figures
│   ├── dynamic_run.py           # Interactive parameter sweeps
│   └── data/                    # Generated synthetic datasets (CSV)
├── notebooks/
│   └── explore.ipynb            # Jupyter notebook for step‑by‑step exploration
├── figures/                     # Pre‑generated figures (PNG, GIF)
│   ├── sim1_deterministic.png
│   ├── sim2_fixed_trust.png
│   ├── sim3_random_trust.png
│   ├── sim4_stochastic.png
│   └── animation_*.gif
└── tests/
    └── test_model.py            # Unit tests for equations

## Getting Started

### 1. Clone the repository

```bash
git clone **https://github.com/USERNAME/hollow-performance-llm-dependence.git**
cd hollow-performance-llm-dependence
