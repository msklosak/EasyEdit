import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog

from easyedit import Editor


@pytest.fixture
def window(qtbot):
    """Pass the application to the test functions via a pytest fixture."""
    newWindow = Editor.Editor()
    qtbot.add_widget(newWindow)
    newWindow.show()
    return newWindow


def testWindowTitle(window):
    """Check that the window title shows as declared."""
    assert window.windowTitle() == 'Untitled - EasyEdit'


def testWindowGeometry(window):
    """Check that the window width and height are set as declared."""
    assert window.width() == 600
    assert window.height() == 800


def testOpenFile(window, qtbot, mock):
    """Test the Open File item of the File submenu.

    Qtbot clicks on the file sub menu and then navigates to the Open File item. Mock creates
    an object to be passed to the QFileDialog.
    """
    qtbot.mouseClick(window.menuBar.fileMenu, Qt.LeftButton)
    qtbot.keyClick(window.menuBar.fileMenu, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('', ''))
    qtbot.keyClick(window.menuBar.fileMenu, Qt.Key_Enter)


def test_about_dialog(window, qtbot, mock):
    """Test the About item of the Help submenu.

    Qtbot clicks on the help sub menu and then navigates to the About item. Mock creates
    a QDialog object to be used for the test.
    """
    qtbot.mouseClick(window.menuBar.helpMenu, Qt.LeftButton)
    qtbot.keyClick(window.menuBar.helpMenu, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.menuBar.helpMenu, Qt.Key_Enter)
