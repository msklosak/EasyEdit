import sys

from PyQt5.QtWidgets import QApplication, QFileDialog, QFontDialog, QMainWindow

from easyedit.about_dialog import AboutDialog
from easyedit.menu_bar import MenuBar
from easyedit.tab_bar import TabBar


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Untitled - EasyEdit")
        self.resize(600, 800)
        self.center_window()

        self.about_dialog = AboutDialog()

        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)

        self.tab_bar = TabBar()
        self.setCentralWidget(self.tab_bar)

        self.status_bar = self.statusBar()

        self.create_status_bar()

        self.configure_signals()

        self.show()

    def closeEvent(self, event):
        while self.tab_bar.count() > 0:
            self.tab_bar.close_tab(0)

        QApplication.quit()

    def configure_signals(self):
        # FILE TAB
        self.menu_bar.new_file.connect(self.tab_bar.open_tab)
        self.menu_bar.open_file.connect(self.open_file)
        self.menu_bar.save_file.connect(self.save_file)
        self.menu_bar.save_file_as.connect(self.save_file)

        # EDIT TAB
        self.menu_bar.undo_edit.connect(self.tab_bar.get_current_tab().undo)
        self.menu_bar.redo_edit.connect(self.tab_bar.get_current_tab().redo)
        self.menu_bar.cut_text.connect(self.tab_bar.get_current_tab().cut)
        self.menu_bar.copy_text.connect(self.tab_bar.get_current_tab().copy)
        self.menu_bar.paste_text.connect(self.tab_bar.get_current_tab().paste)

        # SETTINGS TAB
        self.menu_bar.change_font.connect(self.change_font)

        # HELP TAB
        self.menu_bar.about_dialog.connect(lambda: self.about_dialog.exec_())

        # TAB BAR
        self.tab_bar.tab_changed.connect(self.update_window_title)

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)

        self.move(frame_geometry.topLeft())

    def change_font(self):
        font = QFontDialog().getFont()[0]

        self.setFont(font)
        self.tab_bar.get_current_tab().update_font(font)

    def create_text_edit(self):
        self.setCentralWidget(self.text_edit)

        self.text_edit.textChanged.connect(self.set_unsaved_changes)

    def create_status_bar(self):
        pass

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File")[0]

        if file_name:
            file = open(file_name, 'r')

            with file:
                self.tab_bar.get_current_tab().setText(file.read())

            self.tab_bar.setTabText(self.tab_bar.currentIndex(), file_name)

            file.close()

    def save_file(self):
        file_name = QFileDialog.getSaveFileName(self, "Save File", None, "Text Files (*.txt);;All Files (*)")[0]

        if file_name:
            self.update_window_title(file_name)
            self.tab_bar.setTabText(self.tab_bar.currentIndex(), file_name)

        file = open(file_name, 'w')

        text = self.tab_bar.get_current_tab().toPlainText()

        file.write(text)
        file.close()

    def update_window_title(self, new_title):
        self.setWindowTitle(new_title + " - EasyEdit")


if __name__ == '__main__':
    application = QApplication(sys.argv)

    editor = Editor()

    sys.exit(application.exec_())
