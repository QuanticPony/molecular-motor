import numpy as np
from .motor_head import motor_head

class box_muller():
    @classmethod
    def __call__(cls):
        while True:
            cls._u1 = np.random.uniform()
            cls._u2 = np.random.uniform()

            cls._R = np.sqrt(-2 * np.log(cls._u1))
            cls._Theta = 2 * np.pi * cls._u2
            cls._X = cls._R * np.cos(cls._Theta)
            cls._Y = cls._R * np.sin(cls._Theta)
            yield cls._X
            yield cls._Y
                   
class verlet_integrator:
    def __init__(self, temporal_delta, dumping, betta):
        self.temporal_delta = temporal_delta
        self.dumping = dumping
        self.betta = betta
        self.update_factors()
        self.box_muller = box_muller()    
        
    def __call__(self, motor_heads, potential_active):
        randum = np.zeros((2,2))
        for i in range(2):
            for j in range(2):
                randum[i,j] = self.square * next(self.box_muller())
        m1, m2 = motor_heads
        Force = np.zeros((len(motor_heads), 2)) 
        Force_new = np.zeros((len(motor_heads), 2)) 
        Force[0,:] = m1.spring_force(m2, 0.3, 1000) + m1.rachet_force(m1.position, potential_active[0]) * potential_active[0]
        Force[1,:] = m2.spring_force(m1, 0.3, 1000) + m2.rachet_force(m2.position, potential_active[1]) * potential_active[1]

        m1.position = m1.position + self._b *self.temporal_delta * m1.momentum/m1.mass + 0.5 * self._b *self.temporal_delta *self.temporal_delta * Force[0] /m1.mass + 0.5 * self._b *self.temporal_delta * randum[0] /m1.mass;
        m2.position = m2.position + self._b *self.temporal_delta * m2.momentum/m2.mass + 0.5 * self._b *self.temporal_delta *self.temporal_delta * Force[1] /m2.mass + 0.5 * self._b *self.temporal_delta * randum[1] /m2.mass;
	
        Force_new[0,:] = m1.spring_force( m2, 0.3, 1000) + m1.rachet_force(m1.position, potential_active[0]) * potential_active[0]
        Force_new[1,:] = m2.spring_force( m1, 0.3, 1000) + m2.rachet_force(m2.position, potential_active[1]) * potential_active[1]
        
        m1.momentum = self._a * m1.momentum + 0.5 *self.temporal_delta * (self._a * Force[0] + Force_new[0]) + self._b * randum[0];
        m2.momentum = self._a * m2.momentum + 0.5 *self.temporal_delta * (self._a * Force[1] + Force_new[1]) + self._b * randum[1];
	
    def update_factors(self):
        self._factor = 0.5 * self.dumping * self.temporal_delta
        self._b = 1.0 / (1.0 + self._factor)
        self._a = (1.0 - self._factor) * self._b
        
    @property
    def betta(self):
        return self._betta
    
    @betta.setter
    def betta(self, value):
        self._betta = value
        self.square = np.sqrt(2 * self.dumping * self.temporal_delta/self.betta);