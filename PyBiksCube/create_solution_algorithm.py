from itertools import product
import numpy as np
from PyBiksCube import CubeLookup
from PyBiksCube.utilities import convert_move_command
import matplotlib.pyplot as plt
import cProfile
from numba import jit
from operator import itemgetter


def run_mc_samples(n_mc_cubes=10000, stages=None):
    """ The idea is that we iteratively build this badboy up. """
    
    reverser_lookup_table_letters = {"U":"U'", "F":"F'", "D":"D'", "L":"L'", "R":"R'", "B":"B'", "U'":"U", "F'":"F", "D'":"D", "L'":"L", "R'":"R", "B'":"B"}
    reverser_lookup_table = {}
    for key in reverser_lookup_table_letters:
        reverser_lookup_table[convert_move_command(key)] = convert_move_command(reverser_lookup_table_letters[key])
    
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")

    if stages is None:
        stages = ["krkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkwkkkkkkk",
                  "krkrrkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkwkkkkkkk",
                  "krkrrkkrkkykkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkwkkkkkkk",
                  "krkrrrkrkkykkkkkkkkkkkkkkkkkgkkkkkkkkbkkkkkkkkwkkkkkkk",
                  "rrkrrrkrkkykkkkkkkkkkkkkkkkggkkkkkkkkbkkkkkkkkwwkkkkkk",
                  "rrrrrrkrkkykkkkkkkkkkkkkkkkggkkkkkkkkbbkkkkkkwwwkkkkkk",              
                  "rrrrrrrrkyykkkkkkkkkkkkkkkkgggkkkkkkkbbkkkkkkwwwkkkkkk",
                  "rrrrrrrrryyykkkkkkkkkkkkkkkgggkkkkkkbbbkkkkkkwwwkkkkkk",
                  "rrrrrrrrryyykkkkkkkkkkkkkkkgggggkkkkbbbkkkkkkwwwkwwkkk",
                  "rrrrrrrrryyykkkkkkkkkkkkkkkgggggkkkkbbbkbbkkkwwwwwwkkk",
                  "rrrrrrrrryyyyykkkkkkkkkkkkkggggggkkkbbbkbbkkkwwwwwwkkk",
                  "rrrrrrrrryyyyyykkkkkkkkkkkkggggggkkkbbbbbbkkkwwwwwwkkk",
                  "rrrrrrrrryyyyyykkkkkkkmkkmkggggggkkkbbbbbbkkkwwwwwwkwk",
                  "rrrrrrrrryyyyyykkkkkkmmkkmkggggggkgkbbbbbbkkkwwwwwwkwk",
                  "rrrrrrrrryyyyyykkkkkkmmmkmkggggggkgkbbbbbbkbkwwwwwwkwk",
                  "rrrrrrrrryyyyyykykkmkmmmkmkggggggkgkbbbbbbkbkwwwwwwkwk",
                  "rrrrrrrrryyyyyykykkmkmmmmmkggggggggkbbbbbbkbkwwwwwwkww",
                  "rrrrrrrrryyyyyykykkmkmmmmmmggggggggkbbbbbbkbbwwwwwwwww",
                  "rrrrrrrrryyyyyyyykmmkmmmmmmgggggggggbbbbbbkbbwwwwwwwww",
                  "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"]

    array_of_dict_solvers = [{} for i in range(len(stages))]    
    for i_stage, stage in enumerate(stages):
        
        dict_solver = {}
        
        for i_mc in range(n_mc_cubes):
            
            cube.set_cube_state(stage)
            if i_mc == 0:
                n_moves = 0 # the null case is often possible so must remain on the table
            else:
                n_moves = np.random.randint(1, 10)

            mc_moves = cube.randomize(n_moves)

            for i_stage_correction in np.arange(0, i_stage):
                moves_to_solve = find_moves_to_solve_stage(cube, array_of_dict_solvers[i_stage_correction])
                cube.move_decoder(moves_to_solve)
                mc_moves = np.append(mc_moves, moves_to_solve)

            # The unsolved cube
            cube_state = cube.get_cube_state()

            save_path = False
            if cube_state not in dict_solver:
                save_path = True
            else:
                if len(mc_moves) < len(dict_solver[cube_state]):
                    save_path = True

            if save_path:
                # The steps needed to solve it are the reverse of what made it
                mc_moves = np.flip(mc_moves)
                for i in range(len(mc_moves)):
                    mc_moves[i] = reverser_lookup_table[mc_moves[i]]
                dict_solver[cube_state] = mc_moves
                
        print("Number of unique states: %i" % len(dict_solver))
        
        for i, key in enumerate(dict_solver):
            print("%i) \t %s \t %i" % (i, key, len(dict_solver[key])), end=" ")
            print(dict_solver[key])
            
        array_of_dict_solvers[i_stage] = dict_solver


    return array_of_dict_solvers

