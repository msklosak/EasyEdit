from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenuBar


class MenuBar(QMenuBar):
    new_file = pyqtSignal()
    open_file = pyqtSignal()
    save_file = pyqtSignal()
    save_file_as = pyqtSignal()

    undo_edit = pyqtSignal()
    redo_edit = pyqtSignal()
    cut_text = pyqtSignal()
    copy_text = pyqtSignal()
    paste_text = pyqtSignal()

    change_font = pyqtSignal()

    about_dialog = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.file_menu = None
        self.edit_menu = None
        self.settings_menu = None
        self.help_menu = None

        self.create_file_menu()
        self.create_edit_menu()
        self.create_settings_menu()
        self.create_help_menu()

    def create_file_menu(self):
        new_file_action = QAction(QIcon("new.png"), 'New File', self)
        new_file_action.setShortcut("Ctrl+N")
        new_file_action.setStatusTip("New file")
        new_file_action.triggered.connect(lambda: self.new_file.emit())

        open_file_action = QAction(QIcon("open.png"), 'Open File', self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(lambda: self.open_file.emit())

        save_file_action = QAction(QIcon("save.png"), 'Save File', self)
        save_file_action.setShortcut("Ctrl+S")
        save_file_action.setStatusTip("Save file")
        save_file_action.triggered.connect(lambda: self.save_file.emit())

        save_file_as_action = QAction(QIcon("save.png"), 'Save File As', self)
        save_file_as_action.setShortcut("Ctrl+Shift+S")
        save_file_as_action.setStatusTip("Save file as")
        save_file_as_action.triggered.connect(lambda: self.save_file_as.emit())

        quit_action = QAction(QIcon("quit.png"), 'Quit', self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Quit EasyEdit")
        quit_action.triggered.connect(lambda: QApplication.quit())

        self.file_menu = self.addMenu("File")
        self.file_menu.addAction(new_file_action)
        self.file_menu.addAction(open_file_action)
        self.file_menu.addAction(save_file_action)
        self.file_menu.addAction(quit_action)

    def create_edit_menu(self):
        undo_edit_action = QAction(QIcon("icons/undo.png"), "Undo", self)
        undo_edit_action.setStatusTip("Undo last edit")
        undo_edit_action.setShortcut("Ctrl+Z")
        undo_edit_action.triggered.connect(lambda: self.undo_edit.emit())

        redo_edit_action = QAction(QIcon("icons/redo.png"), "Redo", self)
        redo_edit_action.setStatusTip("Redo last edit")
        redo_edit_action.setShortcut("Ctrl+Shift+Z")
        redo_edit_action.triggered.connect(lambda: self.redo_edit.emit())

        cut_text_action = QAction(QIcon("icons/cut.png"), "Cut Selection", self)
        cut_text_action.setStatusTip("Cut text to clipboard")
        cut_text_action.setShortcut("Ctrl+X")
        cut_text_action.triggered.connect(lambda: self.cut_text.emit())

        copy_text_action = QAction(QIcon("icons/copy.png"), "Copy Selection", self)
        copy_text_action.setStatusTip("Copy text to clipboard")
        copy_text_action.setShortcut("Ctrl+C")
        copy_text_action.triggered.connect(lambda: self.copy_text.emit())

        paste_text_action = QAction(QIcon("icons/paste.png"), "Paste", self)
        paste_text_action.setStatusTip("Paste text from clipboard")
        paste_text_action.setShortcut("Ctrl+V")
        paste_text_action.triggered.connect(lambda: self.paste_text.emit())

        self.edit_menu = self.addMenu("Edit")
        self.edit_menu.addAction(undo_edit_action)
        self.edit_menu.addAction(redo_edit_action)
        self.edit_menu.addAction(cut_text_action)
        self.edit_menu.addAction(copy_text_action)
        self.edit_menu.addAction(paste_text_action)

    def create_settings_menu(self):
        change_font_action = QAction(QIcon("icons/font.png"), "Change Font", self)
        change_font_action.setStatusTip("Change font")
        change_font_action.triggered.connect(lambda: self.change_font.emit())

        self.settings_menu = self.addMenu("Settings")
        self.settings_menu.addAction(change_font_action)

    def create_help_menu(self):
        about_dialog_action = QAction('About', self)
        about_dialog_action.setStatusTip('About the application.')
        about_dialog_action.setShortcut('CTRL+H')
        about_dialog_action.triggered.connect(lambda: self.about_dialog.emit())

        self.help_menu = self.addMenu("Help")
        self.help_menu.addAction(about_dialog_action)
