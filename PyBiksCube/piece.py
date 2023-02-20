import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d

from PyBiksCube.utilities import side_type_converter
    
class Piece:    
    def __init__(self):
        self.colors = np.array(['k', 'k', 'k', 'k', 'k', 'k'])

        # The sides that are rotated when a turn is initiated on given face key
        self.turn_sequences = {'F': ['U', 'R', 'D', 'L'],
                               'B': ['U', 'L', 'D', 'R'],
                               'R': ['U', 'B', 'D', 'F'],
                               'L': ['U', 'F', 'D', 'B'],
                               'U': ['F', 'L', 'B', 'R'],
                               'D': ['F', 'R', 'B', 'L']}

        self.side_to_index_map = {'F': 0,
                                  'B': 2,
                                  'R': 1,
                                  'L': 3,
                                  'U': 5,
                                  'D': 4}
        
    def __str__(self):
        return "|" + " ".join(self.colors) + "|"

    def __repr__(self):
        return "|" + " ".join(self.colors) + "|"
    
    def side_to_index(self, side):        
        ''' Defines the, perhaps strange, coordinate system'''
        converted_side = side_type_converter(side)

        if isinstance(converted_side, list):
            return [self.side_to_index(side_) for side_ in converted_side]

        if converted_side not in self.side_to_index_map:
            raise ValueError("side does not follow UFDLRB notation")
        else:
            return self.side_to_index_map[converted_side]            
    
    def rotate(self, turn_axis, number_of_turns):        
        converted_turn_axis = side_type_converter(turn_axis)
        current_turn = self.turn_sequences[converted_turn_axis]
        sides_to_roll = self.side_to_index(current_turn)
        self.colors[sides_to_roll] = self.colors[np.roll(sides_to_roll, number_of_turns)]

    def get_color(self, side):
        converted_side = side_type_converter(side)
        return self.colors[self.side_to_index(converted_side)]
        
    def set_color(self, side, color):
        converted_side = side_type_converter(side)
        self.colors[self.side_to_index(converted_side)] = color
    
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_aspect("equal")
        ax.set_autoscale_on(True)

        r = [-10, 10]
        ax.set_xlim(r)
        ax.set_ylim(r)
        ax.set_zlim(r)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        coord_system = [[2, 'x'], [2, 'y'], [-2, 'x'], [-2, 'y'], [-2, 'z'], [2, 'z']]
        for i, (z, zdir) in enumerate(coord_system):
            side = Rectangle((-2, -2), 4, 4, facecolor=self.colors[i])
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=z, zdir=zdir)
