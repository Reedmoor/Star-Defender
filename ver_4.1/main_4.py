import sys

from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QPushButton, QVBoxLayout, QWidget, QApplication, QLabel,QAction
from PyQt5.QtGui import QPixmap, QImage, QBrush
from PyQt5.QtCore import Qt, QUrl, QTimer
import PyQt5.QtMultimedia as M
import sys
import json
import gui
from main import scene
from gui import Health
import game

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor,QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGridLayout, \
    QSizePolicy, QSpacerItem

main_widget = None
background = 'res/images/background.png'
button_style = 'color: #fff; ' \
               'background: green; ' \
               'width: 250px; ' \
               'height: 80px;' \
               'font: bold 20px Arial;' \
               'border-radius: 16px'
text_style = 'color: #fff; ' \
             'font: normal 22px Arial;'

class Game_yay_Start(QDialog):
    def close(self):
        print("youlose")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Star defender')
        self.setSizePolicy(800, 600)
        self.setStyleSheet("background-color: black;")

        with open("config.json", 'r') as f:
            file = json.load(f)
            if file['health'] <= 0:
                file['health'] = 3
            with open("config.json", "w") as f:
                json.dump(file, f)
                print(f'main_21_line: {file}')

        self.setWindowIcon(QIcon('icon.png'))
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 800, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setBackgroundBrush(QBrush(QImage("./res/images/background.png")))

        self.score = gui.Score(self.scene)
        self.health = gui.Health(self.scene)
        self.player = game.Player(self.scene, self.score, self.health)
        self.player.setPos(self.view.width() / 2, self.view.height() - self.player.pixmap().height())
        self.player.setPixmap(QPixmap("./res/images/player.png"))
        self.player.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.player.setFocus()

        self.health.dead.connect(self.gameOver)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.url = QUrl.fromLocalFile("/res/sounds/background.wav")
        media = M.QMediaContent(self.url)
        playlist = M.QMediaPlaylist()
        playlist.addMedia(media)
        playlist.setPlaybackMode(M.QMediaPlaylist.Loop)
        self.music = M.QMediaPlayer()
        self.music.setPlaylist(playlist)
        self.music.setVolume(10)
        self.music.play()

        quit = QAction('Quit', self)
        quit.triggered.connect(self.close)

    def closeEvent(self, event):
        event.ignore()

    def gameOver(self):
        self.music.stop()
        self.scene.clear()
        gui.GameOver(self.scene)
        self.close()


