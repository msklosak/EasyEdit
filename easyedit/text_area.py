from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QTextEdit


class TextArea(QTextEdit):
    unsaved_changes = pyqtSignal(str)
    cursor_position_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.unsaved_changes = False

        self.setAcceptRichText(False)

        self.update_font(self.font())

        self.textChanged.connect(self.set_unsaved_changes)
        self.cursorPositionChanged.connect(self.cursor_position_changed)

    def update_font(self, new_font):
        self.setFont(new_font)

        font_metrics = QFontMetrics(new_font)

        self.setTabStopWidth(font_metrics.width("    "))

    def set_unsaved_changes(self):
        self.unsaved_changes = True
