""" Module of utilities useful for interacting with the Cube """

def side_type_converter(side, reverse=False):
    """
    Function to convert between side conventions.
    If reverse == False, converts param side to UFDLRB notation.
    if reverse == True, converts param side to xyz notation
    
    Parameters
    ----------
    side : str or list of str
        String or list of strings of side to be notation converted
    
    Returns
    -------
    converted_side : str or list of str
        String or list of strings of side that have been notation converted
    """

    if isinstance(side, list):
        return [side_type_converter(side_, reverse) for side_ in side]

    legal_xyz = ["x", "y", "z", "-x", "-y", "-z"]
    legal_ufdlrb = list("UFDLRB")

    if side not in legal_xyz + legal_ufdlrb:
        raise ValueError("Cannot convert side value: {side}")

    if reverse:
        if side in legal_xyz:
            return side

        side_map = {"F": "x", "B":"-x",
                    "R": "y", "L":"-y",
                    "U": "z", "D":"-z"}
    else:
        if side in legal_ufdlrb:
            return side

        side_map = {"x": "F", "-x": "B",
                    "y": "R", "-y": "L",                    
                    "z": "U", "-z": "D"}

    if side not in side_map:
        raise ValueError("Side map converter does not have side: {side}")

    return side_map[side]
