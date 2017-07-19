from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QTextEdit


class TextArea(QTextEdit):
    cursorMoved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setAcceptRichText(False)

        self.filePath = "Untitled"

        self.updateFont(self.font())

        self.cursorPositionChanged.connect(self.cursorMoved)

    def updateFont(self, newFont):
        self.setFont(newFont)

        fontMetrics = QFontMetrics(newFont)

        self.setTabStopWidth(fontMetrics.width("    "))
