from itertools import product
import numpy as np
from PyBiksCube import CubeLookup
from PyBiksCube.utilities import convert_move_command
import matplotlib.pyplot as plt
import cProfile
from numba import jit

def run_mc_samples():
    n_mc_cubes = 100000

    fundamental_moves_letters = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]
    fundamental_moves = np.arange(12).astype(np.int16)
    
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")

    # lets see how many errors are in there!
    '''
    stages = ["rkkkkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkkkwkkkkkk",
              "rrkkkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkkwwkkkkkk",
              "rrrkkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkbkkkkkkwwwkkkkkk",
              "rrrrrkkkkkkkkkkkkkkkkkkkkkkggkkkkkkkkkbkkkkkkwwwkkkkkk",
              "rrrrrrkkkkkkkkkkkkkkkkkkkkkggkkkkkkkkbbkkkkkkwwwkkkkkk",
              "rrrrrrrkkykkkkkkkkkkkkkkkkkgggkkkkkkkbbkkkkkkwwwkkkkkk",
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
    '''
    
    #stages = ["krkrrkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkwkkkkkkk", # First half of cross
    #          "krkrrrkrkkykkkkkkkkkkkkkkkkkgkkkkkkkkbkkkkkkkkwkkkkkkk", # Cross on top
    #          "rrrrrrrrryyykkkkkkkkkkkkkkkgggkkkkkkbbbkkkkkkwwwkkkkkk", # Full top
    #          "rrrrrrrrryyyyyykkkkkkkkkkkkggggggkkkbbbbbbkkkwwwwwwkkk", # The next layer
    #          "rrrrrrrrryyyyyykykkmkmmmkmkggggggkgkbbbbbbkbkwwwwwwkwk", # Cross on bottom
    #          "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"] # Rest of the owl
    '''
    stages = ["krkrrkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkwkkkkkkk", # First half of cross              
              "rrrrrkkkkkkkkkkkkkkkkkkkkkkggkkkkkkkkkbkkkkkkwwwkkkkkk",
              "rrrrrrkkkkkkkkkkkkkkkkkkkkkggkkkkkkkkbbkkkkkkwwwkkkkkk",
              "rrrrrrrkkykkkkkkkkkkkkkkkkkgggkkkkkkkbbkkkkkkwwwkkkkkk",
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
    '''

    stages = ["krkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkwkkkkkkk",
              "krkrrkkkkkkkkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkwkkkkkkk",
              "krkrrkkrkkykkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkwkkkkkkk",
              "krkrrrkrkkykkkkkkkkkkkkkkkkkgkkkkkkkkbkkkkkkkkwkkkkkkk",
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
    
    
    # The idea is that we iteratively build this badboy up.
    
    solver_array_of_dicts = [{} for i in range(len(stages))]
    
    for i_stage, stage in enumerate(stages):
        final_states = np.empty(n_mc_cubes, dtype="|S54")
        final_n_moves = np.empty(n_mc_cubes, dtype=int)
        final_moves = np.empty(n_mc_cubes, dtype=object)
        final_consider = np.zeros(n_mc_cubes).astype(bool)
        
        for i_mc in range(n_mc_cubes):

            cube.set_cube_state(stage)
        
            n_moves = np.random.randint(1, 20)
            mc_moves = np.random.choice(fundamental_moves, n_moves)

            cube.move_decoder(mc_moves)

            # Before finding the unique end states, I solve for the pieces before this stage:
            for i_stage_correction in np.arange(0, i_stage):# , -1, -1):
                #print("Correction on: ", i_stage_correction)
                #moves_to_solve = find_moves_to_solve_stage(cube, solver_array_of_dicts[i_stage_correction])

                end_stage = cube.get_cube_state()
                end_stage = np.frombuffer(str.encode(end_stage), dtype="|S1", count=54)
                solver_dict_keys = list(solver_array_of_dicts[i_stage_correction].keys())
                solver_dict_keys_ = np.empty((len(solver_dict_keys), 54), dtype="|S1")
                for i in range(len(solver_dict_keys_)):
                    solver_dict_keys_[i] = np.frombuffer(solver_dict_keys[i], dtype="|S1", count=54)
                moves_to_solve_key = find_moves_to_solve_stage_jit(end_stage, solver_dict_keys_)
                # And now, convert again
                moves_to_solve_key = "".join(moves_to_solve_key.astype('str'))
                moves_to_solve_key = moves_to_solve_key.encode()
                
                moves_to_solve = solver_array_of_dicts[i_stage_correction][moves_to_solve_key]
                cube.move_decoder(moves_to_solve)
                #mc_moves = np.append(mc_moves, moves_to_solve)

            # New approach:
            # to be a canidate, it has to not have modified previous stages pieces before moving forward
            # so basically
            # This isn't working perfectly, seems like some solutions aren't making it. 
            if i_stage > 0:
                end_stage = cube.get_cube_state()
                end_stage = np.frombuffer(str.encode(end_stage), dtype="|S1", count=54)

                key = str.encode(stages[i_stage-1])
                key_cur = np.frombuffer(key, dtype="|S1", count=54)
                
                if np.sum(np.logical_and(key_cur == end_stage, key_cur != b'k')) != np.sum(key_cur != b'k'):
                    continue # reject this solution if it messes with the pieces in place
                
            # The unsolved cube
            cube_state = cube.get_cube_state()
            
            # The steps needed to solve it
            mc_moves = np.flip(mc_moves)
            for i in range(len(mc_moves)):
                letter_move = fundamental_moves_letters[mc_moves[i]]
                if "'" in letter_move:
                    mc_moves[i] = convert_move_command(letter_move[0])
                else:
                    mc_moves[i] = convert_move_command(letter_move + "'")

            final_consider[i_mc] = True
            final_states[i_mc] = cube_state
            final_n_moves[i_mc] = len(mc_moves)
            final_moves[i_mc] = mc_moves
        
        unique_final_states = np.unique(final_states[final_consider])
        print("Number of unique states: %i" % len(unique_final_states))
        
        dict_solver = {}

        for i, unique_final_state in enumerate(unique_final_states):
            paths_of_interest = (final_states == unique_final_state)
            shortest_path_index = np.argmin(final_n_moves[paths_of_interest])
            print("%i) \t %s \t %i" % (i, unique_final_state, final_n_moves[paths_of_interest][shortest_path_index]), end=" ")
            print(final_moves[paths_of_interest][shortest_path_index])
            dict_solver[unique_final_state] = final_moves[paths_of_interest][shortest_path_index]        

        solver_array_of_dicts[i_stage] = dict_solver

        if i_stage == 2:
            break
            
    # Lets try to make a single converter
    cube.set_cube_state("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww")
    n_moves = np.random.randint(5, 10)
    mc_moves = np.random.choice(fundamental_moves, n_moves)
    cube.move_decoder(mc_moves)

    cube.plot()
    plt.title("Before")
    
    # Before finding the unique end states, I solve for the pieces before this stage:
    for i_stage_correction in np.arange(3): #len(stages)):
        #print("Correction on: ", i_stage_correction)
        print(i_stage_correction)
        end_stage = cube.get_cube_state()
        end_stage = np.frombuffer(str.encode(end_stage), dtype="|S1", count=54)
        solver_dict_keys = list(solver_array_of_dicts[i_stage_correction].keys())
        solver_dict_keys_ = np.empty((len(solver_dict_keys), 54), dtype="|S1")
        for i in range(len(solver_dict_keys_)):
            solver_dict_keys_[i] = np.frombuffer(solver_dict_keys[i], dtype="|S1", count=54)
        moves_to_solve_key = find_moves_to_solve_stage_jit(end_stage, solver_dict_keys_)
        # And now, convert again
        moves_to_solve_key = "".join(moves_to_solve_key.astype('str'))
        moves_to_solve_key = moves_to_solve_key.encode()
        
        moves_to_solve = solver_array_of_dicts[i_stage_correction][moves_to_solve_key]

        #moves_to_solve = find_moves_to_solve_stage(cube, solver_array_of_dicts[i_stage_correction])
        print(moves_to_solve)
        cube.move_decoder(moves_to_solve)
    
    #print(end_stage)
    #print(dict_solver)
    
    cube.plot()
    plt.title("After")

    plt.show()
    

def find_moves_to_solve_stage(cube, solver_dict):
    end_stage = cube.get_cube_state()
    end_stage = np.frombuffer(str.encode(end_stage), dtype="|S1", count=54)

    for key in solver_dict:
        key_cur = np.frombuffer(key, dtype="|S1", count=54)
        #print("".join(key_cur.astype('str')), "".join(end_stage.astype('str')), np.sum(key_cur == end_stage) - np.sum(end_stage == b'k'), np.sum(key_cur != b'k'))
        # Yeah, this matching logic is broken, sadly
        # it isn't good enough!
        # Will have to figure out how blank out all 
        if np.sum(np.logical_and(key_cur == end_stage, key_cur != b'k')) == np.sum(key_cur != b'k'):
            return solver_dict[key]

    for key in solver_dict:        
        print("".join(key_cur.astype('str')), np.sum(key_cur == end_stage), np.sum(key_cur != b'k'))
        print("".join(end_stage.astype('str')))
    raise ValueError("Didn't find a solution. Is the cube busted?")

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
    run_mc_samples()

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
