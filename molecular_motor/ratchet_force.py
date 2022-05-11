import numpy as np

class ratchet_force:
    def __init__(self, natural_length, min_position, max_value, confinement_potential_coefficient, offset):
        self.natural_length = natural_length
        self.min_position = min_position
        self.max_value = max_value
        self.confinement_potential_coefficient = confinement_potential_coefficient
        self.offset = offset

    def __call__(self, position, ratchet=True):
        _x = (position[0] + self.offset) % self.natural_length
        return np.array([self.max_value/self.min_position * (_x < self.min_position) * (ratchet) +
                         self.max_value/(self.min_position-self.natural_length) * (_x >= self.min_position) * (ratchet) + 0,
                         -2*self.confinement_potential_coefficient*position[1] * (ratchet)])

    def potential_with_xy(self, x, y):
        _x = (x + self.offset) % self.natural_length
        return (_x < self.min_position) * -(_x-self.min_position)*self.max_value/self.min_position + (_x >= self.min_position) * (_x-self.min_position)*self.max_value/(self.natural_length-self.min_position) + self.confinement_potential_coefficient*y**2
