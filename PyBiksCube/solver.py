import os.path
import numpy as np
from numpy import array, int16


class Solver:
    def __init__(self, solver_file_name=None):
        self.array_of_dict_solvers = []

        if solver_file_name is not None:
            if solver_file_name == "default":
                solver_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                "data/default_algorithm_solver.txt")

                # Check if the default file exists. If not, create it.
                if not os.path.isfile(solver_file_name):
                    from PyBiksCube.create_solution_algorithm import create_algorithm
                    create_algorithm(solver_file_name)
            else:
                # Check if the selected file exists. If not, throw error.
                if not os.path.isfile(solver_file_name):
                    raise ValueError(f"Filename given did not open: {solver_file_name}")
                
            try:
                with open(solver_file_name, 'r', encoding="utf-8") as file:
                    self.array_of_dict_solvers = eval(file.read())
            except:
                raise ValueError("Something wrong happened with opening the algorithm file.")

    def solve_cube(self, cube, output_moves=False):
        if output_moves:
            total_moves_to_solve = np.array([], dtype=np.int16)

        for solver_stage in self.array_of_dict_solvers:
            moves_to_solve = self.find_moves_to_solve_stage(cube, solver_stage)
            cube.move_decoder(moves_to_solve)

            if output_moves:
                total_moves_to_solve = np.append(total_moves_to_solve, moves_to_solve)

        if output_moves:
            return total_moves_to_solve

        return None

    def find_moves_to_solve_stage(self, cube, solver_dict):
        end_stage = cube.get_raw_cube_state()

        for key in solver_dict:
            if cube.check_match_against_key(np.array(list(key), dtype=str)):
                return solver_dict[key]

        for key in solver_dict:
            key_cur = np.array(list(key), dtype=str)
            print(key, np.sum(np.logical_and(key_cur == end_stage, key_cur != 'k')), np.sum(key_cur != 'k'))
            print("".join(end_stage))

        raise ValueError("Didn't find a solution. Is the cube busted? Or maybe a solution is missing?")
