"""Core model placeholder for Hollow Performance simulations.

Contains a minimal `HollowPerformance` class as a starting point.
"""

class HollowPerformance:
    """Placeholder core model class.

    Parameters
    ----------
    params : dict, optional
        Model parameters placeholder.
    """
    def __init__(self, params=None):
        self.params = params or {}

    def step(self):
        """Perform one model step (placeholder)."""
        # TODO: implement model dynamics
        return None


__all__ = ["HollowPerformance"]