class Main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_widget = None
        self.main_layout = QHBoxLayout()

        self.setWindowTitle('Меню')
        self.setLayout(self.main_layout)
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(800, 500, 800, 600)
        self.setStyleSheet(f"background-image: url({background});background-color: black;")

        self.open_main_widget('openMenu')

    def open_main_widget(self, name_widget):
        if name_widget == 'openMenu':
            self.main_widget = self.MenuWindow()
            self.main_layout.addWidget(self.main_widget)
            print('openMenu')
        if name_widget == 'openRules':
            self.main_widget = self.RulesWindow()
            print('openRules')
        if name_widget == 'openShop':
            self.main_widget = self.ShopWindow()
            print('openShop')
        if name_widget == 'openGame':
            self.main_widget.hide()
            print('openGame')

        item = self.main_layout.itemAt(0)
        self.main_layout.removeItem(item)

        self.main_layout.addWidget(self.main_widget)

    def CloseMenuOpenShop(self):
        self.open_main_widget('openShop')
        self.btnPlay.deleteLater()
        self.btnShop.deleteLater()
        self.btnRulesAndControls.deleteLater()
        self.btnExit.deleteLater()

    def CloseMenuOpenRules(self):
        self.open_main_widget('openRules')
        self.btnPlay.deleteLater()
        self.btnShop.deleteLater()
        self.btnRulesAndControls.deleteLater()
        self.btnExit.deleteLater()

    def MenuWindow(self):
        self.btnPlay = QPushButton('Играть', self)
        self.btnPlay.setStyleSheet(button_style)
        self.btnPlay.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPlay.clicked.connect(self.openGame)

        self.btnShop = QPushButton('Магазин', self)
        self.btnShop.setStyleSheet(button_style)
        self.btnShop.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnShop.clicked.connect(lambda: self.CloseMenuOpenShop())

        self.btnRulesAndControls = QPushButton('Правила', self)
        self.btnRulesAndControls.setStyleSheet(button_style)
        self.btnRulesAndControls.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnRulesAndControls.clicked.connect(lambda: self.CloseMenuOpenRules())

        self.btnExit = QPushButton('Выйти', self)
        self.btnExit.setStyleSheet(button_style)
        self.btnExit.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnExit.clicked.connect(lambda: self.close())

        self.menu_layout = QVBoxLayout()
        self.menu_layout.addStretch()
        self.menu_layout.addWidget(self.btnPlay)
        self.menu_layout.addWidget(self.btnShop)
        self.menu_layout.addWidget(self.btnRulesAndControls)
        self.menu_layout.addWidget(self.btnExit)
        self.menu_layout.addStretch()

        self.menu_widget = QWidget()
        self.menu_widget.setFixedWidth(200)
        self.menu_widget.setLayout(self.menu_layout)

        self.window_layout = QHBoxLayout()
        self.window_layout.addWidget(self.menu_widget)

        self.menu_window = QWidget()
        self.menu_window.setLayout(self.window_layout)
        return self.menu_window

    def RulesClose(self):
        self.open_main_widget('openMenu')
        self.rules_widget.deleteLater()
        self.rules_to_menu.deleteLater()

    def RulesWindow(self):
        self.rules_widget = QLabel()
        self.rules_widget.setFixedWidth(800)
        self.rules_widget.setStyleSheet(text_style)
        self.rules_widget.setWordWrap(True)
        self.rules_widget.setText(
            'Управление кораблем осуществляется с помощью стрелок.\n'      
            'Стрелка влево – перемещение корабля влево,\n'
            'Стрелка вправо – перемещение корабля вправо,\n'
            'Стрельба – пробел,\n'
            'Escape во время игры при отсутствии пуль на экране - закрыть окно игры и сохранить прогресс.\n'
            '\n'
            'Правила игры:'
            'Игроку необходимо набрать наибольшее количество очков. '
            'Игрок может двигаться только вправо и влево. Игрок не может выйти за экран. '
            'Для получения очков необходимо уничтожать метеориты (1 очко за серый, 3 очка за синий). '
            'При столкновении с метеоритом происходит потеря одной единицы жизни, '
            'игра заканчивается если количество жизней = 0.'
        )

        self.rules_to_menu = QPushButton('Назад', self)
        self.rules_to_menu.setFixedWidth(200)
        self.rules_to_menu.setStyleSheet(button_style)
        self.rules_to_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.rules_to_menu.clicked.connect(lambda: self.RulesClose())

        self.window_layout = QVBoxLayout()
        self.window_layout.addWidget(self.rules_widget)
        self.window_layout.addWidget(self.rules_to_menu, alignment=Qt.AlignCenter)

        self.rules_window = QWidget()
        self.rules_window.setLayout(self.window_layout)
        return self.rules_window

    def Shopclose(self):

        self.btnHP.deleteLater()
        self.btnMaxBullet.deleteLater()
        self.btnShipSpeed.deleteLater()
        self.btnBulletSpeed.deleteLater()
        self.btnExitToMenu.deleteLater()
        self.open_main_widget('openMenu')

    def message_few_score(self):
        self.few_label = QLabel("Недостаточно очков")
        self.few_label.setStyleSheet(f"{text_style}")
        timer = QTimer()
        timer.singleShot(1000, self.few_label.deleteLater)

    def HPplus(self, score):
        # health_default = gui.health
        # print(health_default)
        self.score_label.setText(f"Score: {score}")
        with open("config.json", "r") as f:
            file = json.load(f)

        # with open("config.json", "w") as f:
        #     json.dump(file, f)
        if score >= 200:
            # gui.Health(scene=scene).setPlainText(f"Health: {gui.health}")
            file['score'] = score - 200
            self.score -= 200
            with open("config.json", "w") as f:
                json.dump(file, f)
                print(f'main4_231_line: {file}')
            gui.increase()
        else:
            self.message_few_score()
            self.window_layout.addWidget(self.few_label, 0, 0)
        self.score_label.setText(f"Очки: {score}")

    def BulletsPlus(self, score):
        with open("config.json", "r") as f:
            file = json.load(f)
        with open("config.json", "w") as f:
            json.dump(file, f)
        if score >= 100:
            # gui.Health(scene=scene).setPlainText(f"Health: {gui.health}")
            file['score'] = score - 100
            self.score -= 100
            with open("config.json", "w") as f:
                json.dump(file, f)
            self.score_label.setText(f"Очки: {score}")
            game.Bullet.bullets += 1
            game.Bullet.Max_bullet +=1
        else:
            self.message_few_score()
            self.window_layout.addWidget(self.few_label, 0, 1)
        self.score_label.setText(f"Очки: {score}")

    def ShipSpPlus(self, score):
        with open("config.json", "r") as f:
            file = json.load(f)
        with open("config.json", "w") as f:
            json.dump(file, f)
        if score >= 50:
            # gui.Health(scene=scene).setPlainText(f"Health: {gui.health}")
            file['score'] = score - 50
            self.score -= 50
            with open("config.json", "w") as f:
                json.dump(file, f)
                print(f'main4_231_line: {file}')
            game.Player.speed += 1
        else:
            self.message_few_score()
            self.window_layout.addWidget(self.few_label, 1, 0)
        self.score_label.setText(f"Очки: {score}")

    def BulSpPlus(self, score):
        with open("config.json", "r") as f:
            file = json.load(f)
        with open("config.json", "w") as f:
            json.dump(file, f)
        if score >= 50:
            # gui.Health(scene=scene).setPlainText(f"Health: {gui.health}")
            file['score'] = score - 50
            self.score -= 50
            with open("config.json", "w") as f:
                json.dump(file, f)
                print(f'main4_231_line: {file}')
            game.Bullet.motion += 1
        else:
            self.message_few_score()
            self.window_layout.addWidget(self.few_label, 1, 1)
        self.score_label.setText(f"Очки: {score}")

    def ShopWindow(self):
        with open("config.json", "r") as f:
            data = json.load(f)

        score = data["score"]

        self.score = score
        self.score_label = QLabel(f"Очки: {self.score}")
        self.score_label.setStyleSheet("font-size: 20px; color: red;")

        self.btnHP = QPushButton('Добавить жизнь\n +1 (200)', self)
        self.btnHP.setStyleSheet(button_style)
        self.btnHP.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnHP.clicked.connect(lambda: self.HPplus(self.score))

        self.btnMaxBullet = QPushButton('Увеличить количество\n пуль +1 (100)', self)
        self.btnMaxBullet.setStyleSheet(button_style)
        self.btnMaxBullet.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnMaxBullet.clicked.connect(lambda: self.BulletsPlus(self.score))

        self.btnShipSpeed = QPushButton('Увеличить скорость\n корабля (50)', self)
        self.btnShipSpeed.setStyleSheet(button_style)
        self.btnShipSpeed.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnShipSpeed.clicked.connect(lambda: self.ShipSpPlus(self.score))

        self.btnBulletSpeed = QPushButton('Увеличить скорость\n пуль (50)', self)
        self.btnBulletSpeed.setStyleSheet(button_style)
        self.btnBulletSpeed.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnBulletSpeed.clicked.connect(lambda: self.BulSpPlus(self.score))

        self.btnExitToMenu = QPushButton('Выход', self)
        self.btnExitToMenu.setStyleSheet(button_style)
        self.btnExitToMenu.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnExitToMenu.clicked.connect(lambda: self.Shopclose())

        self.btnHP.setMinimumWidth(150)
        self.btnMaxBullet.setMinimumWidth(150)
        self.btnShipSpeed.setMinimumWidth(150)
        self.btnBulletSpeed.setMinimumWidth(150)
        self.btnExitToMenu.setMinimumWidth(150)

        self.window_layout = QGridLayout()
        self.window_layout.addWidget(self.btnHP, 0, 0)
        self.window_layout.addWidget(self.btnMaxBullet, 0, 1)
        self.window_layout.addWidget(self.btnShipSpeed, 1, 0)
        self.window_layout.addWidget(self.btnBulletSpeed, 1, 1)
        self.window_layout.addWidget(self.score_label, 0, 3, 1, 2, alignment=Qt.AlignCenter)
        self.window_layout.addWidget(self.btnExitToMenu, 2, 0, 1, 2)

        self.Shop_widget = QWidget()
        self.Shop_widget.setFixedWidth(600)
        self.Shop_widget.setLayout(self.window_layout)

        return self.Shop_widget

    def openGame(self):
        self.game_dialog = Game_yay_Start()
        self.game_dialog.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    # window.showMaximized()
    window.show()
    sys.exit(app.exec())
