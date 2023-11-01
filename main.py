import os
from back_end.game import ChessGame

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    game = ChessGame(player_color="white")
    game.get_valid_moves(2 * 8 + 4)
    