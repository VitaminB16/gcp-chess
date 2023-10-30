import numpy as np

from back_end.utils import (
    binary_array_to_int,
    int_to_binary_array,
    reverse_binary_array_int,
)


class MovesMeta(type):
    def __call__(cls, piece, board, move_data):
        # When Moves is instantiated, redirect to the appropriate subclass
        if piece is None:
            piece_type = "default"
        else:
            piece_type = piece.piece_type.lower()
        subclass = Moves.subclasses.get(piece_type)
        if subclass:
            return super(MovesMeta, subclass).__call__(piece, board, move_data)
        else:
            raise ValueError(f"No movement logic defined for {piece.name}")


class Moves(metaclass=MovesMeta):
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Moves.subclasses[cls.__name__.lower()] = cls

    def __init__(self, piece, board, move_data):
        self.piece = piece
        self.board = board
        self.move_data = move_data
        self.color = piece.color
        self.opposite_color = "black" if piece.color == "white" else "white"
        self.position = piece.position
        self.opposite_color_pieces = board.all_pieces[self.opposite_color]
        self.occupied = self.board.all_pieces["white"] | self.board.all_pieces["black"]
        self.occupied[self.position] = False
        self.attacked_by_piece = np.zeros(64, dtype=bool)
        self.position_array = np.zeros(64, dtype=bool)
        self.position_array[self.position] = True
        self.valid_moves = np.zeros(64, dtype=bool)

    def get_valid_moves(self):
        raise NotImplementedError("Should be implemented in subclasses")


class Default(Moves):
    def get_valid_moves(self):
        return []


class Queen(Moves):
    def get_valid_moves(self):
        """Logic for queen movement."""

        moves = self.move_data["queen"][:, self.position]
        directions = moves
        for direction in directions:
            o = self.occupied[direction]
            if not any(o):
                continue

            s = self.position_array[direction]
            o = self.occupied[direction]

            o_reverse = o[::-1]
            s_reverse = s[::-1]
            o_int = binary_array_to_int(o)
            s_int = binary_array_to_int(s)
            o_reverse_int = binary_array_to_int(o_reverse)
            s_reverse_int = binary_array_to_int(s_reverse)
            o_2s = o_int - 2 * s_int
            o_2s_reverse = reverse_binary_array_int(
                o_reverse_int - 2 * s_reverse_int, len(o)
            )
            line_attacks = o_2s ^ o_2s_reverse
            line_attacks = int_to_binary_array(line_attacks, len(o))

            self.valid_moves[direction] = line_attacks

        self.valid_moves = self.valid_moves & ~self.board.all_pieces[self.color]
        self.attacked_by_piece = self.valid_moves & self.opposite_color_pieces

        return self.valid_moves, self.attacked_by_piece


class Pawn(Moves):
    def get_valid_moves(self):
        """Logic for pawn movement."""
        # Select the correct move and attack patterns based on color
        if self.color == "white":
            moves = self.move_data["pawn"]["white"][self.position]
            attacks = self.move_data["pawn"]["white_attack"][self.position]
        elif self.color == "black":
            moves = self.move_data["pawn"]["black"][self.position]
            attacks = self.move_data["pawn"]["black_attack"][self.position]

        attacks = attacks & self.opposite_color_pieces
        moves = moves & ~self.board.all_pieces["all"]
        valid_moves = moves | attacks

        # TODO: Logic for en passant

        return valid_moves


class Rook(Moves):
    def get_valid_moves(self):
        """Logic for rook movement."""


class Knight(Moves):
    def get_valid_moves(self):
        """Logic for knight movement."""


class Bishop(Moves):
    def get_valid_moves(self):
        """Logic for bishop movement."""


class King(Moves):
    def get_valid_moves(self):
        """Logic for king movement."""
