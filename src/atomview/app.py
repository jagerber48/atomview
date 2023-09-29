import sys
import ctypes
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from atomview.ui.atomviewwindow import AtomViewWindow


def run():
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError as e:
        print(e)
        base_path = Path.cwd()

    app = QApplication([])

    icon_path = str(Path(base_path, 'icon/favicon.ico'))
    app.setWindowIcon(QIcon(icon_path))
    myappid = u'atomview_app'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = AtomViewWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    run()
