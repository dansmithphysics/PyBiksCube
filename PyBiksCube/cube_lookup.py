""" This module defines the Cube class based on look up tables """

from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from PyBiksCube.utilities import side_type_converter

class CubeLookup:
    """
    Representation of a Rubik's Cube. 
    Uses a lookup table for moves, optimized for speed.
    Includes:

    - commands to load and unload the cube state into a 54 character long string.
    - commands to perform moves on the cube following the UFDLRB notation
    - command to check if the cube is solved
    - plotting script for debugging and visualization

    Attributes
    ----------
    cube_state : array of strings, 54 entries for each face on cube
    move_array : 2D array of ints, used to convert moves to indices of cube_state
    """

    def __init__(self, lookup_table_file_name, cube_state=None):
        """
        The constructor for the Cube class.
        
        Parameters
        ----------
        lookup_table_file_name : str
            Location of the lookup table used for moves
        cube_state : str
            Load the cube faces from a 54 character long string.
            Default of None loads the solved cube.
        """

        self.cube_state = np.empty(54, dtype=str)

        if cube_state is None:
            self.set_default_cube_state()
        else:
            self.set_cube_state(cube_state)

        # Load up the workhorse of this operation
        #move_map = open(lookup_table_file_name, 'r').read()
        #move_map = eval(move_map)

        move_map = {'U': [6, 3, 0, 7, 4, 1, 8, 5, 2, 36, 37, 38, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 9, 10, 11, 30, 31, 32, 33, 34, 35, 45, 46, 47, 39, 40, 41, 42, 43, 44, 27, 28, 29, 48, 49, 50, 51, 52, 53],
                    'F': [0, 1, 2, 3, 4, 5, 35, 32, 29, 15, 12, 9, 16, 13, 10, 17, 14, 11, 42, 39, 36, 21, 22, 23, 24, 25, 26, 27, 28, 18, 30, 31, 19, 33, 34, 20, 6, 37, 38, 7, 40, 41, 8, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
                    'D': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 33, 34, 35, 24, 21, 18, 25, 22, 19, 26, 23, 20, 27, 28, 29, 30, 31, 32, 51, 52, 53, 36, 37, 38, 39, 40, 41, 15, 16, 17, 45, 46, 47, 48, 49, 50, 42, 43, 44],
                    'L': [53, 1, 2, 50, 4, 5, 47, 7, 8, 0, 10, 11, 3, 13, 14, 6, 16, 17, 9, 19, 20, 12, 22, 23, 15, 25, 26, 33, 30, 27, 34, 31, 28, 35, 32, 29, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 24, 48, 49, 21, 51, 52, 18],
                    'R': [0, 1, 11, 3, 4, 14, 6, 7, 17, 9, 10, 20, 12, 13, 23, 15, 16, 26, 18, 19, 51, 21, 22, 48, 24, 25, 45, 27, 28, 29, 30, 31, 32, 33, 34, 35, 42, 39, 36, 43, 40, 37, 44, 41, 38, 8, 46, 47, 5, 49, 50, 2, 52, 53],
                    'B': [38, 41, 44, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 27, 30, 33, 2, 28, 29, 1, 31, 32, 0, 34, 35, 36, 37, 26, 39, 40, 25, 42, 43, 24, 51, 48, 45, 52, 49, 46, 53, 50, 47],
                    "U'": [2, 5, 8, 1, 4, 7, 0, 3, 6, 27, 28, 29, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 45, 46, 47, 30, 31, 32, 33, 34, 35, 9, 10, 11, 39, 40, 41, 42, 43, 44, 36, 37, 38, 48, 49, 50, 51, 52, 53],
                    "F'": [0, 1, 2, 3, 4, 5, 36, 39, 42, 11, 14, 17, 10, 13, 16, 9, 12, 15, 29, 32, 35, 21, 22, 23, 24, 25, 26, 27, 28, 8, 30, 31, 7, 33, 34, 6, 20, 37, 38, 19, 40, 41, 18, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
                    "D'": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 42, 43, 44, 20, 23, 26, 19, 22, 25, 18, 21, 24, 27, 28, 29, 30, 31, 32, 15, 16, 17, 36, 37, 38, 39, 40, 41, 51, 52, 53, 45, 46, 47, 48, 49, 50, 33, 34, 35],
                    "L'": [9, 1, 2, 12, 4, 5, 15, 7, 8, 18, 10, 11, 21, 13, 14, 24, 16, 17, 53, 19, 20, 50, 22, 23, 47, 25, 26, 29, 32, 35, 28, 31, 34, 27, 30, 33, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 6, 48, 49, 3, 51, 52, 0],
                    "R'": [0, 1, 51, 3, 4, 48, 6, 7, 45, 9, 10, 2, 12, 13, 5, 15, 16, 8, 18, 19, 11, 21, 22, 14, 24, 25, 17, 27, 28, 29, 30, 31, 32, 33, 34, 35, 38, 41, 44, 37, 40, 43, 36, 39, 42, 26, 46, 47, 23, 49, 50, 20, 52, 53],
                    "B'": [33, 30, 27, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 44, 41, 38, 24, 28, 29, 25, 31, 32, 26, 34, 35, 36, 37, 0, 39, 40, 1, 42, 43, 2, 47, 50, 53, 46, 49, 52, 45, 48, 51]}

        self.move_array = np.empty((12, 54), dtype=np.int16)
        for i, key in enumerate(move_map.keys()):
            self.move_array[i] = move_map[key]

    def set_cube_state(self, cube_state_):
        self.cube_state = np.array(list(cube_state_), dtype=str)

    def get_cube_state(self):
        return "".join(self.cube_state)

    def get_raw_cube_state(self):
        return self.cube_state

    def move_decoder(self, move_command):
        if isinstance(move_command, (list, np.ndarray)):
            for move_command_ in move_command:
                self.move_decoder(move_command_)
            return

        if not isinstance(move_command, (int, np.int16)):
            raise ValueError("Move command should be a int")

        if move_command < 0 or move_command >= 12:
            raise ValueError(f"Not a valid move_command: {move_command}")

        self._fundamental_move(move_command)

    def _fundamental_move(self, move_command):
        self.cube_state = self.cube_state[self.move_array[move_command]]

    def randomize(self, n_moves=None):
        if n_moves is None:
            n_moves = np.random.randint(1, 30)
        mc_moves = np.random.choice(np.arange(12, dtype=np.int16), n_moves)
        self.move_decoder(mc_moves)
        return mc_moves

    def set_default_cube_state(self):
        self.set_cube_state("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww")

    def check_solved(self):
        return self.get_cube_state() == "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"

    def check_match_against_key(self, key):
        converted_key = np.array(list(key), dtype=str)
        return np.sum(np.logical_and(converted_key == self.cube_state, converted_key != 'k')) == np.sum(converted_key != 'k')

    def plot(self):
        """
        Creates a matplotlib plot of the cube
        layed out in a cross.
        Great for debugging.
        """

        _, ax = plt.subplots(figsize=(12, 9))

        for i, (y_pos, x_pos) in enumerate(product(range(3), repeat=2)):
            i += 9 * 0
            y_pos = 5-y_pos
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor="black",
                             facecolor=self.cube_state[i])
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i)

        for i, (y_pos, x_pos) in enumerate(product(range(3), repeat=2)):
            i += 9 * 1
            y_pos = 2-y_pos
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor="black",
                             facecolor=self.cube_state[i])
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i)

        for i, (y_pos, x_pos) in enumerate(product(range(3), repeat=2)):
            i += 9 * 2
            y_pos = -1-y_pos
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor="black",
                             facecolor=self.cube_state[i])
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i)

        for i, (y_pos, x_pos) in enumerate(product(range(3), repeat=2)):
            i += 9 * 3
            x_pos = x_pos - 3
            y_pos = 2-y_pos
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor="black",
                             facecolor=self.cube_state[i])
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i)

        for i, (y_pos, x_pos) in enumerate(product(range(3), repeat=2)):
            i += 9 * 4
            x_pos = x_pos + 3
            y_pos = 2-y_pos
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor="black",
                             facecolor=self.cube_state[i])
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i)

        for i, (y_pos, x_pos) in enumerate(product(range(3), repeat=2)):
            i += 9 * 5
            x_pos = x_pos + 6
            y_pos = 2-y_pos
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor="black",
                             facecolor=self.cube_state[i])
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i)

        ax.set_xlim(-3, 9)
        ax.set_ylim(-3, 6)

if __name__ == "__main__":
    # UFDLRB
    cube = CubeLookup("./data/cube_lookup_table.txt")
    cube.move_decoder(0)
    cube.plot()
    plt.show()
