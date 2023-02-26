""" This module defines the Cube class based on look up tables """

import os.path
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

    def __init__(self, lookup_table_file_name=None, cube_state=None):
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

        if lookup_table_file_name is None:
            lookup_table_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                  "data/default_cube_lookup_table.txt")

            # Check if the default file exists. If not, create it.
            if not os.path.isfile(lookup_table_file_name):
                # It is not typical to import functions mid-code.
                # However, this is only used if the default table doesn't already exist
                # and importing here solves a cyclical import error.
                from PyBiksCube.create_lookup_table import create_lookup_table
                create_lookup_table(lookup_table_file_name)
        else:
            # Check if the selected file exists. If not, throw error.
            if not os.path.isfile(lookup_table_file_name):
                raise ValueError(f"Filename given did not open: {lookup_table_file_name}")

        try:
            self.move_array = np.loadtxt(lookup_table_file_name, delimiter=",", dtype=np.int16)
        except:
            raise ValueError("Something wrong happened with opening the lookup table.")

    def set_cube_state(self, cube_state_):
        """
        Sets cube face colors based on the
        cube_state, a 54 long string.

        Parameters
        ----------
        cube_state : str
            String of 54 characters for color of different faces.
            Order matches self.cube_state_map
        """

        self.cube_state = np.array(list(cube_state_), dtype=str)

    def get_cube_state(self):
        """
        Returns cube face colors based on a 54 long string.

        Returns
        -------
        cube_state : str
            String of 54 characters for color of different faces.
            Order matches self.cube_state_map.
        """

        return "".join(self.cube_state)

    def get_raw_cube_state(self):
        """
        Returns the raw cube face colors based on an array of 54 strings.

        Returns
        -------
        cube_state : array of str
            Array of 54 strings for color of different faces.
            Order matches self.cube_state_map.
        """

        return self.cube_state

    def move_decoder(self, move_command):
        """ 
        Decodes move command, decomposing more complicated moves
        into their fundamental movement components that are
        then executed.

        The notation must be the corresponding integer for each move.
        The mapping, as defined in create_lookup_table, is:
        U:0, F:1, D:2, L:3, R:4, B:5, U':6, F':7, D':8, L':9, R':10, B':11

        Parameters
        ----------
        move_command : str
            Move command to perform.
        """

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
        """ 
        Executes fundamental movements.
        The fundamental movements are U, D, R, L, F, B
        and U', D', R', L', F', B'
        The notation must be the corresponding integer for each move.
        The mapping, as defined in create_lookup_table, is:
        U:0, F:1, D:2, L:3, R:4, B:5, U':6, F':7, D':8, L':9, R':10, B':11

        Parameters
        ----------
        move_command : str
            Move command to perform.
        """

        self.cube_state = self.cube_state[self.move_array[move_command]]

    def randomize(self, n_moves=None):
        """
        Randomizes the cube state by applying 
        n_moves number of random moves on cube.

        Parameters
        ----------
        n_moves : int
            Number of random moves to move.
            Default of None randomly selects an number from 1 to 30.
        """

        if n_moves is None:
            n_moves = np.random.randint(1, 30)
        mc_moves = np.random.choice(np.arange(12, dtype=np.int16), n_moves)
        self.move_decoder(mc_moves)
        return mc_moves

    def set_default_cube_state(self):
        """
        Sets cube state to default Rubik's cube given.
        The red face on top and yellow face on front.
        """

        self.set_cube_state("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww")

    def check_solved(self):
        """ 
        Checks whether the cube is solved.
        Perhaps this can be sped up by only looking at
        the minimum needed, but looking at the full cube for now.

        Returns
        -------
        solved : bool
            Boolean of whether or not the cube is solved.
        """

        return self.get_cube_state() == "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"

    def check_match_against_key(self, key):
        """
        Checks if the cube state matches the key (mask) given.
        The key can have blank spots, designated with the letter 'k',
        which are not used in the match calculation.

        Function is used for the Solver class to find which
        moves to apply to the cube based on a key (mask).

        Parameters
        ----------
        key : array of str
            Array of strings, length of 54, corresponding to the faces of the cube.

        Returns
        -------
        match : bool
            Boolean of whether or not the key matches the cube.
        """
        converted_key = np.array(list(key), dtype=str)
        count_matches = np.sum(np.logical_and(converted_key == self.cube_state,
                                              converted_key != 'k'))
        counts_expected = np.sum(converted_key != 'k')
        return count_matches == counts_expected

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
