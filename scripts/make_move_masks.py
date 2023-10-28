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


def get_line_attacks_mask(position, direction):
    """Computes the mask for the attacked squares on the diagonals."""
    if position > 64 or position < 0:
        return None
    if not all(x in [1, -1, 0] for x in direction) or direction == [0, 0]:
        return None
    # Create an empty mask with all False values.
    attack_mask = np.zeros((8, 8), dtype=bool)

    # Determine the row and column of the position.
    row, col = divmod(position, 8)

    # Positive direction
    while row >= 0 and row < 8 and col >= 0 and col < 8:
        attack_mask[row, col] = True
        row += direction[0]
        col += direction[1]
    
    # Negative direction
    row, col = divmod(position, 8)
    while row >= 0 and row < 8 and col >= 0 and col < 8:
        attack_mask[row, col] = True
        row -= direction[0]
        col -= direction[1]

    attack_mask = attack_mask.reshape((64,))
    # attack_mask[position] = False

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

    BISHOP_MOVES = np.zeros((64, 64, 2), dtype=bool)
    ROOK_MOVES = np.zeros((64, 64, 2), dtype=bool)
    QUEEN_MOVES = np.zeros((64, 64, 4), dtype=bool)
    KNIGHT_MOVES = np.zeros((64, 64), dtype=bool)
    KING_MOVES = np.zeros((64, 64), dtype=bool)
    WHITE_PAWN_MOVES = np.zeros((64, 64), dtype=bool)
    WHITE_PAWN_ATTACKS = np.zeros((64, 64), dtype=bool)
    BLACK_PAWN_MOVES = np.zeros((64, 64), dtype=bool)
    BLACK_PAWN_ATTACKS = np.zeros((64, 64), dtype=bool)
    rook_directions = [[0, 1], [1, 0]]
    bishop_directions = [[1, 1], [1, -1]]
    queen_directions = [[0, 1], [1, 0], [1, 1], [1, -1]]
    for i in range(64):
        for k, direction in enumerate(rook_directions):
            ROOK_MOVES[i, :, k] = get_line_attacks_mask(i, direction)
        for k, direction in enumerate(bishop_directions):
            BISHOP_MOVES[i, :, k] = get_line_attacks_mask(i, direction)
        for k, direction in enumerate(queen_directions):
            QUEEN_MOVES[i, :, k] = get_line_attacks_mask(i, direction)
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
