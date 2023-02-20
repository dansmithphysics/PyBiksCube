import numpy as np
import pandas as pd
from itertools import product, combinations
from operator import itemgetter

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle, Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d

def side_type_converter(side, reverse=False):
    ''' Going to stick with UFDLRB notation. '''

    if isinstance(side, list):
        return [side_type_converter(side_, reverse) for side_ in side]
    
    if reverse:
        if side in 'xyz':
            return side
        else:
            side_map = {'F': 'x', 'B':'-x',
                        'R': 'y', 'L':'-y',
                        'U': 'z', 'D':'-z'}
            if side not in side_map:
                raise ValueError
            else:
                return side_map[side]
    else:        
        if side in 'UFDLRB':
            return side
        else:
            side_map = {'x': 'F', '-x': 'B',                    
                        'y': 'R', '-y': 'L',                    
                        'z': 'U', '-z': 'D'}
            if side not in side_map:
                raise ValueError
            else:
                return side_map[side]
    
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

class Cube:
    def __init__(self, cube_state=None, randomize=False):
        
        self.pieces = np.empty((3, 3, 3), dtype=object)
        for i, j, k in product(range(3), repeat=3):
            self.pieces[i, j, k] = Piece()

        self.face_to_index_map = {"U": [(i, j, 2) for i, j in product(range(3), repeat=2)],
                                  "D": [(i, j, 0) for i, j in product(range(3), repeat=2)],
                                  "F": [(2, i, j) for i, j in product(range(3), repeat=2)],
                                  "B": [(0, i, j) for i, j in product(range(3), repeat=2)],
                                  "L": [(i, 0, j) for i, j in product(range(3), repeat=2)],
                                  "R": [(i, 2, j) for i, j in product(range(3), repeat=2)]}

        self.cube_state_map = {0: [(0, 0, 2), 'U'], 1: [(0, 1, 2), 'U'], 2: [(0, 2, 2), 'U'],
                               3: [(1, 0, 2), 'U'], 4: [(1, 1, 2), 'U'], 5: [(1, 2, 2), 'U'],
                               6: [(2, 0, 2), 'U'], 7: [(2, 1, 2), 'U'], 8: [(2, 2, 2), 'U'],
                               9: [(2, 0, 2), 'F'], 10: [(2, 1, 2), 'F'], 11: [(2, 2, 2), 'F'],
                               12: [(2, 0, 1), 'F'], 13: [(2, 1, 1), 'F'], 14: [(2, 2, 1), 'F'],
                               15: [(2, 0, 0), 'F'], 16: [(2, 1, 0), 'F'], 17: [(2, 2, 0), 'F'],
                               18: [(2, 0, 0), 'D'], 19: [(2, 1, 0), 'D'], 20: [(2, 2, 0), 'D'],
                               21: [(1, 0, 0), 'D'], 22: [(1, 1, 0), 'D'], 23: [(1, 2, 0), 'D'],
                               24: [(0, 0, 0), 'D'], 25: [(0, 1, 0), 'D'], 26: [(0, 2, 0), 'D'],
                               27: [(0, 0, 2), 'L'], 28: [(1, 0, 2), 'L'], 29: [(2, 0, 2), 'L'],
                               30: [(0, 0, 1), 'L'], 31: [(1, 0, 1), 'L'], 32: [(2, 0, 1), 'L'],
                               33: [(0, 0, 0), 'L'], 34: [(1, 0, 0), 'L'], 35: [(2, 0, 0), 'L'],
                               36: [(2, 2, 2), 'R'], 37: [(1, 2, 2), 'R'], 38: [(0, 2, 2), 'R'],
                               39: [(2, 2, 1), 'R'], 40: [(1, 2, 1), 'R'], 41: [(0, 2, 1), 'R'],
                               42: [(2, 2, 0), 'R'], 43: [(1, 2, 0), 'R'], 44: [(0, 2, 0), 'R'],
                               45: [(0, 2, 2), 'B'], 46: [(0, 1, 2), 'B'], 47: [(0, 0, 2), 'B'],
                               48: [(0, 2, 1), 'B'], 49: [(0, 1, 1), 'B'], 50: [(0, 0, 1), 'B'],
                               51: [(0, 2, 0), 'B'], 52: [(0, 1, 0), 'B'], 53: [(0, 0, 0), 'B']}
        
        if cube_state is not None:
            self.set_cube_state(cube_state)
        else:
            # +x and -x
            self.set_face_color('F', 'y')
            self.set_face_color('B', 'w')

            # +y and -y
            self.set_face_color('R', 'b')
            self.set_face_color('L', 'g')

            # +z and -z
            self.set_face_color('U', 'r')
            self.set_face_color('D', 'm') # no orange, so m it is!

        if randomize:
            self.randomize(np.random.randint(2, 20))

    def randomize(self, n_moves=10):
        move_commands = np.random.choice(["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"], n_moves)
        for move_command in move_commands:
            self.fundamental_move(move_command)
                
    def set_cube_state(self, cube_state):
        if len(cube_state) != 54:
            return ValueError("Cube state must be a 54-long list of chars or string of colors")

        for i_color, color in enumerate(cube_state):
            i_position, face = self.cube_state_map[i_color]
            self.pieces[i_position].set_color(face, color)

    def get_cube_state(self):
        # Do the opposite of set_cube_state, output the state string
        cube_state = np.empty(54, dtype='str')
        for i in np.arange(54):
            i_position, face = self.cube_state_map[i]
            cube_state[i] = self.pieces[i_position].get_color(face)
        return ''.join(cube_state)
        
    def set_face_color(self, face, color):
        converted_face = side_type_converter(face)
        
        for i_position in self.face_to_index_map[converted_face]:
            self.pieces[i_position].set_color(converted_face, color)

    def get_face_colors(self, face):
        converted_face = side_type_converter(face)

        colors_flat = np.empty(9, dtype='str')
        for i_flat, i_position in enumerate(self.face_to_index_map[converted_face]):
            colors_flat[i_flat] = self.pieces[i_position].get_color(converted_face)

        return colors_flat
            
    def print_face(self, face):
        converted_face = side_type_converter(face)
        print(face, end=" ")
        for i_position in self.face_to_index_map[converted_face]:
            print(i_position, end=", ")
            print(self.pieces[i_position].get_color(face), end = " | ")
        print(" ")
        print(self.get_color_face(converted_face).reshape((3, 3)))
        print(" ")

    def check_solved(self):
        ''' 
        perhaps this can be sped up by only looking at
        the minimum needed, but no worries.
        '''
        
        faces = self.face_to_index_map.keys()
        for face in faces:
            if len(np.unique(self.get_face_colors(face))) != 1:
                return False
        return True
        
    def fundamental_move(self, move_command):
        # first, sanitize the move face
        # only accepts UFDLRB notation.
        # if there is a prime, that means reverse
        
        if not isinstance(move_command, str):
            raise ValueError("Move command should be a string")

        move_command = move_command.strip()
        
        if len(move_command) == 0:
            return # I suppose a blank command is valid
        elif len(move_command) == 1:
            move_command = move_command.ljust(2)
        elif len(move_command) == 2:
            if move_command[1] not in ["'", " "]:
                raise ValueError("Primed commands should have a prime in their second position")
        else:
            raise ValueError("Move command should be a two character command")

        if move_command[0] not in 'UFDLRB':
            raise ValueError("Move command should follow UFDLRB notation")

        direction = 1
        if move_command[1] == "'":
            direction = -1
        move_command = move_command[0]

        # -1 is needed for the normally defined coordinate system of the notation
        handedness_correction = 1
        if move_command in "UFL":
            handedness_correction *= -1
        
        # The logic to do the shuffle ... not so easy!
        slice_of_pieces = np.array([self.pieces[i_position] for i_position in self.face_to_index_map[move_command]], dtype=object)        
        slice_of_pieces = slice_of_pieces.reshape((3, 3))
        slice_of_pieces = np.rot90(slice_of_pieces, handedness_correction * direction)
        for i_flattened, i_position in enumerate(self.face_to_index_map[move_command]):
            self.pieces[i_position] = slice_of_pieces.flatten()[i_flattened]
            self.pieces[i_position].rotate(move_command, direction)

    def plot(self):
        # Plot it like a normal person
        # first, the front:
        fig, ax = plt.subplots(figsize=(12, 9))
        
        for i_position in self.face_to_index_map['F']:
            x = i_position[1]
            y = i_position[2]
            rect = Rectangle((x, y), 1, 1, edgecolor='black', facecolor=self.pieces[i_position].get_color('F'))                             
            ax.add_patch(rect)
            ax.text(x + 0.1, y + 0.1, i_position)
        for i_position in self.face_to_index_map['R']:
            x = 3 + (2 -i_position[0])
            y = i_position[2]
            rect = Rectangle((x, y), 1, 1, edgecolor='black', facecolor=self.pieces[i_position].get_color('R'))                             
            ax.add_patch(rect)
            ax.text(x + 0.1, y + 0.1, i_position)
        for i_position in self.face_to_index_map['L']:
            x = -3+i_position[0]
            y = i_position[2]
            rect = Rectangle((x, y), 1, 1, edgecolor='black', facecolor=self.pieces[i_position].get_color('L'))                             
            ax.add_patch(rect)
            ax.text(x + 0.1, y + 0.1, i_position)
        for i_position in self.face_to_index_map['B']:
            x = 6 + (2-i_position[1])
            y = i_position[2]
            rect = Rectangle((x, y), 1, 1, edgecolor='black', facecolor=self.pieces[i_position].get_color('B'))
            ax.add_patch(rect)
            ax.text(x + 0.1, y + 0.1, i_position)
        for i_position in self.face_to_index_map['U']:
            x = i_position[1]
            y = 5-i_position[0]
            rect = Rectangle((x, y), 1, 1, edgecolor='black', facecolor=self.pieces[i_position].get_color('U'))
            ax.add_patch(rect)
            ax.text(x + 0.1, y + 0.1, i_position)
        for i_position in self.face_to_index_map['D']:
            x = i_position[1]
            y = i_position[0]-3
            rect = Rectangle((x, y), 1, 1, edgecolor='black', facecolor=self.pieces[i_position].get_color('D'))
            ax.add_patch(rect)
            ax.text(x + 0.1, y + 0.1, i_position)

        ax.set_xlim(-3, 9)
        ax.set_ylim(-3, 6)

            
if __name__ == "__main__":

    # UFDLRB

    cube_state = np.repeat(list("rymgbw"), 9)
    print(''.join(cube_state))
    
    cube = Cube()
    #cube.fundamental_move("U")
    cube.randomize(2)
    cube.plot()
    plt.title("After move")
    plt.show()
