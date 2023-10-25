"""
This script creates the move masks for the chess pieces at any of the 64 positions on the board and saves them as .npy files.
The move masks are constant and can be loaded into memory at the start of the game as lookup tables instead of being calculated every time.
"""

import numpy as np


def print_board(board):
    board_array = board
    # Replace True with "o" and False with "."
    board_array = np.where(board_array, "o", ".")
    board_array = board_array.reshape((8, 8))
    print(board_array)


def get_diagonal_attacks_mask(position):
    """Computes the mask for the attacked squares on the diagonals."""
    if position > 64 or position < 0:
        return None
    # Create an empty mask with all False values.
    attack_mask = np.zeros(64, dtype=bool)

    # Determine the row and column of the position.
    row, col = divmod(position, 8)

    # For the positive diagonal:

    # Determine steps we can take top-left and bottom-right
    top_left_steps = min(row, col)
    bottom_right_steps = min(8 - row - 1, 8 - col - 1)

    # Calculate indices using np.arange()
    indices_positive_diag = np.concatenate(
        [
            position - np.arange(1, top_left_steps + 1) * 9,
            position + np.arange(1, bottom_right_steps + 1) * 9,
        ]
    )

    attack_mask[indices_positive_diag] = True

    # For the negative diagonal:

    # Determine steps we can take top-right and bottom-left
    top_right_steps = min(row, 8 - col - 1)
    bottom_left_steps = min(8 - row - 1, col)

    # Calculate indices using np.arange()
    indices_negative_diag = np.concatenate(
        [
            position - np.arange(1, top_right_steps + 1) * 7,
            position + np.arange(1, bottom_left_steps + 1) * 7,
        ]
    )

    attack_mask[indices_negative_diag] = True

    return attack_mask


def get_line_attacks_mask(position):
    """Computes the mask for the attacked squares on the vertical/horizontal."""
    if position > 64 or position < 0:
        return None
    # Create an empty mask with all False values.
    attack_mask = np.zeros(64, dtype=bool)

    # Determine the row and column of the position.
    row, col = divmod(position, 8)

    for i in range(8):
        position_i = row * 8 + i
        if position == position_i:
            continue
        attack_mask[position_i] = True
    for i in range(8):
        position_i = i * 8 + col
        if position == position_i:
            continue
        attack_mask[position_i] = True

    return attack_mask


def get_knight_attacks_mask(position):
    if position > 64 or position < 0:
        return None
    attack_mask = np.zeros(64, dtype=bool)
    row, col = divmod(position, 8)
    for i in range(-2, 3):
        for j in range(-2, 3):
            if abs(i) + abs(j) == 3:
                if row + i >= 0 and row + i < 8 and col + j >= 0 and col + j < 8:
                    attack_mask[(row + i) * 8 + col + j] = True
    return attack_mask


def get_king_attacks_mask(position):
    if position > 64 or position < 0:
        return None
    attack_mask = np.zeros(64, dtype=bool)
    row, col = divmod(position, 8)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (
                row + i >= 0
                and row + i < 8
                and col + j >= 0
                and col + j < 8
                and (i != 0 or j != 0)
            ):
                attack_mask[(row + i) * 8 + col + j] = True
    return attack_mask


def get_pawn_attacks_mask(position, color):
    row, col = divmod(position, 8)
    attack_mask = np.zeros(64, dtype=bool)
    if color == "white":
        if row > 0:
            if col > 0:
                attack_mask[(row - 1) * 8 + col - 1] = True
            if col < 7:
                attack_mask[(row - 1) * 8 + col + 1] = True
    else:
        if row < 7:
            if col > 0:
                attack_mask[(row + 1) * 8 + col - 1] = True
            if col < 7:
                attack_mask[(row + 1) * 8 + col + 1] = True
    return attack_mask


def get_pawn_attacks_mask(position, color):
    row, col = divmod(position, 8)
    attack_mask = np.zeros(64, dtype=bool)
    if color == "white":
        if row > 0:
            if col > 0:
                attack_mask[(row - 1) * 8 + col - 1] = True
            if col < 7:
                attack_mask[(row - 1) * 8 + col + 1] = True
    else:
        if row < 7:
            if col > 0:
                attack_mask[(row + 1) * 8 + col - 1] = True
            if col < 7:
                attack_mask[(row + 1) * 8 + col + 1] = True
    return attack_mask


def get_pawn_move_mask(position, color):
    row, col = divmod(position, 8)
    move_mask = np.zeros(64, dtype=bool)
    if color == "white":
        if row > 0:
            move_mask[(row - 1) * 8 + col] = True
            if row == 6:
                move_mask[(row - 2) * 8 + col] = True

    else:
        if row < 7:
            move_mask[(row + 1) * 8 + col] = True
            if row == 1:
                move_mask[(row + 2) * 8 + col] = True
    return move_mask


if __name__ == "__main__":
    import os

    BISHOP_MOVES = np.zeros((64, 64), dtype=bool)
    ROOK_MOVES = np.zeros((64, 64), dtype=bool)
    QUEEN_MOVES = np.zeros((64, 64), dtype=bool)
    KNIGHT_MOVES = np.zeros((64, 64), dtype=bool)
    KING_MOVES = np.zeros((64, 64), dtype=bool)
    WHITE_PAWN_MOVES = np.zeros((64, 64), dtype=bool)
    WHITE_PAWN_ATTACKS = np.zeros((64, 64), dtype=bool)
    BLACK_PAWN_MOVES = np.zeros((64, 64), dtype=bool)
    BLACK_PAWN_ATTACKS = np.zeros((64, 64), dtype=bool)
    for i in range(64):
        ROOK_MOVES[i] = get_line_attacks_mask(i)
        BISHOP_MOVES[i] = get_diagonal_attacks_mask(i)
        QUEEN_MOVES[i] = ROOK_MOVES[i] | BISHOP_MOVES[i]
        KNIGHT_MOVES[i] = get_knight_attacks_mask(i)
        KING_MOVES[i] = get_king_attacks_mask(i)
        WHITE_PAWN_MOVES[i] = get_pawn_move_mask(i, color="white")
        WHITE_PAWN_ATTACKS[i] = get_pawn_attacks_mask(i, color="white")
        BLACK_PAWN_MOVES[i] = get_pawn_move_mask(i, color="black")
        BLACK_PAWN_ATTACKS[i] = get_pawn_attacks_mask(i, color="black")
    if not os.path.exists("back_end/lookup_tables"):
        os.makedirs("back_end/lookup_tables")
    np.save("back_end/lookup_tables/ROOK_MOVES.npy", ROOK_MOVES)
    np.save("back_end/lookup_tables/BISHOP_MOVES.npy", BISHOP_MOVES)
    np.save("back_end/lookup_tables/QUEEN_MOVES.npy", QUEEN_MOVES)
    np.save("back_end/lookup_tables/KNIGHT_MOVES.npy", KNIGHT_MOVES)
    np.save("back_end/lookup_tables/KING_MOVES.npy", KING_MOVES)
    np.save("back_end/lookup_tables/WHITE_PAWN_MOVES.npy", WHITE_PAWN_MOVES)
    np.save("back_end/lookup_tables/WHITE_PAWN_ATTACKS.npy", WHITE_PAWN_ATTACKS)
    np.save("back_end/lookup_tables/BLACK_PAWN_MOVES.npy", BLACK_PAWN_MOVES)
    np.save("back_end/lookup_tables/BLACK_PAWN_ATTACKS.npy", BLACK_PAWN_ATTACKS)
