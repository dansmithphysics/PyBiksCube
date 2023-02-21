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

    #remove_list = [
    
    cur_map = np.empty(54, dtype=int)
    for i in range(54):
        cur_map_ = initial_cube_state.index(final_cube_state[i])
        cur_map[i] = cur_map_

    return cur_map


def create_lookup_table(output_file_name):
    fundamental_moves = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]

    move_map = {}
    for move in fundamental_moves:
        cur_map = lookup_table_calculator_for_move(move)
        move_map[move] = list(cur_map)

    f = open(output_file_name, "w")
    f.write(str(move_map))
    f.close()

if __name__ == "__main__":

    create_lookup_table("./data/cube_lookup_table.txt")

    move_map = open('cube_lookup_table.txt', 'r').read()
    move_map = eval(move_map)
    
    # quickly check to make sure it is real
    cube = Cube()
    initial_cube_state = cube.get_cube_state()
    cube.move_decoder("U")
    final_cube_state = cube.get_cube_state()

    # open file for writing
    
    print(move_map)
    
    print(initial_cube_state)
    print(final_cube_state)

    # now, the look up table way:
    lookup_cube_state = initial_cube_state
    lookup_cube_state = np.array(list(lookup_cube_state))
    lookup_cube_state = lookup_cube_state[move_map["U"]]
    lookup_cube_state = "".join(lookup_cube_state)
    
    print(lookup_cube_state)
    
