import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from .motor_head import motor_head
from .verlet_integrator import verlet_integrator

class molecular_motor:
    def __init__(self):
        self._length_potential = 0.5
        self.motor_heads = [motor_head(1, 0, self._length_potential), motor_head(1, self.length_potential/2, self._length_potential)]
        self.motor_heads[0].position[0] = 0.3
        self.integrator = verlet_integrator(0.01, 70, 2)
        self.iteration = 0
        self.Periode = 2000
        self._potential_offset = 1
        
    def prepare_canvas(self, steps_per_frame=40, frames_per_second=5):
        # self.fig, self.axs = plt.subplots(ncols=2, nrows=2)
        # gs = self.axs[1, 0].get_gridspec()
        # for ax in self.axs[1, :]:
        #     ax.remove()
        # self.ax_sliders = self.fig.add_subplot(gs[-1, :])
        
        self.steps_per_frame = steps_per_frame
        
        self.fig, self.axs = plt.subplots(figsize=(5,5))

        self.fig.tight_layout()
        self.animation = FuncAnimation(self.fig, self.replot, frames_per_second)
        
        self._prev_mean = sum(self.get_x_position())/2
        self.mesh_0 = np.meshgrid(np.linspace(self._prev_mean-0.5, self._prev_mean+0.5, 40), np.linspace(0,0.5,20), sparse=True)
        self.mesh_1 = np.meshgrid(np.linspace(self._prev_mean-0.5, self._prev_mean+0.5, 40), np.linspace(-0.5,0,20), sparse=True)
        self.xx_0, self.yy_0 = self.mesh_0
        self.xx_1, self.yy_1 = self.mesh_1
        
    def get_x_position(self):
        return [m.position[0] for m in self.motor_heads]
    def get_y_position(self):
        return [m.position[1] for m in self.motor_heads]
    
    def replot(self, *args):
        self.plot_state()
        # self.plot_mean_position()
    
    def plot_state(self):
        for _ in range(self.steps_per_frame):
            self.iteration = (self.iteration + 1) if self.iteration<self.Periode else 0
            first_head_potential = (self.iteration<(self.Periode/2))
            second_head_potential = ((self.Periode/2)<=self.iteration)
            self.integrator(self.motor_heads, np.array([first_head_potential, second_head_potential]))
        
        mean = sum(self.get_x_position())/2
        diff = mean - self._prev_mean
        
        self.xx_0 += diff
        self.xx_1 += diff
        mesh_0 = self.motor_heads[0].rachet_force.potential_with_xy(self.xx_0, self.yy_0)
        mesh_1 = self.motor_heads[1].rachet_force.potential_with_xy(self.xx_1, self.yy_1)
        
        try: #TODO: Add mean x values. maybe.
            self.axs[0,0].cla()
            self.axs[0,0].pcolormesh(self.xx_0, self.yy_0, mesh_0, vmax=self.motor_heads[0].rachet_force.max_value, cmap='viridis_r', alpha=0.3 + 0.7*first_head_potential)
            self.axs[0,0].pcolormesh(self.xx_1, self.yy_1, mesh_1, vmax=self.motor_heads[1].rachet_force.max_value, cmap='inferno_r', alpha=0.3 + 0.7*second_head_potential)
            self.axs[0,0].scatter(self.get_x_position(), self.get_y_position(), color=['blue', 'red'])
        except TypeError:
            self.axs.cla()
            self.axs.pcolormesh(self.xx_0, self.yy_0, mesh_0, vmax=self.motor_heads[0].rachet_force.max_value, cmap='viridis_r', alpha=0.3 + 0.7*first_head_potential)
            self.axs.pcolormesh(self.xx_1, self.yy_1, mesh_1, vmax=self.motor_heads[1].rachet_force.max_value, cmap='inferno_r', alpha=0.3 + 0.7*second_head_potential)
            self.axs.scatter(self.get_x_position(), self.get_y_position(), color=['blue', 'red'])
            self.axs.plot(self.get_x_position(), self.get_y_position(), color='black')
        self._prev_mean = mean
        
    def plot_mean_position(self):
        mean_x = sum(self.get_x_position())/2
        self.axs[0,1].scatter(self.iteration, mean_x, color='black')
        
    @property
    def length_potential(self):
        return self._length_potential
        
    @length_potential.setter
    def length_potential(self, value):
        self._length_potential = value
        self.motor_heads[1].rachet_force.offset = self.potential_offset
        for m in self.motor_heads:
            m.rachet_force.natural_length = value
        
    @property
    def low_point_potential(self):
        return self._low_point_potential
        
    @low_point_potential.setter
    def low_point_potential(self, value):
        self._low_point_potential = value
        for m in self.motor_heads:
            m.rachet_force.min_position = value
        
    @property
    def max_value_potential(self):
        return self._max_value_potential
        
    @max_value_potential.setter
    def max_value_potential(self, value):
        self._max_value_potential = value
        for m in self.motor_heads:
            m.rachet_force.max_value = value
    
    @property
    def confinement_potential_coefficient(self):
        return self._confinement_potential_coefficient
        
    @confinement_potential_coefficient.setter
    def confinement_potential_coefficient(self, value):
        self._confinement_potential_coefficient = value
        for m in self.motor_heads:
            m.rachet_force.confinement_potential_coefficient = value
        
    #! This may be innecessary
    @property
    def potential_offset(self):
        return self._potential_offset

    @potential_offset.setter
    def potential_offset(self, value):
        self._potential_offset = value
        self.motor_heads[0].rachet_force.offset = 0
        self.motor_heads[1].rachet_force.offset = value
        