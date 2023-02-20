import pytest
from PyBiksCube import Piece


@pytest.mark.parametrize("initial_face, turn_face, arrive_face, number_of_turns, expected_color",
                         [('F', 'F', 'F', 1, 'g'),
                          ('F', 'U', 'L', 1, 'g'),
                          ('F', 'D', 'R', 1, 'g'),
                          ('F', 'R', 'U', 1, 'g'),
                          ('F', 'L', 'D', 1, 'g'),
                          ('F', 'B', 'F', 1, 'g'),
                          ('U', 'F', 'R', 1, 'g'),
                          ('U', 'U', 'U', 1, 'g'),
                          ('U', 'D', 'U', 1, 'g'),
                          ('U', 'R', 'B', 1, 'g'),
                          ('U', 'L', 'F', 1, 'g'),
                          ('U', 'B', 'L', 1, 'g'),
                          ('F', 'F', 'F', 2, 'g'),
                          ('F', 'U', 'B', 2, 'g'),
                          ('F', 'D', 'B', 2, 'g'),
                          ('F', 'R', 'B', 2, 'g'),
                          ('F', 'L', 'B', 2, 'g'),
                          ('F', 'B', 'F', 2, 'g'),
                          ('U', 'F', 'D', 2, 'g'),
                          ('U', 'U', 'U', 2, 'g'),
                          ('U', 'D', 'U', 2, 'g'),
                          ('U', 'R', 'D', 2, 'g'),
                          ('U', 'L', 'D', 2, 'g'),
                          ('U', 'B', 'D', 2, 'g'),
                          ('F', 'F', 'F', -1, 'g'),
                          ('F', 'U', 'R', -1, 'g'),
                          ('F', 'D', 'L', -1, 'g'),
                          ('F', 'R', 'D', -1, 'g'),
                          ('F', 'L', 'U', -1, 'g'),
                          ('F', 'B', 'F', -1, 'g'),
                          ('U', 'F', 'L', -1, 'g'),
                          ('U', 'U', 'U', -1, 'g'),
                          ('U', 'D', 'U', -1, 'g'),
                          ('U', 'R', 'F', -1, 'g'),
                          ('U', 'L', 'B', -1, 'g'),
                          ('U', 'B', 'R', -1, 'g')])
def test_single_color_rotate(initial_face, turn_face, arrive_face, number_of_turns, expected_color):

    # Arrange
    piece = Piece()
    piece.set_color(initial_face, expected_color)

    # Act 
    piece.rotate(turn_face, number_of_turns)

    # Assert
    assert piece.get_color(arrive_face) == expected_color
    
