import numpy as np
from .ratchet_force import ratchet_force

class motor_head:
    def __init__(self, mass, offset, natural_length):
        self.mass = mass
        self.position = np.zeros(2)
        self.momentum = np.zeros(2)
        self.rachet_force = ratchet_force(natural_length,0.85*natural_length,20,100, offset)
    

    def spring_force(self, A, L_natural, K_cuadratic):
        """Spring force between `self` and `A` motorheads.

        Parameters
        ----------
        A : motor_head
            The other motor_head.
        L_natural : float
            Natural length of interaction.
        K_cuadratic : float
            Quadratic coefficient.

        Returns
        -------
        numpy.ndarray(2)
            X and Y components of the force on `self`.
        """
        L = A.position-self.position
        L_mod = np.sqrt(np.sum(np.square(L)))
        return -L/L_mod**2 * 2*K_cuadratic*(L_natural - L_mod)