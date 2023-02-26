import pytest
import numpy as np
import numpy.testing as npt
from PyBiksCube import CubeLookup, Solver


@pytest.fixture
def cube():
    return CubeLookup()

@pytest.fixture
def solver():
    return Solver("default")

# This might be classified as an integration test!
@pytest.mark.parametrize("random_seed", list(range(1, 100)))
def test_random_solver(cube, solver, random_seed):
    # Assemble
    np.random.seed(random_seed)
    cube.randomize()

    # Act
    solver.solve_cube(cube)

    # Assert
    assert cube.check_solved()

@pytest.mark.parametrize("cube_state, expected_moves", [("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", [1]),
                                                        ("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm", [2])])
def test_moves_to_solve_stage(cube, solver, cube_state, expected_moves):
    # Arrange
    solver_dict = {"rkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk": [1],
                   "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm": [2]}
    solver.array_of_dict_solvers = [solver_dict]
    cube.set_cube_state(cube_state)
    solver.cube = cube
    
    # Act
    actual_moves = solver.find_moves_to_solve_stage(0)
    
    # Assert
    npt.assert_array_equal(actual_moves, expected_moves)
