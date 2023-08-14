import random as rn
import sys

import numpy
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QDialog, QVBoxLayout, QLabel

NUMBER_OF_UNIT: int = 4
UNIT_SIZE: int = 100



class MyDialog(QDialog):
    def __init__(self, message: str, my_title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(my_title)
        self.setModal(True)
        self.setFixedSize(300, 180)
        layout = QVBoxLayout(self)
        label = QLabel(message)
        layout.addWidget(label)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


class Game:  # up second
    def __init__(self):
        self.score: int = 0
        self.number_array = numpy.full((NUMBER_OF_UNIT, NUMBER_OF_UNIT), 0)
        first_place: int = rn.randint(0, NUMBER_OF_UNIT * NUMBER_OF_UNIT - 1)
        self.number_array[first_place % NUMBER_OF_UNIT][first_place // NUMBER_OF_UNIT] = int(rn.randint(1, 2) * 2)

    def go_up(self) -> None:
        # print(self.number_array)
        for i in range(NUMBER_OF_UNIT):
            counter: int = 0
            for j in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] != 0:
                    temp = self.number_array[i][j]
                    self.number_array[i][j] = 0
                    self.number_array[i][counter] = temp
                    # print("counter" + str(counter) + str(i))
                    counter += 1
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT - 1):
                if self.number_array[i][j] == self.number_array[i][j + 1]:
                    self.number_array[i][j] *= 2
                    self.score += self.number_array[i][j]
                    self.number_array[i][j + 1] = 0
        for i in range(NUMBER_OF_UNIT):
            counter: int = 0
            for j in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] != 0:
                    temp = self.number_array[i][j]
                    self.number_array[i][j] = 0
                    self.number_array[i][counter] = temp
                    counter += 1

    def go_left(self) -> None:
        self.go_right()
        for i in range(NUMBER_OF_UNIT):
            if self.number_array[0][i] != 0:
                number_of_non_zero_numbers = 0
                for j in range(NUMBER_OF_UNIT):
                    if self.number_array[j][i] != 0:
                        number_of_non_zero_numbers += 1
                for k in range(number_of_non_zero_numbers):
                    self.number_array[- k - 1][i] = self.number_array[number_of_non_zero_numbers - k - 1][i]
                    if number_of_non_zero_numbers != NUMBER_OF_UNIT:
                        self.number_array[number_of_non_zero_numbers - k - 1][i] = 0

    def go_right(self) -> None:
        for j in range(NUMBER_OF_UNIT):
            counter: int = 0
            for i in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] != 0:
                    temp = self.number_array[i][j]
                    self.number_array[i][j] = 0
                    self.number_array[counter][j] = temp
                    counter += 1
        for i in range(NUMBER_OF_UNIT - 1):
            for j in range(NUMBER_OF_UNIT):
                if self.number_array[i + 1][j] == self.number_array[i][j]:
                    self.number_array[i][j] *= 2
                    self.score += self.number_array[i][j]
                    self.number_array[i + 1][j] = 0
        for j in range(NUMBER_OF_UNIT):
            counter: int = 0
            for i in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] != 0:
                    temp = self.number_array[i][j]
                    self.number_array[i][j] = 0
                    self.number_array[counter][j] = temp
                    counter += 1

    def go_down(self) -> None:
        self.go_up()
        for i in range(NUMBER_OF_UNIT):
            if self.number_array[i][0] != 0:
                number_of_non_zero_numbers = 0
                for j in range(NUMBER_OF_UNIT):
                    if self.number_array[i][j] != 0:
                        number_of_non_zero_numbers += 1
                for k in range(number_of_non_zero_numbers):
                    self.number_array[i][- k - 1] = self.number_array[i][number_of_non_zero_numbers - k - 1]
                    if number_of_non_zero_numbers != NUMBER_OF_UNIT:
                        self.number_array[i][number_of_non_zero_numbers - k - 1] = 0

    def get_score(self) -> int:  # update the score at the same time
        print(self.score)
        return self.score

    def generate_random_number(self) -> None:
        count_of_empty: int = 0
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] == 0:
                    count_of_empty += 1
        if count_of_empty == 0:
            return
        my_random_number = rn.randint(0, count_of_empty - 1)
        count_of_empty = 0
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] == 0:
                    if count_of_empty == my_random_number:
                        self.number_array[i][j] = rn.randint(1, 2) * 2
                        return

                    count_of_empty += 1

    def check_defeat(self) -> bool:
        copy = self.number_array
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT):
                if copy[i][j] == 0:
                    return False
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT - 1):
                if copy[i][j] == copy[i][j + 1] or copy[j][i] == copy[j + 1][i]:
                    return False
        return True

    def check_win(self) -> bool:
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT):
                if self.number_array[i][j] >= 2048:
                    return True
        return False

    def get_board(self):
        return self.number_array


