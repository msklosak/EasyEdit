from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QTabWidget

from easyedit.text_area import TextArea


class TabBar(QTabWidget):
    tab_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setMovable(True)
        self.setTabsClosable(True)

        self.open_tab()

        self.currentChanged.connect(self.change_tab)
        self.tabCloseRequested.connect(self.close_tab)

    def get_current_tab(self):
        return self.currentWidget()

    def open_tab(self):
        text_widget = TextArea()

        if self.count() == 0:
            self.addTab(text_widget, "Untitled")
        else:
            self.addTab(text_widget, "Untitled ({})".format(self.count() + 1))

        self.setCurrentIndex(self.count() - 1)

    def change_tab(self, index):
        self.tab_changed.emit(self.tabText(self.currentIndex()))

    def close_tab(self, index):
        if self.widget(index).unsaved_changes:
            # UNSAVED DIALOG
            pass

        self.removeTab(index)

        if self.count() == 0:
            QApplication.quit()
