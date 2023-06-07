from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import json
import game

with open("config.json", "r") as f:
    file = json.load(f)
health = file['health']
print(f'gui_11_line: {health}')



class Score(QGraphicsTextItem):

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        scene.addItem(self)
        self.score = 0
        self.setFont(QFont("Arial", 15))
        self.setPlainText(f"Очки: {self.score}")
        self.setDefaultTextColor(Qt.blue)

    def increase(self):
        self.score += 1
        with open("config.json", "r") as f:
            file = json.load(f)
        self.setPlainText(f"Очки: {self.score}")
        score_dict = {"score": self.score, "health": file['health']}

        with open("config.json", "w") as f:
            json.dump(score_dict, f)

    def increase_3(self):
        self.score += 3
        with open("config.json", "r") as f:
            file = json.load(f)
        self.setPlainText(f"Очки: {self.score}")
        score_dict = {"score": self.score, "health": file['health']}

        with open("config.json", "w") as f:
            json.dump(score_dict, f)


class Health(QGraphicsTextItem):
    dead = pyqtSignal()

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        scene.addItem(self)
        # print(scene)

        with open("config.json", "r") as f:
            file = json.load(f)
        health2 = file['health']

        self.setFont(QFont("Arial", 15))
        self.setPlainText(f"Жизни: {health2}")
        print(f'жизнь на поле(gui_52_line): {health2}')
        self.setDefaultTextColor(Qt.red)
        rect = self.boundingRect()
        self.setPos((800) - rect.width(), self.y())

    def decrease(self):
        # global health
        # health -= 1

        with open("config.json", "r") as f:
            file = json.load(f)

        file['health'] -= 1
        print(f"жизь: {file['health']}")
        print(f'gui_70_line: {file}')
        with open("config.json", "w") as f:
            json.dump(file, f)
        self.setPlainText(f"Жизни: {file['health']}")
        if file['health'] <= 0:
            self.dead.emit()


def increase():
    with open("config.json", "r") as f:
        file = json.load(f)
    file['health'] += 1
    print(f"жизь: {file['health']}")
    print(f'gui_70_line: {file}')
    with open("config.json", "w") as f:
        json.dump(file, f)
    # Health(scene=scene).setPlainText(f"Health: {health}")


class GameOver(QGraphicsTextItem):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        scene.addItem(self)
        game.Player.speed = 3
        game.Bullet.bullets = 3
        game.Bullet.motion = 1
        with open("config.json", "r") as f:
            file = json.load(f)
        self.score = file['score']
        self.setPlainText(f"                     Вы набрали очков:{self.score}\n                          Игра окончена\n нажмите на Escape чтобы выйти в главное меню")
        self.setDefaultTextColor(Qt.red)
        self.setFont(QFont("Arial", 16))
        rect = self.boundingRect()
        self.setPos((800 / 2) - rect.width() / 2, (600 / 2) - rect.height() / 2)
        print(self.boundingRect(), rect.width())
        with open("config.json", "w") as f:
            file['score'] = 0
            json.dump(file, f)