class MyWindows(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.pushBTN = QtWidgets.QPushButton(self)
        self.pushBTN.setText("      reset     ")
        # self.pushBTN.move(310, 50)
        self.pushBTN.setStyleSheet("QPushButton {\
                      background-color: #6740dd;border-style: solid;border-width: 3px;border-radius: 20px;\
                      border-color: #2196F3;\
                      padding: 10px;\
                      }\
                      QPushButton:hover {\
                      background-color: #2196F3;\
                      color: white;\
                      }")
        self.pushBTN.clicked.connect(self.new_game)
        self.setWindowTitle("2048")
        self.widget: QtWidgets.QFrame = QtWidgets.QFrame(self)
        self.widget.setStyleSheet("border: 5px solid red;background-color:white;")
        self.widget.setFixedSize(UNIT_SIZE * NUMBER_OF_UNIT, UNIT_SIZE * NUMBER_OF_UNIT)
        self.widget.move(50, 120)
        self.setFixedSize(UNIT_SIZE * NUMBER_OF_UNIT + 100, UNIT_SIZE * NUMBER_OF_UNIT + 200)
        self.widget_list: list = []
        self.widget_string_color: list = []
        self.score_label = QtWidgets.QLabel(self)
        self.score_label.move(self.width() // 2, 20)
        self.score_label.setText("score: 0         ")
        self.score_label.setStyleSheet("background-color: #ff0000;padding: 25 px ;border-radius: 15px;border-radius: "
                                       "10px;")
        my_font = QFont()
        my_font.setPointSize(22)
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT):
                temp_label = QtWidgets.QLabel(self.widget)
                temp_label.move(i * UNIT_SIZE, j * UNIT_SIZE)  # set the place
                temp_label.setFixedSize(UNIT_SIZE, UNIT_SIZE)
                temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                temp_label.setStyleSheet("background: #ffffff;border: 1px solid red;text-align: "
                                         "center;color:black;border-radius:8")
                self.widget_string_color.append("#ffffff")  # white
                temp_label.setFont(my_font)
                self.widget_list.append(temp_label)
                # print("append is called")
        self.render_game_screen()
        self.show()

    def new_game(self):
        self.game = Game()
        self.render_game_screen()

    def reset(self):
        self.game = Game()
        self.render_game_screen()

    def render_game_screen(self):
        self.score_label.setText(f"score: {self.game.get_score()}")
        self.game.generate_random_number()
        board = self.game.get_board()
        if self.game.check_win():
            dig = MyDialog("you win!\nDo you want to continue?", "win")
            if dig.exec() == QDialog.DialogCode.Rejected:
                self.game = Game()
                self.render_game_screen()
        elif self.game.check_defeat():
            dig = MyDialog("GAME OVER!\nDo you want to play again?", "lose")
            if dig.exec() == QDialog.DialogCode.Accepted:
                self.game = Game()
                self.render_game_screen()
        for i in range(NUMBER_OF_UNIT):
            for j in range(NUMBER_OF_UNIT):
                number = board[i][j]
                if number == 0:
                    self.widget_list[NUMBER_OF_UNIT * i + j].setText("")
                else:
                    self.widget_list[NUMBER_OF_UNIT * i + j].setText(str(number))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_R or event.key() == Qt.Key.Key_Left:
            self.game.go_right()
            self.render_game_screen()
        elif event.key() == Qt.Key.Key_L or event.key() == Qt.Key.Key_Right:
            self.game.go_left()
            self.render_game_screen()
        elif event.key() == Qt.Key.Key_U or event.key() == Qt.Key.Key_Up:
            self.game.go_up()
            self.render_game_screen()
        elif event.key() == Qt.Key.Key_D or event.key() == Qt.Key.Key_Down:
            self.game.go_down()
            self.render_game_screen()
        elif event.key() == Qt.Key.Key_N:
            self.new_game()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindows()
    app.exec()
