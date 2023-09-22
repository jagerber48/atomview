import sys

from PyQt6 import QtWidgets, QtCore
from pyvistaqt import MainWindow

from ui_atomviewwindow import Ui_AtomViewWindow
from atomview.atom_wavefunction import get_wavefunction_prob_contour_mesh, \
    get_wavefunction_volume_mesh


class AtomViewWindow(MainWindow):
    nlm_update_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_AtomViewWindow()
        self.ui.setupUi(self)

        self.signal_close.connect(self.ui.plotter.close)

        self.n = 1
        self.l = 0
        self.m = 0
        self.real = self.ui.real_checkBox.isChecked()
        self.clip = self.ui.clip_checkBox.isChecked()
        self.contour_mode = self.ui.contour_radioButton.isChecked()

        self.ui.plotter.camera.position = (10, 10, 10)
        self.ui.plotter.set_background('black')
        self.update_mesh()

        self.ui.n_comboBox.activated.connect(self.update_n)
        self.ui.l_comboBox.activated.connect(self.update_l)
        self.ui.m_comboBox.activated.connect(self.update_m)

        self.ui.real_checkBox.stateChanged.connect(self.update_real)
        self.ui.clip_checkBox.stateChanged.connect(self.update_clip)

        self.ui.buttonGroup.buttonClicked.connect(self.update_mode)

        self.show()

    def update_mode(self):
        self.contour_mode = self.ui.contour_radioButton.isChecked()
        self.update_mesh()

    def update_mesh(self):
        camera_position = self.ui.plotter.camera.position
        self.ui.plotter.clear_actors()

        if self.contour_mode:
            mesh = get_wavefunction_prob_contour_mesh(self.n, self.l, self.m,
                                                      num_pts=100,
                                                      real=self.real,
                                                      clip=self.clip)
            self.ui.plotter.add_mesh(mesh, scalars='rgba', rgb=True,
                                     specular=1, diffuse=1, ambient=0.3)
        else:
            mesh = get_wavefunction_volume_mesh(self.n, self.l, self.m,
                                                num_pts=100, real=self.real,
                                                max_opacity=1)
            self.ui.plotter.add_volume(mesh, scalars='rgba', mapper='gpu')

        self.ui.plotter.camera.position = camera_position

    def update_real(self):
        self.real = self.ui.real_checkBox.isChecked()
        self.update_mesh()

    def update_clip(self):
        self.clip = self.ui.clip_checkBox.isChecked()
        self.update_mesh()

    def update_n(self):
        self.n = int(self.ui.n_comboBox.currentText())

        self.ui.l_comboBox.clear()
        self.ui.l_comboBox.addItems(map(str, range(self.n)))
        if self.l < self.n:
            self.ui.l_comboBox.setCurrentIndex(self.l)
        else:
            self.ui.l_comboBox.setCurrentIndex(self.n - 1)

        self.update_l()

    def update_l(self):
        self.l = int(self.ui.l_comboBox.currentText())

        self.ui.m_comboBox.clear()
        self.ui.m_comboBox.addItems(map(str, range(-self.l, self.l + 1)))
        if self.m < -self.l:
            self.ui.m_comboBox.setCurrentIndex(0)
        elif self.m > self.l:
            self.ui.m_comboBox.setCurrentIndex(2 * self.l)
        else:
            self.ui.m_comboBox.setCurrentIndex(self.l + self.m)

        self.update_m()

    def update_m(self):
        self.m = int(self.ui.m_comboBox.currentText())
        self.update_mesh()


if __name__ == '__main__':
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    window = AtomViewWindow()
    app.exec()
