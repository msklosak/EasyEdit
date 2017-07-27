from PyQt5.Qsci import QsciScintilla, QsciLexerBash, QsciLexerBatch, QsciLexerCMake, QsciLexerCoffeeScript, \
    QsciLexerCPP, QsciLexerCSharp, QsciLexerCSS, QsciLexerD, QsciLexerFortran, QsciLexerHTML, QsciLexerJava, \
    QsciLexerJavaScript, QsciLexerJSON, QsciLexerLua, QsciLexerMakefile, QsciLexerMarkdown, QsciLexerMatlab, \
    QsciLexerPascal, QsciLexerPerl, QsciLexerPython, QsciLexerRuby, QsciLexerSQL, QsciLexerTeX, QsciLexerYAML, \
    QsciLexerXML


class TextArea(QsciScintilla):
    def __init__(self):
        super().__init__()

        self.languageToLexer = {
            'Bash': QsciLexerBash,
            'Batch': QsciLexerBatch,
            'CMake': QsciLexerCMake,
            'CoffeeScript': QsciLexerCoffeeScript,
            'C++': QsciLexerCPP,
            'C#': QsciLexerCSharp,
            'CSS': QsciLexerCSS,
            'D': QsciLexerD,
            'Fortran': QsciLexerFortran,
            'HTML': QsciLexerHTML,
            'Java': QsciLexerJava,
            'JavaScript': QsciLexerJavaScript,
            'JSON': QsciLexerJSON,
            'Lua': QsciLexerLua,
            'Makefile': QsciLexerMakefile,
            'Markdown': QsciLexerMarkdown,
            'Matlab': QsciLexerMatlab,
            'Pascal': QsciLexerPascal,
            'Perl': QsciLexerPerl,
            'Python': QsciLexerPython,
            'Ruby': QsciLexerRuby,
            'SQL': QsciLexerSQL,
            'TeX': QsciLexerTeX,
            'YAML': QsciLexerYAML,
            'XML': QsciLexerXML
        }

        self.filePath = "Untitled"
        self.currentLanguage = None
        self.setMargins(1)
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setUtf8(True)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(False)
        self.setAutoIndent(True)

    def changeLexer(self, lexer):
        if lexer is not None:
            newLexer = self.languageToLexer.get(lexer)(self)
            self.setLexer(newLexer)
            self.currentLanguage = lexer

    def changeMarginWidth(self):
        numLines = self.lines()

        self.setMarginWidth(0, "00" * len(str(numLines)))

    def updateFont(self, newFont):
        if self.currentLanguage is not None:
            self.lexer().setFont(newFont)
