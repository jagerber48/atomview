import sys
import ctypes

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from atomview.atomviewwindow import AtomViewWindow


def run():
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon('icon/favicon.ico'))
    myappid = u'atomview_app'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    ex = AtomViewWindow()
    app.exec()


if __name__ == '__main__':
    run()
