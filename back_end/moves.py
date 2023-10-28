import numpy as np


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

    def get_valid_moves(self):
        raise NotImplementedError("Should be implemented in subclasses")

    
    def arr_to_int(self, ray):
        return int("".join(ray.astype(int).astype(str)), 2)


class Default(Moves):
    def get_valid_moves(self):
        return []


class Queen(Moves):
    def get_valid_moves(self):
        """Logic for queen movement."""

        

        moves = self.move_data["queen"][self.position]
        positive_directions = moves[:, [0, 1, 2, 3]]
        negative_directions = moves[:, [-1, -2, -3, -4]]

        o = self.occupied[positive_directions[:,2]]
        self.board.print_boolean(positive_directions[:,2])

        return None


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
