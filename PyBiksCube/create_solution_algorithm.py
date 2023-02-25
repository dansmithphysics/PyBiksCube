from itertools import product
import numpy as np
from PyBiksCube import CubeLookup, Solver
from PyBiksCube.utilities import convert_move_command
import matplotlib.pyplot as plt
import cProfile
from numba import jit
from operator import itemgetter
from numpy import array, int16

def run_mc_samples(n_mc_cubes=10000, stages=None):
    """ The idea is that we iteratively build this badboy up. """
    
    reverser_lookup_table_letters = {"U":"U'", "F":"F'", "D":"D'", "L":"L'", "R":"R'", "B":"B'", "U'":"U", "F'":"F", "D'":"D", "L'":"L", "R'":"R", "B'":"B"}
    reverser_lookup_table = {}
    for key in reverser_lookup_table_letters:
        reverser_lookup_table[convert_move_command(key)] = convert_move_command(reverser_lookup_table_letters[key])
    
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")

    solver = Solver()
    
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

        # Start with the empty set, in case this stage can be skipped
        dict_solver = {stage: np.array([], dtype=np.int16)}
        
        for i_mc in range(n_mc_cubes):
            
            cube.set_cube_state(stage)
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


def make_list(list_to_convert):
    return np.array(list(list_to_convert), dtype=str)


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


if __name__ == "__main__":
    '''
    array_of_dict_solvers = run_mc_samples(100000)

    f = open("algorithm_solver_.txt", "w")
    f.write(str(array_of_dict_solvers))
    f.close()
    '''

    solver = Solver("algorithm_solver.txt")

    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")    
    cube.randomize()

    cube.plot()
    plt.title("Before")

    solver.solve_cube(cube)
    
    cube.plot()
    plt.title("After")
    plt.show()
