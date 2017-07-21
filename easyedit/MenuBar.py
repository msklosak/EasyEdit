from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenuBar


class MenuBar(QMenuBar):
    newFile = pyqtSignal()
    openFile = pyqtSignal()
    saveFile = pyqtSignal()
    saveFileAs = pyqtSignal()

    undoEdit = pyqtSignal()
    redoEdit = pyqtSignal()
    cutText = pyqtSignal()
    copyText = pyqtSignal()
    pasteText = pyqtSignal()

    changeFont = pyqtSignal()

    openAboutDialog = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.fileMenu = None
        self.editMenu = None
        self.settingsMenu = None
        self.helpMenu = None

        self.changeFileMenu()
        self.createEditMenu()
        self.createSettingsMenu()
        self.createHelpMenu()

    def changeFileMenu(self):
        newFileAction = QAction(QIcon("new.png"), 'New File', self)
        newFileAction.setShortcut("Ctrl+N")
        newFileAction.setStatusTip("New file")
        newFileAction.triggered.connect(lambda: self.newFile.emit())

        openFileAction = QAction(QIcon("open.png"), 'Open File', self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Open file")
        openFileAction.triggered.connect(lambda: self.openFile.emit())

        saveFileAction = QAction(QIcon("save.png"), 'Save File', self)
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.setStatusTip("Save file")
        saveFileAction.triggered.connect(lambda: self.saveFile.emit())

        saveFileAsAction = QAction(QIcon("save.png"), 'Save File As', self)
        saveFileAsAction.setShortcut("Ctrl+Shift+S")
        saveFileAsAction.setStatusTip("Save file as")
        saveFileAsAction.triggered.connect(lambda: self.saveFileAs.emit())

        quitAction = QAction(QIcon("quit.png"), 'Quit', self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip("Quit EasyEdit")
        quitAction.triggered.connect(lambda: QApplication.quit())

        self.fileMenu = self.addMenu("File")
        self.fileMenu.addAction(newFileAction)
        self.fileMenu.addAction(openFileAction)
        self.fileMenu.addAction(saveFileAction)
        self.fileMenu.addAction(quitAction)

    def createEditMenu(self):
        undoEditAction = QAction(QIcon("icons/undo.png"), "Undo", self)
        undoEditAction.setStatusTip("Undo last edit")
        undoEditAction.setShortcut("Ctrl+Z")
        undoEditAction.triggered.connect(lambda: self.undoEdit.emit())

        redoEditAction = QAction(QIcon("icons/redo.png"), "Redo", self)
        redoEditAction.setStatusTip("Redo last edit")
        redoEditAction.setShortcut("Ctrl+Shift+Z")
        redoEditAction.triggered.connect(lambda: self.redoEdit.emit())

        cutTextAction = QAction(QIcon("icons/cut.png"), "Cut Selection", self)
        cutTextAction.setStatusTip("Cut text to clipboard")
        cutTextAction.setShortcut("Ctrl+X")
        cutTextAction.triggered.connect(lambda: self.cutText.emit())

        copyTextAction = QAction(QIcon("icons/copy.png"), "Copy Selection", self)
        copyTextAction.setStatusTip("Copy text to clipboard")
        copyTextAction.setShortcut("Ctrl+C")
        copyTextAction.triggered.connect(lambda: self.copyText.emit())

        pasteTextAction = QAction(QIcon("icons/paste.png"), "Paste", self)
        pasteTextAction.setStatusTip("Paste text from clipboard")
        pasteTextAction.setShortcut("Ctrl+V")
        pasteTextAction.triggered.connect(lambda: self.pasteText.emit())

        self.editMenu = self.addMenu("Edit")
        self.editMenu.addAction(undoEditAction)
        self.editMenu.addAction(redoEditAction)
        self.editMenu.addAction(cutTextAction)
        self.editMenu.addAction(copyTextAction)
        self.editMenu.addAction(pasteTextAction)

    def createSettingsMenu(self):
        changeFontAction = QAction(QIcon("icons/font.png"), "Change Font", self)
        changeFontAction.setStatusTip("Change font")
        changeFontAction.triggered.connect(lambda: self.changeFont.emit())

        self.settingsMenu = self.addMenu("Settings")
        self.settingsMenu.addAction(changeFontAction)

    def createHelpMenu(self):
        aboutDialogAction = QAction('About', self)
        aboutDialogAction.setStatusTip('About the application.')
        aboutDialogAction.setShortcut('CTRL+H')
        aboutDialogAction.triggered.connect(lambda: self.openAboutDialog.emit())

        self.helpMenu = self.addMenu("Help")
        self.helpMenu.addAction(aboutDialogAction)
