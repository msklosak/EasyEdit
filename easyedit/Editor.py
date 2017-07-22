import sys
from os.path import split

from PyQt5.QtCore import QSettings, QPoint, QSize, pyqtSlot
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

        self.changeFont(self.font())

        self.statusBar = self.statusBar()
        # self.updateStatusBarText()

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

        savedTabs = settings.value("openedTabs")
        if savedTabs is None:
            self.tabBar.openTab()
        else:
            for fileName in savedTabs:
                if fileName != "Untitled":
                    self.tabBar.openTab()
                    self.openFile(fileName)

        self.tabBar.setCurrentIndex(int(settings.value("currentTab", 0)))

        self.updateWindowTitle()

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
        self.menuBar.changeFont.connect(self.changeFontDialog)

        # HELP TAB
        self.menuBar.openAboutDialog.connect(lambda: self.aboutDialog.exec_())

        # TAB BAR
        self.tabBar.currentChanged.connect(self.tabChanged)

        # TEXT AREA
        # self.tabBar.currentWidget().cursorPositionChanged.connect(self.updateStatusBarText)

    def changeFont(self, newFont):
        self.setFont(newFont)

        currentTab = 0
        while currentTab < self.tabBar.count():
            self.tabBar.widget(currentTab).updateFont(newFont)
            currentTab += 1

    def changeFontDialog(self):
        font = QFontDialog().getFont()[0]

        self.changeFont(font)

    def openFile(self, fileName):
        with open(fileName, 'r') as file:
            self.tabBar.currentWidget().setText(file.read())

        shortenedFileName = split(fileName)[1]

        self.tabBar.currentWidget().filePath = fileName
        self.tabBar.setTabText(self.tabBar.currentIndex(), shortenedFileName)
        self.tabBar.currentWidget().changeMarginWidth()
        self.updateWindowTitle()

    def openFileDialog(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File")[0]

        if fileName != "":
            with open(fileName, 'r') as file:
                self.tabBar.currentWidget().setText(file.read())

                shortenedFileName = split(fileName)[1]

            self.tabBar.currentWidget().filePath = fileName
            self.tabBar.setTabText(self.tabBar.currentIndex(), shortenedFileName)
            self.tabBar.currentWidget().changeMarginWidth()
            self.updateWindowTitle()

    def saveFile(self):
        if self.tabBar.currentWidget().filePath != "Untitled":
            fileName = self.tabBar.currentWidget().filePath
        else:
            fileName = QFileDialog.getSaveFileName(self, "Save File", None, "Text Files (*.txt);;All Files (*)")[0]

            if fileName != "":
                shortenedFileName = split(fileName)[1]

                self.tabBar.setTabText(self.tabBar.currentIndex(), shortenedFileName)
                self.updateWindowTitle()

        if fileName != "":
            text = self.tabBar.currentWidget().text()

            with open(fileName, 'w') as file:
                file.write(text)

    def tabChanged(self):
        if self.tabBar.count() > 1:
            # self.tabBar.currentWidget().cursorPositionChanged.connect(self.updateStatusBarText)

            self.updateWindowTitle()

    def updateWindowTitle(self):
        self.setWindowTitle(self.tabBar.tabText(self.tabBar.currentIndex()) + " - EasyEdit")

    @pyqtSlot(int, int)
    def updateStatusBarText(self, line, column):
        self.statusBar.showMessage("Line {}, Column {}".format(line, column))


if __name__ == '__main__':
    application = QApplication(sys.argv)

    editor = Editor()

    sys.exit(application.exec_())
