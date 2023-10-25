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
            "black_attack": np.load("back_end/lookup_tables/BLACK_PAWN_ATTACKS.npy")
        },
        "rook": np.load("back_end/lookup_tables/ROOK_MOVES.npy"),
        "bishop": np.load("back_end/lookup_tables/BISHOP_MOVES.npy"),
        "knight": np.load("back_end/lookup_tables/KNIGHT_MOVES.npy"),
        "queen": np.load("back_end/lookup_tables/QUEEN_MOVES.npy"),
        "king": np.load("back_end/lookup_tables/KING_MOVES.npy")
    }


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
