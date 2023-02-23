from itertools import product
import numpy as np
from PyBiksCube import Cube
import matplotlib.pyplot as plt
import cProfile

def run_mc_samples():
    n_mc_cubes = 100000

    fundamental_moves = ["U", "F", "D", "L", "R", "B", "U'", "F'", "D'", "L'", "R'", "B'"]

    final_states = np.empty(n_mc_cubes, dtype="|S54")
    final_n_moves = np.empty(n_mc_cubes, dtype=int)
    final_moves = np.empty(n_mc_cubes, dtype=object)

    cube = Cube()
    
    for i_mc in range(n_mc_cubes):
        cube.set_cube_state("kkkkkkkkkkkkkkkykkmkkkkkkkkkkkkkkkkgkkkkkkkkkkkkkkkkkk")

        n_moves = np.random.randint(1, 4)

        mc_moves = np.random.choice(fundamental_moves, n_moves)

        cube.move_decoder(list(mc_moves))

    '''
        # The unsolved cube
        cube_state = cube.get_cube_state()

        # The steps needed to solve it
        mc_moves = np.flip(mc_moves)
        for i in range(len(mc_moves)):
            if "'" in mc_moves[i]:
                mc_moves[i] = mc_moves[i][0]
            else:
                mc_moves[i] += "'"
        
        final_states[i_mc] = cube_state
        final_n_moves[i_mc] = len(mc_moves)
        final_moves[i_mc] = mc_moves
        
    unique_final_states = np.unique(final_states)
    for i, unique_final_state in enumerate(unique_final_states):
        paths_of_interest = (final_states == unique_final_state)
        shortest_path_index = np.argmin(final_n_moves[paths_of_interest])
        print("%i) \t %s \t %i" % (i, unique_final_state, final_n_moves[paths_of_interest][shortest_path_index]), end=" ")
        print(final_moves[paths_of_interest][shortest_path_index])

    '''

if __name__ == "__main__":
    #cProfile.run("run_mc_samples()")
    run_mc_samples()
