""" An example script that creates a cube, scrambles it, and solves it again. """

import matplotlib.pyplot as plt
from PyBiksCube import CubeLookup, Solver


def example():
    """An example script that creates a cube, scrambles it, and solves it again."""

    # Initialize a cube.
    cube = CubeLookup()

    # Randomize the cube.
    cube.randomize()

    # Plot the scrambled cube.
    cube.plot()
    plt.title("Cube Before Solved")

    # Initialize a cube solver.
    solver = Solver("default")

    # Solve the cube using the solver
    solver.solve_cube(cube)

    # Plot the solved cube.
    cube.plot()
    plt.title("Cube After Solved")

    # Draw to screw the plots.
    plt.show()


if __name__ == "__main__":
    example()
