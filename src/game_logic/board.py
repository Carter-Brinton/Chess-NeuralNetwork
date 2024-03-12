# /game_logic/board.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtCore import Qt
from .pieces import get_piece_name, get_image_path

class ChessboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 400)  # Fixed size for the chessboard
        self.create_board()

    def create_board(self):
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        square_size = 50
        
        for i in range(8):
            for j in range(8):
                color = QColor("white" if (i + j) % 2 == 0 else "gray")
                cell = QLabel()
                cell.setStyleSheet(f"background-color: {color.name()}; border: 0px")
                cell.setFixedSize(square_size, square_size)
                
                piece = get_piece_name(i, j)
                if piece:
                    piece_color = "white" if i < 2 else "black"
                    image_path = get_image_path(piece_color, piece)
                    pixmap = QPixmap(image_path).scaled(square_size, square_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    cell.setPixmap(pixmap)
                
                layout.addWidget(cell, i, j)
