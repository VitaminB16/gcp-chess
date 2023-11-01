from back_end.board import Board
from back_end.moves import Moves
from back_end.utils import load_chess_move_tables
import numpy as np


class ChessGame:
    def __init__(self, **kwargs):
        """
        Initialize a chess game.
        """
        self.player_color = kwargs.get("player_color", "white")
        self.board = Board(**kwargs)
        self.move_tables = load_chess_move_tables()

    def get_valid_moves(self, position):
        """
        Get the valid moves for a position.
        """
        piece = self.board.get_piece(position)
        moves = Moves(piece, self.board, self.move_tables)
        valid_moves, attacked_pieces = moves.get_valid_moves()

        return valid_moves, attacked_pieces

    def get_attacked_squares(self, color):
        """
        Get all squares attacked by a color.
        """
        piece_types = ["knight", "bishop", "rook", "queen", "king"]
        attacked_squares = np.zeros(64, dtype=bool)
        attacked_squares |= self.get_attacked_pawn_squares(color)
        piece_positions = set(self.board.all_pieces[color].nonzero()[0])
        piece_positions = piece_positions - set(self.board.pawns[color])
        for position in piece_positions:
            piece = self.board.get_piece(position)
            moves = Moves(piece, self.board, self.move_tables)
            valid_moves, attacked_pieces = moves.get_valid_moves()
            attacked_squares = attacked_squares | valid_moves

        return attacked_squares

    def get_attacked_pawn_squares(self, color="black"):
        """
        Get all squares attacked by the pawns of a color.
        """
        bool_mask = np.zeros(64, dtype=bool)
        pawns = self.board.pawns[color]

        if len(pawns) == 0:
            return bool_mask

        if color == "white":
            pawns_attack_left = pawns + 7
            pawns_attack_left = pawns_attack_left[
                (pawns_attack_left % 8 != 7) & (pawns_attack_left < 64)
            ]
            pawns_attack_right = pawns + 9
            pawns_attack_right = pawns_attack_right[
                (pawns_attack_right % 8 != 0) & (pawns_attack_right < 64)
            ]
        else:
            pawns_attack_right = pawns - 9
            pawns_attack_right = pawns_attack_right[
                (pawns_attack_right % 8 != 7) & (pawns_attack_right >= 0)
            ]
            pawns_attack_left = pawns - 7
            pawns_attack_left = pawns_attack_left[
                (pawns_attack_left % 8 != 0) & (pawns_attack_left >= 0)
            ]

        bool_mask[pawns_attack_left] = True
        bool_mask[pawns_attack_right] = True

        return bool_mask
