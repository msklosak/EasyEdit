import sys
from os.path import split

from PyQt5.QtWidgets import QApplication, QFileDialog, QFontDialog, QMainWindow

from easyedit.AboutDialog import AboutDialog
from easyedit.MenuBar import MenuBar
from easyedit.TabBar import TabBar


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Untitled - EasyEdit")
        self.resize(600, 800)

        self.aboutDialog = AboutDialog()

        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)

        self.tabBar = TabBar()
        self.setCentralWidget(self.tabBar)

        self.statusBar = self.statusBar()

        self.createStatusBar()

        self.configureSignals()

        self.show()

    def closeEvent(self, event):
        while self.tabBar.count() > 0:
            self.tabBar.closeTab(0)

    def configureSignals(self):
        # FILE TAB
        self.menuBar.newFile.connect(self.tabBar.openTab)
        self.menuBar.openFile.connect(self.openFile)
        self.menuBar.saveFile.connect(self.saveFile)
        self.menuBar.saveFileAs.connect(self.saveFile)

        # EDIT TAB
        self.menuBar.undoEdit.connect(self.tabBar.currentWidget().undo)
        self.menuBar.redoEdit.connect(self.tabBar.currentWidget().redo)
        self.menuBar.cutText.connect(self.tabBar.currentWidget().cut)
        self.menuBar.copyText.connect(self.tabBar.currentWidget().copy)
        self.menuBar.pasteText.connect(self.tabBar.currentWidget().paste)

        # SETTINGS TAB
        self.menuBar.changeFont.connect(self.change_font)

        # HELP TAB
        self.menuBar.aboutDialog.connect(lambda: self.aboutDialog.exec_())

        # TAB BAR
        self.tabBar.currentChanged.connect(self.tabChanged)

        # TEXT AREA
        self.tabBar.currentWidget().cursorMoved.connect(self.updateStatusBarText)

    def change_font(self):
        font = QFontDialog().getFont()[0]

        self.setFont(font)

        current_tab = 0
        while current_tab > self.tabBar.count():
            self.tabBar.widget(current_tab).updateFont(font)

    def create_text_edit(self):
        self.setCentralWidget(self.text_edit)

        self.text_edit.textChanged.connect(self.set_unsaved_changes)

    def createStatusBar(self):
        self.updateStatusBarText()

    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File")[0]

        if file_name != "":
            with open(file_name, 'r') as file:
                self.tabBar.currentWidget().setText(file.read())

            shortened_file_name = split(file_name)[1]

            self.tabBar.currentFilePath = file_name
            self.tabBar.setTabText(self.tabBar.currentIndex(), shortened_file_name)
            self.updateWindowTitle()

    def saveFile(self):
        if self.tabBar.currentFilePath != "Untitled":
            file_name = self.tabBar.currentFilePath
        else:
            file_name = QFileDialog.getSaveFileName(self, "Save File", None, "Text Files (*.txt);;All Files (*)")[0]

            if file_name != "":
                shortened_file_name = split(file_name)[1]

                self.tabBar.setTabText(self.tabBar.currentIndex(), shortened_file_name)
                self.updateWindowTitle()

        if file_name != "":
            text = self.tabBar.currentWidget().toPlainText()

            with open(file_name, 'w') as file:
                file.write(text)

    def tabChanged(self):
        self.tabBar.currentWidget().cursorMoved.connect(self.updateStatusBarText)

        self.updateWindowTitle()
        self.updateStatusBarText()

    def updateWindowTitle(self):
        self.setWindowTitle(self.tabBar.tabText(self.tabBar.currentIndex()) + " - EasyEdit")

    def updateStatusBarText(self):
        cursorLine = self.tabBar.currentWidget().textCursor().blockNumber()
        cursorColumn = self.tabBar.currentWidget().textCursor().columnNumber()

        self.statusBar.showMessage("Line {}, Column {}".format(cursorLine, cursorColumn))


if __name__ == '__main__':
    application = QApplication(sys.argv)

    editor = Editor()

    sys.exit(application.exec_())
