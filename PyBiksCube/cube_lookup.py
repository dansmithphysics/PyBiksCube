""" This module defines the Cube class based on look up tables """

from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from PyBiksCube.utilities import side_type_converter
from PyBiksCube import Piece

class CubeLookup:
    def __init__(self, lookup_table_file_name, cube_state=None):
        
        self.cube_state = np.empty(54).astype("|S1")
                
        if cube_state != None:
            self.set_cube_state(cube_state)
        else:
            self.set_cube_state("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww")

        # Load up the workhorse of this operation
        self.move_map = open(lookup_table_file_name, 'r').read()
        self.move_map = eval(self.move_map)

    def set_cube_state(self, cube_state):
        if not isinstance(cube_state, (str, np.ndarray)):
            raise ValueError("Move command should be a string or list of chr")

        if len(cube_state) != 54:
            raise ValueError("Cube state must be a 54-long list of chars or string of colors")

        self.cube_state = np.fromstring(cube_state, dtype="|S1")

    def get_cube_state(self):
        return "".join(self.cube_state)

    def move_decoder(self, move_command):
        if isinstance(move_command, (list, np.ndarray)):
            for move_command_ in move_command:
                self.move_decoder(move_command_)
            return

        if not isinstance(move_command, str):
            raise ValueError("Move command should be a string")
        move_command = move_command.strip()

        if move_command not in self.move_map.keys():
            raise ValueError(f"Not a valid move_command: {move_command}")

        self.fundamental_move(move_command)
        
    def fundamental_move(self, move_command):
        if not isinstance(move_command, str):
            raise ValueError("Move command should be a string")

        move_command = move_command.strip()

        if len(move_command) == 0:
            return # I suppose a blank command is valid

        if move_command[0] not in "UFDLRB":
            raise ValueError(f"Move command should follow UFDLRB notation: {move_command[0]}")

        self.cube_state = self.cube_state[self.move_map[move_command]]

    def check_solved(self):
        return "".join(self.cube_state) == "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"

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
    cube.move_decoder("U")
    cube.plot()
    plt.show()
