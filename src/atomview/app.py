import sys
import ctypes
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from atomview.atomviewwindow import AtomViewWindow


def run():
    app = QApplication(sys.argv)

    # Code to setup windows icon for jkam
    # app.setWindowIcon(QIcon('package/imagedata/favicon.ico'))
    myappid = u'jkam_app'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    ex = AtomViewWindow()
    app.exec()


if __name__ == '__main__':
    run()
