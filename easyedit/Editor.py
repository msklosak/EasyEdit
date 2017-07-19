import sys
from os.path import split

from PyQt5.QtCore import QSettings, QPoint, QSize
from PyQt5.QtWidgets import QApplication, QFileDialog, QFontDialog, QMainWindow

from easyedit.AboutDialog import AboutDialog
from easyedit.MenuBar import MenuBar
from easyedit.TabBar import TabBar


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.readWindowSettings()

        self.aboutDialog = AboutDialog()

        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)

        self.tabBar = TabBar()
        self.readTabBarSettings()
        self.setCentralWidget(self.tabBar)

        self.statusBar = self.statusBar()

        self.createStatusBar()

        self.configureSignals()

        self.show()

    def readWindowSettings(self):
        settings = QSettings("msklosak", "EasyEdit")

        settings.beginGroup("Editor")
        self.resize(settings.value("size", QSize(600, 800)))
        self.move(settings.value("pos", QPoint(0, 0)))
        self.setFont(settings.value("font", self.font()))
        settings.endGroup()

    def writeWindowSettings(self):
        settings = QSettings("msklosak", "EasyEdit")

        settings.beginGroup("Editor")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.setValue("font", self.font())
        settings.endGroup()

    def readTabBarSettings(self):
        settings = QSettings("msklosak", "EasyEdit")
        settings.beginGroup("Tab Bar")

        savedTabs = settings.value("openedTabs", list("Untitled"))
        if savedTabs is None:
            self.tabBar.openTab()
        else:
            for fileName in savedTabs:
                if fileName != "Untitled":
                    self.tabBar.openTab()
                    self.openFile(fileName)

        self.tabBar.setCurrentIndex(int(settings.value("currentTab", 0)))

        settings.endGroup()

    def writeTabBarSettings(self):
        openTabs = []

        currentTab = 0
        while currentTab < self.tabBar.count():
            openTabs.append(self.tabBar.widget(currentTab).filePath)
            currentTab += 1

        settings = QSettings("msklosak", "EasyEdit")
        settings.beginGroup("Tab Bar")
        settings.setValue("openedTabs", openTabs)
        settings.setValue("currentTab", self.tabBar.currentIndex())
        settings.endGroup()

    def closeEvent(self, event):
        self.writeTabBarSettings()
        self.writeWindowSettings()

        while self.tabBar.count() > 0:
            self.tabBar.closeTab(0)

    def configureSignals(self):
        # FILE TAB
        self.menuBar.newFile.connect(self.tabBar.openTab)
        self.menuBar.openFile.connect(self.openFileDialog)
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

    def openFile(self, fileName):
        with open(fileName, 'r') as file:
            self.tabBar.currentWidget().setText(file.read())

        shortened_file_name = split(fileName)[1]

        self.tabBar.currentWidget().filePath = fileName
        self.tabBar.setTabText(self.tabBar.currentIndex(), shortened_file_name)
        self.updateWindowTitle()

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File")[0]

        if file_name != "":
            with open(file_name, 'r') as file:
                self.tabBar.currentWidget().setText(file.read())

            shortened_file_name = split(file_name)[1]

            self.tabBar.currentWidget().filePath = file_name
            self.tabBar.setTabText(self.tabBar.currentIndex(), shortened_file_name)
            self.updateWindowTitle()

    def saveFile(self):
        if self.tabBar.currentWidget().filePath != "Untitled":
            file_name = self.tabBar.currentWidget().filePath
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
