""" Module that defines the Solver class """

import os.path
import numpy as np
from numpy import array, int16  # Needed for eval on loaded file


class Solver:
    """
    Solver class for the Rubik's Cube.

    Algorithmically solves the cube in steps.
    In each step, there is a dictionary with keys that
    represent each state the cube can be during this stage
    after being masked for the pieces being solved in that stage.
    The key's corresponding values are lists of moves needed to
    bring the cube in to the next stage.

    The most straight-forward approach is to solve for each
    piece iteratively, with 20 stages and each stage not having more
    than 24 possible cube states. The default solver uses this approach.

    Attributes
    ----------
    array_of_dict_solvers : array of dictionaries
        Array of the dictionaries used in each stage.
    cube : Cube object being solved.
    """

    def __init__(self, solver_file_name=None):
        """
        The constructor for the Solver class.

        Parameters
        ----------
        solver_file_name : str
            File name of where the array of dictionaries for solving the cube are saved.
            If "default", attempts to load the default solver in data/default_algorithm_solver.txt.
            Creates the default if doesn't exist.
            If None, initializes a blank array.
            Otherwise, attempts to load the designated solver file.
        """

        self.array_of_dict_solvers = []
        self.cube = None

        if solver_file_name is not None:
            if solver_file_name == "default":
                solver_file_name = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "data/default_algorithm_solver.txt",
                )

                # Check if the default file exists. If not, create it.
                if not os.path.isfile(solver_file_name):
                    # It is not typical to import functions mid-code.
                    # However, this is only used if the default solver doesn't already exist
                    # and importing here solves a cyclical import error.
                    from PyBiksCube.create_solution_algorithm import create_algorithm

                    create_algorithm(solver_file_name)
            else:
                # Check if the selected file exists. If not, throw error.
                if not os.path.isfile(solver_file_name):
                    raise ValueError(f"Filename given did not open: {solver_file_name}")

            try:
                with open(solver_file_name, "r", encoding="utf-8") as file:
                    self.array_of_dict_solvers = eval(file.read())
            except:
                raise ValueError(
                    "Something wrong happened with opening the algorithm file."
                )

    def solve_cube(self, cube, output_moves=False):
        """
        Solves the given cube using the algorithm that is already loaded into the class.

        Parameters
        ----------
        cube : cube object
            The cube to be solved. Is loaded into the class attribute cube.
        output_moves : bool
            Returns the moves used to solve.
        """

        self.cube = cube

        if output_moves:
            total_moves_to_solve = np.array([], dtype=np.int16)

        for i_solver_stage in range(len(self.array_of_dict_solvers)):
            moves_to_solve = self.find_moves_to_solve_stage(i_solver_stage)
            cube.move_decoder(moves_to_solve)

            if output_moves:
                total_moves_to_solve = np.append(total_moves_to_solve, moves_to_solve)

        self.cube = None

        if output_moves:
            return total_moves_to_solve

        return None

    def find_moves_to_solve_stage(self, i_solver_dict):
        """
        Helper function to find the moves to solve a single stage of the solver algorithm.

        Parameters
        ----------
        i_solver_dict : int
            Index of current stage being solved for.

        Returns
        -------
        moves_to_solve : array of integers
            The moves needed to solve this stage of the cube.
        """

        solver_dict = self.array_of_dict_solvers[i_solver_dict]
        end_stage = self.cube.get_raw_cube_state()

        for key in solver_dict:
            if self.cube.check_match_against_key(np.array(list(key), dtype=str)):
                return solver_dict[key]

        for key in solver_dict:
            key_cur = np.array(list(key), dtype=str)
            print(
                key,
                np.sum(np.logical_and(key_cur == end_stage, key_cur != "k")),
                np.sum(key_cur != "k"),
                "".join(end_stage),
            )

        raise ValueError(
            "Didn't find a solution. Is the cube busted? Or a solution is missing?"
        )