def find_moves_to_solve_stage(cube, solver_dict):
    end_stage = cube.get_raw_cube_state()
    
    for key in solver_dict:
        if cube.check_match_against_key(make_list(key)):
            return solver_dict[key]

    for key in solver_dict:
        key_cur = make_list(key)
        print(key, np.sum(np.logical_and(key_cur == end_stage, map_key != 'k')), np.sum(key_cur != 'k'))
        print("".join(end_stage))
        
    raise ValueError("Didn't find a solution. Is the cube busted? Or maybe a solution is missing?")


@jit(nopython=True)
def find_moves_to_solve_stage_jit(end_stage, solver_dict_keys):

    for key_cur in solver_dict_keys:
        number_of_colors = 0
        for i in np.arange(len(key_cur)):
            if key_cur[i] != b'k':
                number_of_colors += 1

        number_on_actual = 0
        for i in np.arange(len(key_cur)):
            if key_cur[i] == end_stage[i] and key_cur[i] != b'k':
                number_on_actual += 1

        if number_on_actual == number_of_colors:
            return key_cur

    print(end_stage)
    #print("".join(key_cur.astype('str')), "".join(end_stage.astype('str')), np.sum(key_cur == end_stage), np.sum(key_cur != b'k'))
    raise ValueError("Didn't find a solution. Is the cube busted?")


if __name__ == "__main__":
    # Actually really need to add the "Do nothing" command! Could that be it? It is confused when it is in the correct place? But the R R' trick should solve it?
    #cProfile.run("run_mc_samples()")

    array_of_dict_solvers = run_mc_samples()

    f = open("algorithm_solver", "w")
    f.write(str(array_of_dict_solvers))
    f.close()

    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")
    
    # Lets try to make a single converter
    cube.set_cube_state("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww")
    mc_moves = cube.randomize()

    cube.plot()
    plt.title("Before")
    
    # Before finding the unique end states, I solve for the pieces before this stage:
    try:
        for i_stage_correction, stage in enumerate(array_of_dict_solvers):
            print(i_stage_correction)        
            moves_to_solve = find_moves_to_solve_stage(cube, array_of_dict_solvers[i_stage_correction])
            print(moves_to_solve)
            cube.move_decoder(moves_to_solve)
    except:
        print("Failed on", i_stage_correction)
        print(stage)
        print(cube.get_raw_cube_state())
        cube.plot()
        plt.title("After")
        plt.show()

    cube.plot()
    plt.title("After")
    plt.show()

    
    '''
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")
    cube.set_cube_state("rkkwkkkkkkkkkkkkkkkkkkkkkkkgrkkkkkkkkkkkkkkkkkkwkkkkkk")
    cube.plot()
    
    cube.set_cube_state("rbbwrrbbryygyygyywmmrmmgmmmgrrggrgggybyybbbrbmmwwwwwww")
    cube.plot()

    fundamental_moves_letters = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]

    for move in [2, 3, 3]:
        letter_move = fundamental_moves_letters[move]
        print(letter_move)
        
    cube.move_decoder([2, 3, 3])
    cube.plot()
    
    plt.show()
    
    #run_mc_samples()
    '''
