import pytest

import pytest
from PyBiksCube import CubeLookup
from PyBiksCube.utilities import convert_move_command

@pytest.mark.parametrize("move_command, expected_state",
                         [("U ", "rrrrrrrrrbbbyyyyyymmmmmmmmmyyyggggggwwwbbbbbbgggwwwwww"),                          
                          ("U'", "rrrrrrrrrgggyyyyyymmmmmmmmmwwwggggggyyybbbbbbbbbwwwwww"),
                          ("F ", "rrrrrrgggyyyyyyyyybbbmmmmmmggmggmggmrbbrbbrbbwwwwwwwww"),
                          ("F'", "rrrrrrbbbyyyyyyyyygggmmmmmmggrggrggrmbbmbbmbbwwwwwwwww"),
                          ("R ", "rryrryrryyymyymyymmmwmmwmmwgggggggggbbbbbbbbbrwwrwwrww"),
                          ("R'", "rrwrrwrrwyyryyryyrmmymmymmygggggggggbbbbbbbbbmwwmwwmww"),
                          ("L ", "wrrwrrwrrryyryyryyymmymmymmgggggggggbbbbbbbbbwwmwwmwwm"),
                          ("L'", "yrryrryrrmyymyymyywmmwmmwmmgggggggggbbbbbbbbbwwrwwrwwr"),
                          ("D ", "rrrrrrrrryyyyyygggmmmmmmmmmggggggwwwbbbbbbyyywwwwwwbbb"),
                          ("D'", "rrrrrrrrryyyyyybbbmmmmmmmmmggggggyyybbbbbbwwwwwwwwwggg"),
                          ("B ", "bbbrrrrrryyyyyyyyymmmmmmgggrggrggrggbbmbbmbbmwwwwwwwww"),
                          ("B'", "gggrrrrrryyyyyyyyymmmmmmbbbmggmggmggbbrbbrbbrwwwwwwwww")])
def test_single_fundamental_move(move_command, expected_state):
    # Arrange
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")

    # Act
    move_command = convert_move_command(move_command)
    cube._fundamental_move(move_command)

    # Assert
    assert cube.get_cube_state() == expected_state


@pytest.mark.parametrize("move_command_1, move_command_2, expected_state",
                         [("U ", "U'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),                          
                          ("F ", "F'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("R ", "R'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("L ", "L'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("D ", "D'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("B ", "B'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("B ", "L ", "wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm")])
def test_two_fundamental_moves(move_command_1, move_command_2, expected_state):
    # Arrange
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt")

    # Act
    move_command_1 = convert_move_command(move_command_1)
    move_command_2 = convert_move_command(move_command_2)
    cube._fundamental_move(move_command_1)
    cube._fundamental_move(move_command_2)

    # Assert
    assert cube.get_cube_state() == expected_state


@pytest.mark.parametrize("cube_state, expected_solved",
                         [("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", True),
                          ("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm", False)])                          
def test_check_solved(cube_state, expected_solved):
    # Arrange
    cube = CubeLookup("./PyBiksCube/data/cube_lookup_table.txt", cube_state)

    # Act
    actual_solved = cube.check_solved()

    # Assert
    assert expected_solved == actual_solved
    
    
    

