from enum import Enum

from PyQt6 import QtWidgets, QtCore
from pyvistaqt import MainWindow

from atomview.ui_atomviewwindow import Ui_AtomViewWindow
from atomview.atom_wavefunction import get_wavefunction_prob_contour_mesh, \
    get_wavefunction_volume_mesh


class VisMode(Enum):
    CONTOUR = 'contour'
    VOLUME = 'volume'


class AtomViewWindow(MainWindow):
    nlm_update_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_AtomViewWindow()
        self.ui.setupUi(self)

        self.signal_close.connect(self.ui.plotter.close)

        self.n = int(self.ui.n_comboBox.currentText())
        self.l = int(self.ui.l_comboBox.currentText())
        self.m = int(self.ui.m_comboBox.currentText())
        self.real = self.ui.real_radioButton.isChecked()
        self.cutout = self.ui.cutout_checkBox.isChecked()
        self.vis_mode = self.get_vis_mode()
        self.contour_prob_threshold = float(self.ui.enclosed_prob_lineEdit.text())
        self.max_opacity = round(float(self.ui.max_opacity_lineEdit.text()), 2)
        self.opacity_exp = round(float(self.ui.opacity_exponent_lineEdit.text()), 2)

        self.ui.plotter.camera.position = (10, 10, 10)
        self.ui.plotter.set_background('black')
        self.update_mesh()

        self.ui.n_comboBox.activated.connect(self.update_n)
        self.ui.l_comboBox.activated.connect(self.update_l)
        self.ui.m_comboBox.activated.connect(self.update_m)

        self.ui.real_complex_buttonGroup.buttonToggled.connect(self.update_real)
        self.ui.cutout_checkBox.stateChanged.connect(self.update_cutout)

        self.ui.mode_tabWidget.currentChanged.connect(self.update_vis_mode)
        self.ui.enclosed_prob_lineEdit.editingFinished.connect(
            self.contour_prob_threshold_updated
        )
        self.ui.max_opacity_lineEdit.editingFinished.connect(
            self.max_opacity_updated
        )
        self.ui.opacity_exponent_lineEdit.editingFinished.connect(
            self.opacity_exp_updated
        )
        self.show()

    def get_vis_mode(self):
        if self.ui.mode_tabWidget.currentIndex() == 0:
            return VisMode.CONTOUR
        elif self.ui.mode_tabWidget.currentIndex() == 1:
            return VisMode.VOLUME
        else:
            raise ValueError

    def contour_prob_threshold_updated(self):
        try:
            new_threshold = round(
                float(self.ui.enclosed_prob_lineEdit.text()), 2
            )
            if not 0 < new_threshold < 1:
                raise ValueError
        except ValueError:
            pass
        else:
            self.contour_prob_threshold = new_threshold
            self.update_mesh()
        finally:
            self.ui.enclosed_prob_lineEdit.setText(
                f'{self.contour_prob_threshold:.2f}')

    def max_opacity_updated(self):
        try:
            new_max_opacity = round(
                float(self.ui.max_opacity_lineEdit.text()), 2
            )
            if new_max_opacity <= 0:
                raise ValueError
        except ValueError:
            pass
        else:
            self.max_opacity = new_max_opacity
            self.update_mesh()
        finally:
            self.ui.max_opacity_lineEdit.setText(
                f'{self.max_opacity:.2f}')

    def opacity_exp_updated(self):
        try:
            new_opacity_exp = round(
                float(self.ui.opacity_exponent_lineEdit.text()), 2
            )
            if new_opacity_exp <= 0:
                raise ValueError
        except ValueError:
            pass
        else:
            self.opacity_exp = new_opacity_exp
            self.update_mesh()
        finally:
            self.ui.opacity_exponent_lineEdit.setText(
                f'{self.opacity_exp:.2f}')

    def update_vis_mode(self):
        self.vis_mode = self.get_vis_mode()
        self.update_mesh()

    def update_mesh(self):
        camera_position = self.ui.plotter.camera.position
        self.ui.plotter.clear_actors()

        if self.vis_mode is VisMode.CONTOUR:
            mesh = get_wavefunction_prob_contour_mesh(
                self.n, self.l, self.m,
                prob_threshold_list=[self.contour_prob_threshold],
                num_pts=100,
                real=self.real,
                clip=self.cutout)
            try:
                self.ui.plotter.add_mesh(
                    mesh, scalars='rgba', rgb=True,
                    specular=1, diffuse=1, ambient=0.3)
            except ValueError:
                self.ui.plotter.add_text('Empty mesh.\n'
                                         'Choose a threshold\n'
                                         'further away from 0 or 1.',
                                         font_size=12,
                                         color='red',
                                         position='lower_edge')
        elif self.vis_mode is VisMode.VOLUME:
            mesh = get_wavefunction_volume_mesh(self.n, self.l, self.m,
                                                num_pts=100, real=self.real,
                                                max_opacity=self.max_opacity,
                                                opacity_exp=self.opacity_exp)
            self.ui.plotter.add_volume(mesh, scalars='rgba', mapper='gpu')
        else:
            raise NotImplementedError

        self.ui.plotter.camera.position = camera_position

    def update_real(self):
        self.real = self.ui.real_radioButton.isChecked()
        self.update_mesh()

    def update_cutout(self):
        self.cutout = self.ui.cutout_checkBox.isChecked()
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
