""" Module that defines the Piece class. """

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import art3d

from PyBiksCube.utilities import side_type_converter


class Piece:
    """
    Representation of a one piece of a Rubik's Cube. Includes:

    - commands to load and unload the colors of the piece.
    - commands to perform rotate the cube following the UFDLRB notation
    - plotting script for debugging and visualization

    Attributes
    ----------
    colors : list of strings
        The color of each side, with map in self.side_to_index_map
    turn_sequences : dict of lists of strings
        Returns the names of the sides that are rotated along the axis (that is the key)
    side_to_index_map : dict of ints
        Returns the index of the side that corresponds to the face name
    """

    def __init__(self):
        """The constructor for the Piece class."""

        self.colors = np.array(["k", "k", "k", "k", "k", "k"])

        # The sides that are rotated when a turn is initiated on given face key
        self.turn_sequences = {
            "F": ["U", "R", "D", "L"],
            "B": ["U", "L", "D", "R"],
            "R": ["U", "B", "D", "F"],
            "L": ["U", "F", "D", "B"],
            "U": ["F", "L", "B", "R"],
            "D": ["F", "R", "B", "L"],
        }

        self.side_to_index_map = {"F": 0, "B": 2, "R": 1, "L": 3, "U": 5, "D": 4}

    def side_to_index(self, side):
        """
        Converts the side name to the index in the colors array.
        Function sanitizes the input and then uses the side_to_index_map dict.
        Can be used with a list for faster indexing.

        Parameters
        ----------
        side : str or list of strs
            Side or list of strings to find the indices of in the colors array.
        """

        converted_side = side_type_converter(side)

        if isinstance(converted_side, list):
            return [self.side_to_index(side_) for side_ in converted_side]

        if converted_side not in self.side_to_index_map:
            raise ValueError("side does not follow UFDLRB notation")

        return self.side_to_index_map[converted_side]

    def rotate(self, turn_axis, number_of_turns):
        """
        Rotate the piece along the turn_axis
        the number of turns in number_of_turns.
        Rotation can be flipped with a negative number_of_turns.

        Parameters
        ----------
        turn_axis : str
            Name of face to turn around.
        number_of_turns : int
            Integer of number of turns to turn about turn_axis.
            May be negative for opposite direction turn.
        """
        converted_turn_axis = side_type_converter(turn_axis)
        current_turn = self.turn_sequences[converted_turn_axis]
        sides_to_roll = self.side_to_index(current_turn)
        self.colors[sides_to_roll] = self.colors[
            np.roll(sides_to_roll, number_of_turns)
        ]

    def get_color(self, side):
        """
        Retrieve color on side of piece.

        Parameters
        ----------
        side : str
            Name of face to get color of.
        """
        converted_side = side_type_converter(side)
        return self.colors[self.side_to_index(converted_side)]

    def set_color(self, side, color):
        """
        Set color on side of piece.

        Parameters
        ----------
        side : str
            Name of face to put color on.
        color : str
            Name of color to put on. Should be a matplotlib-compatible color.
        """

        converted_side = side_type_converter(side)
        self.colors[self.side_to_index(converted_side)] = color

    def plot(self):
        """
        Create a 3D plot of the piece, for debugging purposes.
        """

        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        ax.set_aspect("equal")
        ax.set_autoscale_on(True)

        ax_limit = [-10, 10]
        ax.set_xlim(ax_limit)
        ax.set_ylim(ax_limit)
        ax.set_zlim(ax_limit)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        coord_system = [[2, "x"], [2, "y"], [-2, "x"], [-2, "y"], [-2, "z"], [2, "z"]]
        for i, (z, zdir) in enumerate(coord_system):
            side = Rectangle((-2, -2), 4, 4, facecolor=self.colors[i])
            ax.add_patch(side)
            art3d.pathpatch_2d_to_3d(side, z=z, zdir=zdir)
