import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QLineEdit, QDialogButtonBox, \
                            QFormLayout, QMessageBox
from PyQt6.QtCore import pyqtSlot, QFile, QTextStream, QPropertyAnimation, QDir, Qt
from PyQt6 import QtCore

from ui.desktop_app_ui import Ui_MainWindow
# from ui.desktop_app_old_uii import Ui_MainWindow

from modules import *
from modules.models import AnimeDatabase


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # QDir.setCurrent("./")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        widgets.leftMenu.show()
        widgets.logoLabel_3.hide()

        # UI: Toggle menu
        self.toggleButtonPressed = False
        widgets.toggleButton.clicked.connect(lambda:UIFunctions.toggle_menu(self))
        widgets.toggleButton.clicked.connect(lambda:UIFunctions.toggleButtonMousePressed(self, pressed=self.toggleButtonPressed))

        # CRUD Model: Setup Manage Views
        self.dtb = AnimeDatabase()
        self.dtb.load_data()
        widgets.animeList.addItems(self.dtb.anime_title_list)
        widgets.animeList.setCurrentRow(0)
        widgets.addButton.clicked.connect(lambda:UIManageFunctions.addAnime(self))
        widgets.editButton.clicked.connect(lambda:UIManageFunctions.editAnime(self))
        widgets.removeButton.clicked.connect(lambda:UIManageFunctions.deleteAnime(self))
        widgets.searchAnime.clicked.connect(lambda:UIManageFunctions.searchAnime(self))

        # RANKING VIEW: Setup Anime by Columns
        widgets.sortRankButton.clicked.connect(lambda:AnimeColumnView.viewSortedByRank(self))
        widgets.sortDateButton.clicked.connect(lambda:AnimeColumnView.viewSortedByDate(self))
        widgets.AtoZButton.clicked.connect(lambda:AnimeColumnView.viewSortedAtoZ(self))
        # TODO: EDIT THIS
        anime1 = self.dtb.anime_item_list[0]
        anime2 = self.dtb.anime_item_list[1]
        anime3 = self.dtb.anime_item_list[2]
        anime4 = self.dtb.anime_item_list[3]
        AnimeColumnView.viewAnimeInColumn(self, anime1, widgets.animeLabel1, widgets.animeTitle1)
        AnimeColumnView.viewAnimeInColumn(self, anime2, widgets.animeLabel2, widgets.animeTitle2)
        AnimeColumnView.viewAnimeInColumn(self, anime3, widgets.animeLabel3, widgets.animeTitle3)
        AnimeColumnView.viewAnimeInColumn(self, anime4, widgets.animeLabel4, widgets.animeTitle4)


    # Function for searching anime
    def on_searchButton_clicked(self):
        # Set index for searching
        self.ui.stackedWidget.setCurrentIndex(5) # ???
        search_text = self.ui.searchInput.text().strip()
        if search_text:
            self.ui.label_8.setText(search_text)
    
    # Function for changing page to user page
    def on_userButton_clicked(self):
        # Set index to change to user page=4
        self.ui.stackedWidget.setCurrentIndex(4)
    
    # Function for changing menu page
    # (0) Home Page -> (1) Tv Show -> (2) Movies -> (3) Ranking -> (4) User
    def on_homeButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_tvshowsButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
                
    def on_moviesButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_rankButton_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def on_exitButton_1_clicked(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load style
    with open("ui/style.qss", "r") as style_file:
        style_config = style_file.read()
    app.setStyleSheet(style_config)


    window = MainWindow()
    window.show()

    sys.exit(app.exec())