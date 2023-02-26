import numpy as np
import matplotlib.pyplot as plt
from PyBiksCube import CubeLookup, Solver


def run_mc_samples(n_mc_cubes=10000, stages=None, verbose=False):
    """ The idea is that we iteratively build this badboy up. """

    # Turns clockwise turns to counterclockwise
    reverser_lookup_table = {0: 6, 1: 7, 2: 8, 3: 9, 4: 10, 5: 11,
                             6: 0, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5}

    cube = CubeLookup()
    solver = Solver()

    # Default Stages
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
            n_moves = int(np.ceil(10.0 * (i_mc + 1.0) / n_mc_cubes))
            mc_moves = cube.randomize(n_moves)

            solver.array_of_dict_solvers = array_of_dict_solvers[0:i_stage]
            moves_to_solve_to_prev_stage = solver.solve_cube(cube, True)
            mc_moves = np.append(mc_moves, moves_to_solve_to_prev_stage)

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
                mc_moves = [reverser_lookup_table[mc_move] for mc_move in mc_moves]
                dict_solver[cube_state] = mc_moves

        if verbose:
            print(f"Number of unique states: {len(dict_solver)}")
            for i, key in enumerate(dict_solver):
                print(f"{i}) \t {key} \t {len(dict_solver[key])} \t {dict_solver[key]}")

        array_of_dict_solvers[i_stage] = dict_solver

    return array_of_dict_solvers


def create_algorithm(output_file_name, n_mc_cubes=10000, verbose=False, stages=None):
    array_of_dict_solvers = run_mc_samples(n_mc_cubes, verbose=True, stages=None)

    with open(output_file_name, "w", encoding="utf-8") as f:
        f.write(str(array_of_dict_solvers))

    
if __name__ == "__main__":




    

    #solver = Solver("algorithm_solver.txt")
    solver = Solver("algorithm_solver_.txt")

    cube = CubeLookup()
    cube.randomize()

    cube.plot()
    plt.title("Before")

    solver.solve_cube(cube)

    cube.plot()
    plt.title("After")
    plt.show()
