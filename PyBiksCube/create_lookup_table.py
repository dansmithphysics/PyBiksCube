import os.path
import numpy as np
from PyBiksCube import Cube


def lookup_table_calculator_for_move(move):
    """
    Need to create look up tables for:
    - index to face + face position
    - indices used in rotations from start to end
    """

    cube = Cube()

    initial_cube_state = 'abcdefghijklmnopqrstuvwxyz[ABCDEFGHIJKLMNOPQRSTUVWXYZ]'    
    cube.set_cube_state(initial_cube_state)
    cube.move_decoder(move)
    final_cube_state = list(cube.get_cube_state())
    
    cur_map = np.empty(54, dtype=int)
    for i in range(54):
        cur_map[i] = initial_cube_state.index(final_cube_state[i])

    return cur_map


def create_lookup_table(output_file_name):
    fundamental_moves = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]
    
    move_array = np.empty((12, 54), dtype=np.int16)
    for i, move in enumerate(fundamental_moves):
        cur_map = lookup_table_calculator_for_move(move)
        move_array[i] = cur_map

    np.savetxt(output_file_name, move_array, fmt="%i", delimiter=",")
