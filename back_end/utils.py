def square_to_position(square: str):
    """
    Convert a square to a position.
    """
    if len(square) != 2:
        raise ValueError("Square must be a string of length 2.")
    row = int(square[1]) - 1
    col = ord(square[0]) - 65
    position = row * 8 + col
    return position


def ensure_position(position):
    if isinstance(position, tuple):
        position = position[0] * 8 + position[1]
    elif isinstance(position, str):
        position = square_to_position(position)
    if position < 0 or position > 63:
        raise ValueError("Position must be between 0 and 63.")
    return position


if __name__ == "__main__":
    tests = [square_to_position("A1") == 0, square_to_position("E4") == 28]
    if all(tests):
        print("Success!")
    else:
        print("One or more tests failed.")
