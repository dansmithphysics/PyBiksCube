"""
PyBiksCube
==========

My take at a Rubik's Cube representation and solver.

Provides:
    1. Two representations of a Rubik's Cube, one object oriented (Cube) and 
        the other optimized for speed (CubeLookup)
    2. Solver class for solving the two Cube classes
    3. Helper function to create algorithms to solve the cube via the Solver class

The package includes an example script (PyBiksCube/example.py) that
shows the creation of a Cube, scrambling, solving, and plotting.

The lookup tables and solving algorithm are produced on the fly if they
do not already exist inside of the PyBiksCube/data directory. They are 
saved as text files.

Includes a PyTest suit, in the tests directory.
"""
__version__ = "0.1.0"
from .piece import Piece
from .cube import Cube
from .cube_lookup import CubeLookup
from .solver import Solver
