import matplotlib.pyplot as plt
from molecular_motor import molecular_motor
    
if __name__=='__main__':
    sim = molecular_motor()
    sim.period = 2000
    sim.length_potential = 0.5
    sim.low_point_potential = 0.45
    sim.potential_offset = 0.25
    
    sim.max_value_potential = 40
    sim.confinement_potential_coefficient = 100
    
    sim.prepare_canvas(steps_per_frame=40, frames_per_second=5)
    plt.show()