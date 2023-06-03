import sys
from random import randint

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QImage, QKeyEvent, QPainter, QFont, QFontMetrics, QColor
from PyQt6.QtWidgets import QWidget, QApplication

from constants import B_WIDTH, B_HEIGHT, DELAY, RAND_POS, DOT_SIZE, ALL_DOTS


class Snake(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color:black;')

        self.left_direction = False
        self.right_direction = True
        self.up_direction = False
        self.down_direction = False

        self.in_game = True

        self.dots = 3

        self.dot = QImage()
        self.head = QImage()
        self.apple = QImage()

        self.resize(B_WIDTH, B_HEIGHT)
        self.x = [0] * ALL_DOTS
        self.y = [0] * ALL_DOTS

        self.load_images()
        self.init_game()

    def load_images(self):

        self.dot.load('images/dot.png')
        self.head.load('images/head.png')
        self.apple.load('images/apple.png')

    def init_game(self):
        for i in range(self.dots):
            self.x.append(50 - i * 10)
            self.y.append(50)

        self.locate_apple()

        self.timer_id = self.startTimer(DELAY)

    def locate_apple(self):
        self.apple_x = randint(0, RAND_POS) * DOT_SIZE
        self.apple_y = randint(0, RAND_POS) * DOT_SIZE

    def keyPressEvent(self, e: QKeyEvent) -> None:
        key = e.key()

        if key == Qt.Key.Key_Left and not self.right_direction:
            self.left_direction = True
            self.up_direction = False
            self.down_direction = False
            print('Key_Left')

        if key == Qt.Key.Key_Right and not self.left_direction:
            self.right_direction = True
            self.up_direction = False
            self.down_direction = False
            print('Key_Right')

        if key == Qt.Key.Key_Up and not self.down_direction:
            self.up_direction = True
            self.right_direction = False
            self.left_direction = False
            print('Key_Up')

        if key == Qt.Key.Key_Down and not self.up_direction:
            self.down_direction = True
            self.right_direction = False
            self.left_direction = False
            print('Key_Down')

        super().keyPressEvent(e)

    def paintEvent(self, e):
        self.do_drawing()

    def do_drawing(self):
        qp = QPainter(self)

        if self.in_game:
            qp.drawImage(self.apple_x, self.apple_y, self.apple)

            for z in range(self.dots):
                if z == 0:
                    qp.drawImage(self.x[z], int(self.y[z]), self.head)
                else:
                    qp.drawImage(self.x[z], self.y[z], self.dot)

        else:
            self.game_over(qp)

    def game_over(self, qp):
        message = 'Game over'
        font = QFont("Courier", 15, QFont.Weight.DemiBold)
        fm = QFontMetrics(font)
        text_width = fm.averageCharWidth() * len(message)

        qp.setPen(QColor('white'))
        qp.setFont(font)

        h = self.height()
        w = self.width()
        print(text_width)

        qp.translate(QPoint(w // 2, h // 2))
        qp.drawText(-text_width // 2, 0, message)

    def check_apple(self):
        if self.x[0] == self.apple_x and self.y[0] == self.apple_y:
            self.dots += 1
            self.locate_apple()

    def move(self):
        for z in reversed(range(1, self.dots)):
            self.x[z] = self.x[z - 1]
            self.y[z] = self.y[z - 1]

        if self.left_direction:
            self.x[0] -= DOT_SIZE

        if self.right_direction:
            self.x[0] += DOT_SIZE

        if self.up_direction:
            self.y[0] -= DOT_SIZE

        if self.down_direction:
            self.y[0] += DOT_SIZE

    def check_collision(self):
        for z in reversed(range(self.dots)):
            if z > 4 and self.x[0] == self.x[z] and self.y[0] == self.y[z]:
                self.in_game = False

        if self.y[0] >= B_HEIGHT:
            self.in_game = False

        if self.y[0] < 0:
            self.in_game = False

        if self.x[0] >= B_WIDTH:
            self.in_game = False

        if self.x[0] < 0:
            self.in_game = False

        if not self.in_game:
            self.killTimer(self.timer_id)

    def timerEvent(self, e):
        if self.in_game:
            self.check_apple()
            self.check_collision()
            self.move()

        self.repaint()


def main():
    app = QApplication(sys.argv)

    window = Snake()
    window.setWindowTitle('Snake')
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
