from PyQt5.Qsci import QsciScintilla, QsciLexerPython


class TextArea(QsciScintilla):
    def __init__(self):
        super().__init__()

        self.filePath = "Untitled"

        self.pythonLexer = QsciLexerPython(self)
        self.setLexer(self.pythonLexer)
        self.setMargins(1)
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setUtf8(True)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(False)
        self.setAutoIndent(True)

    def changeMarginWidth(self):
        numLines = self.lines()

        self.setMarginWidth(0, "00" * len(str(numLines)))

    def updateFont(self, newFont):
        self.lexer().setFont(newFont)
