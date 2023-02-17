import numpy as np
import pandas as pd
from itertools import product, combinations
from operator import itemgetter

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle, Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d


class Piece:    
    def __init__(self, rainbow=False):
        self.side_map = {'x': 0, '-x':2,
                         'y': 1, '-y':3,
                         'z': 5, '-z':4}

        if rainbow:
            self.colors = np.array(['b', 'g', 'r', 'c', 'm', 'y'])
        else:
            self.colors = np.array(['k', 'k', 'k', 'k', 'k', 'k'])

    def __str__(self):
        return "|" + " ".join(self.colors) + "|"

    def __repr__(self):
        return "|" + " ".join(self.colors) + "|"

    def rotate(self, axis, number_of_turns):
        sides = ['z', 'y', 'x']
        sides.remove(axis)
        sides.extend(["-" + side for side in sides])
        sides_to_roll = [self.side_map[side] for side in sides]
        self.colors[sides_to_roll] = np.roll(self.colors[sides_to_roll], number_of_turns)

    def get_color(self, side):
        return self.colors[self.side_map[side]]
        
    def recolor(self, side, color):
        self.colors[self.side_map[side]] = color
    
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

class Cube:
    def __init__(self):
        self.pieces = np.empty((3, 3, 3), dtype=object)
        for x in range(3):
            for y in range(3):
                for z in range(3):                    
                    self.pieces[x, y, z] = Piece()

        # +x and -x
        for y in range(3):
            for z in range(3):                
                self.pieces[2, y, z].recolor('x', 'w')
                self.pieces[0, y, z].recolor('-x', 'y')
        # +y and -y
        for x in range(3):
            for z in range(3):              
                self.pieces[x, 2, z].recolor('y', 'r')
                self.pieces[x, 0, z].recolor('-y', 'o')
        # +z and -z
        for x in range(3):
            for y in range(3):                
                self.pieces[x, 2, 0].recolor('z', 'b')
                self.pieces[x, 0, 2].recolor('-z', 'g')

    def plot_side(self, side):
        if '-' in side:
            index = 0
        else:
            index = 2
            
        if 'x' in side:
            for y in range(3):
                for z in range(3):
                    print(self.pieces[index, y, z].get_color(side), end = " ")
                print("")
        elif 'y' in side:
            for x in range(3):
                for z in range(3):                
                    print(self.pieces[x, index, z].get_color(side), end = " ")
                print("")
        elif 'z' in side:
            for x in range(3):
                for y in range(3):                
                    print(self.pieces[x, y, index].get_color(side), end = " ")
                print("")
        else:
            pass    

    def move(self, move):
        if move == "U":
            self.pieces[:, :, 2] = np.rot90(self.pieces[:, :, 2])

            #print(self.pieces[:, :, 2])
            #print(self.pieces[:, :, 2].shape)
            
            for x in range(3):
                for y in range(3):
                    self.pieces[x, y, 2].rotate('z', -1)
                    
        #if move == "D":
        #    self.pieces[:, 2, :] = np.rot90(self.pieces[:, 2, :], 1)
                
if __name__ == "__main__":

    cube = Cube()
    print(cube.pieces)
    
    cube.plot_side('x')
    cube.plot_side('y')
    cube.plot_side('z')
    cube.plot_side('-x')
    cube.plot_side('-y')
    cube.plot_side('-z')

    cube.move('U')

    print(cube.pieces)
    
    print("After move:")
    cube.plot_side('x')
    cube.plot_side('y')
    cube.plot_side('z')
    cube.plot_side('-x')
    cube.plot_side('-y')
    cube.plot_side('-z')

    
    '''
    piece = Piece()
    piece.plot()
    plt.title("Unrotated")

    piece.rotate('z', 1)
    piece.plot()
    plt.title("Rotated in z by 1")

    plt.show()
    '''
