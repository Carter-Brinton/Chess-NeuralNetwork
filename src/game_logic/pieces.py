# /game_logic/pieces.py

def get_piece_name(i, j):
    if i == 0 or i == 7:
        return ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"][j]
    elif i == 1 or i == 6:
        return "pawn"
    return None

def get_image_path(piece_color, piece):
    return f"src/assets/images/chess_pieces/{piece_color}-{piece}.png"
