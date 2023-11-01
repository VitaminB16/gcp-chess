import numpy as np


def square_to_position(square: str):
    """
    Convert a square to a position.
    """
    if len(square) != 2:
        raise ValueError("Square must be a string of length 2.")
    row = int(square[1]) - 1
    col = ord(square[0].upper()) - 65
    position = row * 8 + col
    return position


def rankfile_to_position(rankfile: tuple):
    rank, file = rankfile
    return rank * 8 + file


def ensure_position(position):
    if isinstance(position, tuple):
        position = rankfile_to_position(position)
    elif isinstance(position, str):
        position = square_to_position(position)
    if position < 0 or position > 63:
        raise ValueError("Position must be between 0 and 63.")
    return position


def load_chess_move_tables():
    import numpy as np

    return {
        "pawn": {
            "white": np.load("back_end/lookup_tables/WHITE_PAWN_MOVES.npy"),
            "black": np.load("back_end/lookup_tables/BLACK_PAWN_MOVES.npy"),
            "white_attack": np.load("back_end/lookup_tables/WHITE_PAWN_ATTACKS.npy"),
            "black_attack": np.load("back_end/lookup_tables/BLACK_PAWN_ATTACKS.npy"),
        },
        "rook": np.load("back_end/lookup_tables/ROOK_MOVES.npy"),
        "bishop": np.load("back_end/lookup_tables/BISHOP_MOVES.npy"),
        "knight": np.load("back_end/lookup_tables/KNIGHT_MOVES.npy"),
        "queen": np.load("back_end/lookup_tables/QUEEN_MOVES.npy"),
        "king": np.load("back_end/lookup_tables/KING_MOVES.npy"),
    }


def binary_array_to_int(arr):
    """Convert a binary array to an integer, e.g. [1, 0, 1] -> 5."""
    return int("".join(str(int(b)) for b in arr), 2)


def int_to_binary_array(num, length):
    """Convert an integer to a binary array, e.g. 5 -> [1, 0, 1]."""
    return np.array([bool(int(x)) for x in f"{num:0{length}b}"])


def reverse_binary_array(arr):
    """Reverse a binary array, e.g. [1, 1, 0] -> [0, 1, 1]"""
    return arr[::-1]


def reverse_binary_array_int(num, length):
    """Reverse an integer's binary representation, e.g. 6 -> [1, 1, 0] -> [0, 1, 1] -> 3"""
    if num < 0:
        num = 0
    return binary_array_to_int(reverse_binary_array(int_to_binary_array(num, length)))


def compute_line_attacks(o, s):
    """Compute the line attacks for a slider piece s and occupied squares o.
    E.g. (o=[1,1,1,0,0,1,0,1], s=[0,0,0,0,0,1,0,0]) -> [0,0,1,1,1,0,1,1]
    """
    o_reverse = o[::-1]
    s_reverse = s[::-1]
    o_int = binary_array_to_int(o)
    s_int = binary_array_to_int(s)
    o_reverse_int = binary_array_to_int(o_reverse)
    s_reverse_int = binary_array_to_int(s_reverse)
    o_2s = o_int - 2 * s_int
    o_2s_reverse = reverse_binary_array_int(o_reverse_int - 2 * s_reverse_int, len(o))
    line_attacks = o_2s ^ o_2s_reverse
    line_attacks = int_to_binary_array(line_attacks, len(o))
    return line_attacks


if __name__ == "__main__":
    tests = [
        square_to_position("A1") == 0,
        square_to_position("E4") == 28,
        rankfile_to_position((5, 5)) == 45,
    ]
    if all(tests):
        print("Success!")
    else:
        print("One or more tests failed.")
