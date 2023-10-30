from back_end.board import Board
from back_end.moves import Moves
from back_end.utils import load_chess_move_tables


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
        # print(piece)
        moves = Moves(piece, self.board, self.move_tables)
        valid_moves, attacked_pieces = moves.get_valid_moves()
