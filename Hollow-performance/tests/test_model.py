import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.hollow_performance import HollowPerformanceModel

def test_observed_performance():
    m = HollowPerformanceModel()
    assert np.isclose(m.observed_performance(0.1, 0.9), 0.955)
    assert m.observed_performance(0, 0) == 0
    assert m.observed_performance(1, 0) == 1

def test_learning_loop_strength():
    m = HollowPerformanceModel(alpha=1.0, beta=0.0)
    assert m.learning_loop_strength(1,1,1,1) == 1.0
    assert m.learning_loop_strength(0,1,1,1) == 0.0
    m2 = HollowPerformanceModel(alpha=0.8, beta=0.2)
    assert np.isclose(m2.learning_loop_strength(0,1,1,1), 0.2)

def test_retention_factor():
    m = HollowPerformanceModel(lam=0.15, tau=1.0, rho=0.5)
    assert 0 < m.retention_factor(0) < 1
    assert m.retention_factor(np.inf) == np.exp(0)  # 1
    assert np.isclose(m.retention_factor(0), np.exp(-0.15))

def test_mastery_update():
    m = HollowPerformanceModel()
    K = 0.5
    new_K = m.mastery_update(K, L=0.1, offload=0.02, forget=0.03)
    assert np.isclose(new_K, 0.55)
    # clipping
    assert m.mastery_update(0.95, L=0.1, offload=0, forget=0) == 1.0
    assert m.mastery_update(0.05, L=0, offload=0.1, forget=0) == 0.0

if __name__ == "__main__":
    test_observed_performance()
    test_learning_loop_strength()
    test_retention_factor()
    test_mastery_update()
    print("All tests passed.")
