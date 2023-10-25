from back_end.board import Board
from back_end.moves import Moves


class ChessGame:
    def __init__(self, **kwargs):
        """
        Initialize a chess game.
        """
        self.player_color = kwargs.get("player_color", "white")
        self.board = Board(**kwargs)

    def get_valid_moves(self, position):
        """
        Get the valid moves for a position.
        """
        piece = self.board.get_piece(position)
        moves = Moves(piece, self.board)
        moves.get_valid_moves()

