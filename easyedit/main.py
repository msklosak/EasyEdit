import sys

from easyedit.Editor import Editor
from PyQt5.QtWidgets import QApplication


def main():
    application = QApplication(sys.argv)

    Editor()

    sys.exit(application.exec_())


if __name__ == '__main__':
    main()
