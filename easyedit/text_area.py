from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTextEdit


class TextArea(QTextEdit):
    unsaved_changes = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.unsaved_changes = False

        self.setAcceptRichText(False)

        self.textChanged.connect(self.set_unsaved_changes)

    def set_unsaved_changes(self):
        self.unsaved_changes = True
