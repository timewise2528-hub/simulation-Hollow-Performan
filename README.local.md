Skip to content
timewise2528-hub
simulation-Hollow-Performan
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security and quality
Insights
Settings
Files
Go to file
t
T
README.md
simulation-Hollow-Performan
/
README.md
in
main

Edit

Preview
Indent mode

Spaces
Indent size

2
Line wrap mode

Soft wrap
Editing README.md file contents
  1
  2
  3
  4
  5
  6
  7
  8
  9
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
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
Use Control + Shift + m to toggle the tab key moving focus. Alternatively, use esc then tab to move to the next interactive element on the page.
No file chosen
Attach files by dragging & dropping, selecting or pasting them.
