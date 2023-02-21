""" This module defines the Cube class. """

from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from PyBiksCube.utilities import side_type_converter
from PyBiksCube import Piece


class Cube:
    """
    Representation of a Rubik's Cube. Includes:

    - commands to load and unload the cube state into a 54 character long string.
    - commands to perform moves on the cube following the UFDLRB notation
    - command to check if the cube is solved
    - plotting script for debugging and visualization

    Attributes
    ----------
    pieces : 3D list of Pieces objects
    face_to_index_map : dict to convert faces to 3d pieces indices
    cube_state_map : dict to convert flat index to 3d pieces and face
    """

    def __init__(self, cube_state=None, randomize=False):
        """
        The constructor for the Cube class.
        
        Parameters
        ----------
        cube_state : str
            Load the cube faces from a 54 character long string.
            Default of None loads the solved cube.
        randomize : bool
            Randomize the cube via a random number of 
            fundamental movements.
            Default to False.
        """

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
        """
        Randomizes the cube state by applying 
        n_moves number of random moves on cube.

        Parameters
        ----------
        n_moves : int
            Number of random moves to move.
        """
        fundamental_moves = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]
        move_commands = np.random.choice(fundamental_moves, n_moves)
        for move_command in move_commands:
            self.fundamental_move(move_command)

    def set_cube_state(self, cube_state):
        """
        Sets cube face colors based on the
        cube_state, a 54 long string.

        Parameters
        ----------
        cube_state : str
            String of 54 characters for color of different faces.
            Order matches self.cube_state_map
        """

        if len(cube_state) != 54:
            raise ValueError("Cube state must be a 54-long list of chars or string of colors")

        for i_color, color in enumerate(cube_state):
            i_position, face = self.cube_state_map[i_color]
            self.pieces[i_position].set_color(face, color)

    def get_cube_state(self):
        """
        Returns cube face colors based on a 54 long string.

        Returns
        -------
        cube_state : str
            String of 54 characters for color of different faces.
            Order matches self.cube_state_map.
        """

        # Do the opposite of set_cube_state, output the state string
        cube_state = np.empty(54, dtype='str')
        for i in np.arange(54):
            i_position, face = self.cube_state_map[i]
            cube_state[i] = self.pieces[i_position].get_color(face)
        return ''.join(cube_state)

    def set_face_color(self, face, color):
        """
        Sets all faces on side with color.        

        Parameters
        ----------
        face : str
            Face to color in, following either xyz or FBRLUD
        color : str
            Color to fill in face. Should be a matplotlib color.
        """

        converted_face = side_type_converter(face)

        for i_position in self.face_to_index_map[converted_face]:
            self.pieces[i_position].set_color(converted_face, color)

    def get_face_colors(self, face):
        """
        Gets color of all faces on side.

        Parameters
        ----------
        face : str
            Face to color retrieve colors for, following either xyz or FBRLUD

        Returns
        -------
        colors_flat : list of str
            List of strings of all 9 face colors on a side.
        """

        converted_face = side_type_converter(face)

        colors_flat = np.empty(9, dtype='str')
        for i_flat, i_position in enumerate(self.face_to_index_map[converted_face]):
            colors_flat[i_flat] = self.pieces[i_position].get_color(converted_face)

        return colors_flat

    def print_face(self, face):
        """
        Prints and gets color of all faces on side.

        Parameters
        ----------
        face : str
            Face to color retrieve colors for, following either xyz or FBRLUD
        """

        converted_face = side_type_converter(face)
        print(face, end=" ")
        for i_position in self.face_to_index_map[converted_face]:
            print(i_position, end=", ")
            print(self.pieces[i_position].get_color(face), end = " | ")
        print(" ")
        print(self.get_face_colors(converted_face).reshape((3, 3)))
        print(" ")

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

        faces = self.face_to_index_map.keys()
        for face in faces:
            if len(np.unique(self.get_face_colors(face))) != 1:
                return False
        return True

    def move_decoder(self, move_command):
        """ 
        Decodes move command, decomposing more complicated moves
        into their fundamental movement components that are
        then executed.
        Currently, only complicated moves implemented are
        the double moves U2, D2, R2, L2, F2, and B2

        Parameters
        ----------
        move_command : str
            Move command to perform.
        """

        if isinstance(move_command, list):
            for move_command_ in move_command:
                self.move_decoder(move_command_)

        if not isinstance(move_command, str):
            raise ValueError("Move command should be a string")
        move_command = move_command.strip()

        fundamental_moves = ["", "U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]
        double_moves = ["U2", "D2", "R2", "L2", "F2", "B2"]
        #wide_moves = ["u", "d", "r", "l", "f", "b"]
        #coordinate_moves = ['x', 'y', 'z']

        valid_moves = fundamental_moves + double_moves
        if move_command not in valid_moves:
            raise ValueError("Not a valid move_command: {move_command}")

        if move_command in fundamental_moves:
            self.fundamental_move(move_command)
        elif move_command in double_moves:
            single_move = move_command[0]
            self.fundamental_move(single_move)
            self.fundamental_move(single_move)

    def fundamental_move(self, move_command):
        """ 
        Executes fundamental movements.
        The fundamental movements are U, D, R, L, F, B
        and U', D', R', L', F', B'

        Parameters
        ----------
        move_command : str
            Move command to perform.
        """

        if not isinstance(move_command, str):
            raise ValueError("Move command should be a string")

        move_command = move_command.strip()

        if len(move_command) == 0:
            return # I suppose a blank command is valid

        if len(move_command) == 1:
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
        slice_of_pieces = [self.pieces[i_position] for i_position
                           in self.face_to_index_map[move_command]]
        slice_of_pieces = np.array(slice_of_pieces, dtype=object)
        slice_of_pieces = slice_of_pieces.reshape((3, 3))
        slice_of_pieces = np.rot90(slice_of_pieces, handedness_correction * direction)
        for i_flattened, i_position in enumerate(self.face_to_index_map[move_command]):
            self.pieces[i_position] = slice_of_pieces.flatten()[i_flattened]
            self.pieces[i_position].rotate(move_command, direction)

    def plot(self):
        """ 
        Creates a matplotlib plot of the cube
        layed out in a cross.
        Great for debugging.
        """

        _, ax = plt.subplots(figsize=(12, 9))

        for i_position in self.face_to_index_map['F']:
            x_pos = i_position[1]
            y_pos = i_position[2]
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor='black',
                             facecolor=self.pieces[i_position].get_color('F'))
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i_position)
        for i_position in self.face_to_index_map['R']:
            x_pos = 3 + (2 -i_position[0])
            y_pos = i_position[2]
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor='black',
                             facecolor=self.pieces[i_position].get_color('R'))
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i_position)
        for i_position in self.face_to_index_map['L']:
            x_pos = -3+i_position[0]
            y_pos = i_position[2]
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor='black',
                             facecolor=self.pieces[i_position].get_color('L'))
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i_position)
        for i_position in self.face_to_index_map['B']:
            x_pos = 6 + (2-i_position[1])
            y_pos = i_position[2]
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor='black',
                             facecolor=self.pieces[i_position].get_color('B'))
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i_position)
        for i_position in self.face_to_index_map['U']:
            x_pos = i_position[1]
            y_pos = 5-i_position[0]
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor='black',
                             facecolor=self.pieces[i_position].get_color('U'))
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i_position)
        for i_position in self.face_to_index_map['D']:
            x_pos = i_position[1]
            y_pos = i_position[0]-3
            rect = Rectangle((x_pos, y_pos), 1, 1,
                             edgecolor='black',
                             facecolor=self.pieces[i_position].get_color('D'))
            ax.add_patch(rect)
            ax.text(x_pos + 0.1, y_pos + 0.1, i_position)

        ax.set_xlim(-3, 9)
        ax.set_ylim(-3, 6)


if __name__ == "__main__":
    # UFDLRB
    cube = Cube()
    cube.move_decoder("U2")
    cube.plot()
    plt.show()
