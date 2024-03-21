# pieces.py
SQUARE_SIZE = 80  # Size of a square in pixels
BOARD_SIZE = 8    # 8x8 Chessboard

class Piece:
    def __init__(self, color, piece_type, image):
        self.color = color
        self.type = piece_type
        self.image = image 

    def get_moves(self, x, y, board):
        # This will be overridden by derived classes
        pass
    
class Pawn(Piece):
    def __init__(self, color, image):
        super().__init__(color, 'pawn', image)

    def get_moves(self, x, y, board):
        moves = []
        direction = -1 if self.color == 'white' else 1  # Adjusted based on standard board orientation
        start_row = 6 if self.color == 'white' else 1

        # Check forward move
        if 0 <= y + direction < BOARD_SIZE and board[y + direction][x] is None:
            moves.append((x, y + direction))
            # Double move from start row
            if y == start_row and board[y + 2 * direction][x] is None:
                moves.append((x, y + 2 * direction))

        # Check captures
        for dx in [-1, 1]:
            if 0 <= x + dx < BOARD_SIZE and 0 <= y + direction < BOARD_SIZE:
                if board[y + direction][x + dx] is not None and board[y + direction][x + dx].color != self.color:
                    moves.append((x + dx, y + direction))

        return moves


class Knight(Piece):
    def __init__(self, color, image):
        super().__init__(color, 'knight', image)

    def get_moves(self, x, y, board):
        moves = []
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[ny][nx] is None or board[ny][nx].color != self.color:
                    moves.append((nx, ny))

        return moves


    
class Bishop(Piece):
    def __init__(self, color, image):
        super().__init__(color, 'bishop', image)

    def get_moves(self, x, y, board):
        # Implement bishop-specific logic here
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonals
        for dx, dy in directions:
            for step in range(1, 8):
                new_x, new_y = x + dx*step, y + dy*step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_y][new_x] is None:
                        moves.append((new_x, new_y))
                    else:
                        if board[new_y][new_x].color != self.color:
                            moves.append((new_x, new_y))
                        break
                else:
                    break
        return moves

class Rook(Piece):
    def __init__(self, color, image):
        super().__init__(color, 'rook', image)

    def get_moves(self, x, y, board):
        # Implement rook-specific logic here
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Right, Down, Left, Up
        for dx, dy in directions:
            for step in range(1, 8):  # Assuming an 8x8 board
                new_x, new_y = x + dx*step, y + dy*step
                if 0 <= new_x < 8 and 0 <= new_y < 8:  # Stay on the board
                    if board[new_y][new_x] is None:  # Empty square
                        moves.append((new_x, new_y))
                    else:
                        if board[new_y][new_x].color != self.color:  # Capture
                            moves.append((new_x, new_y))
                        break  # Blocked path
                else:
                    break  # Off the board
        return moves


class Queen(Piece):
    def __init__(self, color, image):
        super().__init__(color, 'queen', image)

    def get_moves(self, x, y, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            for step in range(1, 8):
                nx, ny = x + dx*step, y + dy*step
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break
                if board[ny][nx] is None:
                    moves.append((nx, ny))
                else:
                    if board[ny][nx].color != self.color:
                        moves.append((nx, ny))
                    break

        return moves

    
class King(Piece):
    def __init__(self, color, image):
        super().__init__(color, 'king', image)

    def get_moves(self, x, y, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[ny][nx] is None or board[ny][nx].color != self.color:
                    moves.append((nx, ny))

        return moves
