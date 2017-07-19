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
        self.tab_bar.tab_changed.connect(self.tab_changed)

        # TEXT AREA
        self.tab_bar.currentWidget().cursor_position_changed.connect(self.update_status_bar_text)

    def change_font(self):
        font = QFontDialog().getFont()[0]

        self.setFont(font)

        current_tab = 0
        while current_tab > self.tab_bar.count():
            self.tab_bar.widget(current_tab).update_font(font)

    def create_text_edit(self):
        self.setCentralWidget(self.text_edit)

        self.text_edit.textChanged.connect(self.set_unsaved_changes)

    def create_status_bar(self):
        self.update_status_bar_text()

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File")[0]

        if file_name != "":
            with open(file_name, 'r') as file:
                self.tab_bar.get_current_tab().setText(file.read())

            self.tab_bar.setTabText(self.tab_bar.currentIndex(), file_name)
            self.update_window_title(file_name)

    def save_file(self):
        if self.tab_bar.tabText(self.tab_bar.currentIndex()) != "Untitled":
            file_name = self.tab_bar.tabText(self.tab_bar.currentIndex())
        else:
            file_name = QFileDialog.getSaveFileName(self, "Save File", None, "Text Files (*.txt);;All Files (*)")[0]

            if file_name != "":
                self.update_window_title(file_name)
                self.tab_bar.setTabText(self.tab_bar.currentIndex(), file_name)

        if file_name != "":
            text = self.tab_bar.get_current_tab().toPlainText()

            with open(file_name, 'w') as file:
                file.write(text)

    def tab_changed(self):
        self.tab_bar.currentWidget().cursor_position_changed.connect(self.update_status_bar_text)

        self.update_window_title(self.tab_bar.tabText(self.tab_bar.currentIndex()))
        self.update_status_bar_text()

    def update_window_title(self, new_title):
        self.setWindowTitle(new_title + " - EasyEdit")

    def update_status_bar_text(self):
        self.status_bar.showMessage("Line {}, Column {}".format(self.tab_bar.currentWidget().textCursor().blockNumber(),
                                                                self.tab_bar.currentWidget().textCursor().columnNumber()))


if __name__ == '__main__':
    application = QApplication(sys.argv)

    editor = Editor()

    sys.exit(application.exec_())
