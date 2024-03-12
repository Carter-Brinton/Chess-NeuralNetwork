# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from game_logic.board import ChessboardWidget
from PyQt6.QtCore import Qt

class ChessBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess Board")
        self.setGeometry(100, 100, 500, 500)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        chessboard_widget = ChessboardWidget()
        main_layout.addWidget(chessboard_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chess_board = ChessBoard()
    chess_board.show()
    sys.exit(app.exec())
