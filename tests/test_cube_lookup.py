import pytest

import numpy as np
import numpy.testing as npt
from PyBiksCube import CubeLookup
from PyBiksCube.utilities import convert_move_command


@pytest.fixture
def cube():
    return CubeLookup()


@pytest.mark.parametrize("cube_state",
                         [("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          ("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm"),
                          ("rryrryrryyymyymyymmmwmmwmmwgggggggggbbbbbbbbbrwwrwwrww"),
                          ("rrwrrwrrwyyryyryyrmmymmymmygggggggggbbbbbbbbbmwwmwwmww"),
                          ("wrrwrrwrrryyryyryyymmymmymmgggggggggbbbbbbbbbwwmwwmwwm"),
                          ("yrryrryrrmyymyymyywmmwmmwmmgggggggggbbbbbbbbbwwrwwrwwr")])
def test_set_cube_state(cube, cube_state):
    # Arrange
    cube.set_cube_state(cube_state)
    expected_state = cube_state

    # Act
    actual_state = cube.get_cube_state()

    # Assert
    assert expected_state == actual_state


def test_get_state(cube):
    # Arrange
    expected_state = "wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm"
    cube.set_cube_state("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm")

    # Act
    actual_state = cube.get_cube_state()

    # Assert
    assert expected_state == actual_state


def test_get_raw_state(cube):
    # Arrange
    cube_state = "wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm"
    cube.set_cube_state("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm")
    expected_state = np.array(list("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm"), dtype=str)

    # Act
    actual_state = cube.get_raw_cube_state()

    # Assert
    npt.assert_array_equal(actual_state, expected_state)


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
def test_single_fundamental_move(cube, move_command, expected_state):
    # No Arrange

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
def test_two_fundamental_moves(cube, move_command_1, move_command_2, expected_state):
    # No Arrange

    # Act
    move_command_1 = convert_move_command(move_command_1)
    move_command_2 = convert_move_command(move_command_2)
    cube._fundamental_move(move_command_1)
    cube._fundamental_move(move_command_2)

    # Assert
    assert cube.get_cube_state() == expected_state


@pytest.mark.parametrize("move_command_1, move_command_2, expected_state",
                         [(0, 6, "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          (1, 7, "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          (2, 8, "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          (3, 9, "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          (4, 10, "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          (5, 11, "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"),
                          (5, 3, "wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm")])
def test_two_moves(cube, move_command_1, move_command_2, expected_state):
    # No Arrange

    # Act
    cube.move_decoder([move_command_1, move_command_2])

    # Assert
    assert cube.get_cube_state() == expected_state


@pytest.mark.parametrize("random_seed", list(range(1, 100)))
def test_randomize(cube, random_seed):
    """ This actually Could fail sometimes while still working correctly due to randomness. Oh well. """
    # Arrange
    np.random.seed(random_seed)

    # Act
    cube.randomize(20)

    # Assert
    assert cube.check_solved() == False


def test_default_state(cube):
    # Arrange
    expected_state = "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww"

    # Act
    cube.set_default_cube_state()
    actual_state = cube.get_cube_state()

    # Assert
    assert expected_state == actual_state


@pytest.mark.parametrize("cube_state, expected_solved",
                         [("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", True),
                          ("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm", False)])
def test_check_solved(cube, cube_state, expected_solved):
    # Arrange
    cube.set_cube_state(cube_state)

    # Act
    actual_solved = cube.check_solved()

    # Assert
    assert expected_solved == actual_solved


@pytest.mark.parametrize("cube_state, key, expected_match",
                         [("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", "rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", True),
                          ("rrrrrrrrryyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", "kkkkkkkkkyyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", True),
                          ("rrrrrrrrryyyykyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", "kkkkkkkkkyyyyyyyyymmmmmmmmmgggggggggbbbbbbbbbwwwwwwwww", False),
                          ("wbbwrrwrrbyyryyryyymmymmyggrrrggggggbbmbbmbbmwwgwwmwwm", "wbbwrrwrrbyyryyryyymmymmkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", True)])
def check_match_against_key(cube, cube_state, key, expected_match):
    # Arrange
    cube.set_state(cube_state)

    # Act
    actual_match = cube.check_match_against_key(key)

    # Assert
    assert expected_match == actual_match
