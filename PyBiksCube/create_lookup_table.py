import numpy as np
from PyBiksCube import Cube


def calc_lookup_table_for_move(move):
    """
    Need to create look up tables for:
    - index to face + face position
    - indices used in rotations from start to end
    """

    cube = Cube()

    initial_cube_state = "abcdefghijklmnopqrstuvwxyz[ABCDEFGHIJKLMNOPQRSTUVWXYZ]"
    cube.set_cube_state(initial_cube_state)
    cube.move_decoder(move)
    final_cube_state = list(cube.get_cube_state())

    cur_map = np.array([initial_cube_state.index(state) for state in final_cube_state],
                       dtype=np.int16)

    return cur_map


def create_lookup_table(output_file_name):
    fundamental_moves = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]

    move_array = np.array([calc_lookup_table_for_move(move) for move in fundamental_moves],
                          dtype=np.int16)

    np.savetxt(output_file_name, move_array, fmt="%i", delimiter=",")
