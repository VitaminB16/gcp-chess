class Moves:
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Moves.subclasses[cls.__name__.lower()] = cls

    def __init__(self, piece, board):
        self.piece = piece
        self.board = board

        # Fetch the relevant subclass based on the piece's name/type.
        subclass = Moves.subclasses.get(piece.name.lower())

        if subclass:
            self.movement_logic = subclass(piece, board)
        else:
            raise ValueError(f"No movement logic defined for {piece.name}")


class Pawn(Moves):
    def __init__(self, piece, board):
        super().__init__(piece, board)


class Rook(Moves):
    def __init__(self, piece, board):
        super().__init__(piece, board)


class Knight(Moves):
    def __init__(self, piece, board):
        super().__init__(piece, board)


class Bishop(Moves):
    def __init__(self, piece, board):
        super().__init__(piece, board)


class Queen(Moves):
    def __init__(self, piece, board):
        super().__init__(piece, board)


class King(Moves):
    def __init__(self, piece, board):
        super().__init__(piece, board)
