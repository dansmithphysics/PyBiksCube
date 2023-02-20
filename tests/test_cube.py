import pytest
from PyBiksCube.cube import Cube

@pytest.mark.parametrize("move_command, expected_state",
                         [("  ", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("U ", "rrrrrrrrrbbbyyyyyymmmmmmmmmyyyggggggwwwbbbbbbgggwwwwww"),
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
    cube = Cube()

    # Act 
    cube.fundamental_move(move_command)

    # Assert
    assert cube.get_cube_state() == expected_state

@pytest.mark.parametrize("move_command_1, move_command_2, expected_state",
                         [("  ", "  ", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("U ", "U'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("F ", "F'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("R ", "R'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("L ", "L'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("D ", "D'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("B ", "B'", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww")])
def test_two_fundamental_moves(move_command_1, move_command_2, expected_state):
    # Arrange
    cube = Cube()

    # Act 
    cube.fundamental_move(move_command_1)
    cube.fundamental_move(move_command_2)

    # Assert
    assert cube.get_cube_state() == expected_state
    
    

