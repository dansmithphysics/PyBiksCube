import pytest
from PyBiksCube.utilities import side_type_converter


@pytest.mark.parametrize("initial_side, expected_side",
                         [("U", "U"), ("F", "F"), ("D", "D"), ("L", "L"), ("R", "R"), ("B", "B"),
                          ("z", "U"), ("x", "F"), ("-z", "D"), ("-y", "L"), ("y", "R"), ("-x", "B")])
def test_notation_converter_forward(initial_side, expected_side):
    # Arrange
    # Not needed!

    # Act 
    actual_side = side_type_converter(initial_side)

    # Assert
    assert actual_side == expected_side


@pytest.mark.parametrize("initial_side, expected_side",
                         [("U", "z"), ("F", "x"), ("D", "-z"), ("L", "-y"), ("R", "y"), ("B", "-x"),
                          ("z", "z"), ("x", "x"), ("-z", "-z"), ("-y", "-y"), ("y", "y"), ("-x", "-x")])
def test_notation_converter_backward(initial_side, expected_side):
    # Arrange
    # Not needed!

    # Act 
    actual_side = side_type_converter(initial_side, reverse=True)

    # Assert
    assert actual_side == expected_side


@pytest.mark.parametrize("initial_side",
                         [("X"), ("a"), ("u"), (["x", "y", "u"])])
def test_notation_converter_valueerror(initial_side):
    with pytest.raises(ValueError):
        side_type_converter(initial_side)


