""" Module that creates the lookup table used for moves in the CubeLookup class """
import numpy as np
from PyBiksCube import Cube


def create_lookup_table(output_file_name):
    """
    Creates the lookup tables for moves in a lookup table based Cube class.

    The lookup table is a map of indices used in rotations from before to after the move.

    Works by:
    1) Loading up the Cube class, which uses an object oriented approach for
    simulating the cube, with unique colors on each face.
    2) Apply move to the cube
    3) Find the new indices of each face after the move
    4) Collect all fundamdental moves and their index maps into a 2D array
    5) Save array to output_file_name

    Parameters
    ----------
    output_file_name : str
        Name of output csv file.
    """

    fundamental_moves = [
        "U",
        "F",
        "D",
        "L",
        "R",
        "B",
        "U'",
        "F'",
        "D'",
        "L'",
        "R'",
        "B'",
    ]

    move_array = np.array(
        [calc_lookup_table_for_move(move) for move in fundamental_moves], dtype=np.int16
    )

    np.savetxt(output_file_name, move_array, fmt="%i", delimiter=",")


def calc_lookup_table_for_move(move):
    """
    Calculate the indices needed for a single move.

    Parameters
    ----------
    move : str
        Move to perform on the cube, in UFDLRB notation.

    Returns
    -------
    cur_map : array of ints
        Indices corresponding to the move requested. Length of 54 elements.
    """

    cube = Cube()

    initial_cube_state = "abcdefghijklmnopqrstuvwxyz[ABCDEFGHIJKLMNOPQRSTUVWXYZ]"
    cube.set_cube_state(initial_cube_state)
    cube.move_decoder(move)
    final_cube_state = list(cube.get_cube_state())

    cur_map = np.array(
        [initial_cube_state.index(state) for state in final_cube_state], dtype=np.int16
    )

    return cur_map
