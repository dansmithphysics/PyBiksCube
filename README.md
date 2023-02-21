# PyBikCube
My take on Rubik's Cube code in python.

So far, I am not happiest with the implementation but it passes the unit tests.
The cube is a 3x3x3 array of Pieces objects.

Moves are rotates of the pieces in the array + rotation of the pieces.

It isn't the most efficient since some of the pieces don't move, especially the center of the cube.

Perhaps, as I keep working, I will find a more efficient implementation.