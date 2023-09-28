from enum import Enum

from PyQt6 import QtCore
from pyvistaqt import MainWindow

from ui.ui_atomviewwindow import Ui_AtomViewWindow
from atomview.atom_wavefunction import get_wavefunction_prob_contour_mesh, \
    get_wavefunction_volume_mesh


class VisMode(Enum):
    CONTOUR = 'contour'
    MULTI_CONTOUR = 'multi_contour'
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
        self.vis_mode = VisMode.CONTOUR
        self.contour_prob_threshold = self.ui.enclosed_prob_doubleSpinBox.value()
        self.max_opacity = self.ui.max_opacity_doubleSpinBox.value()
        self.opacity_exp = self.ui.opacity_exp_doubleSpinBox.value()
        self.mc_threshold_list = self.get_multi_contour_list()

        self.ui.plotter.camera.position = (10, 10, 10)
        self.ui.plotter.set_background('black')
        self.update_mesh()

        self.ui.n_comboBox.activated.connect(self.update_n)
        self.ui.l_comboBox.activated.connect(self.update_l)
        self.ui.m_comboBox.activated.connect(self.update_m)

        self.ui.real_complex_buttonGroup.buttonToggled.connect(self.update_real)
        self.ui.cutout_checkBox.stateChanged.connect(self.update_cutout)

        self.ui.vismode_buttonGroup.buttonToggled.connect(self.update_vis_mode)

        self.ui.enclosed_prob_doubleSpinBox.editingFinished.connect(
            self.contour_prob_threshold_updated
        )
        self.ui.max_opacity_doubleSpinBox.editingFinished.connect(
            self.max_opacity_updated
        )
        self.ui.opacity_exp_doubleSpinBox.editingFinished.connect(
            self.opacity_exp_updated
        )

        self.ui.mc_checkBox_0.toggled.connect(self.mc_checkbox_0_toggled)
        self.ui.mc_checkBox_1.toggled.connect(self.mc_checkbox_1_toggled)
        self.ui.mc_checkBox_2.toggled.connect(self.mc_checkbox_2_toggled)
        self.ui.mc_checkBox_3.toggled.connect(self.mc_checkbox_3_toggled)
        self.ui.mc_checkBox_4.toggled.connect(self.mc_checkbox_4_toggled)

        mc_spinbox_list = [
            self.ui.mc_doubleSpinBox_0,
            self.ui.mc_doubleSpinBox_1,
            self.ui.mc_doubleSpinBox_2,
            self.ui.mc_doubleSpinBox_3,
            self.ui.mc_doubleSpinBox_4
        ]

        for spinbox in mc_spinbox_list:
            spinbox.editingFinished.connect(
                self.multi_contour_prob_threshold_updated)

    def mc_checkbox_0_toggled(self):
        self.ui.mc_doubleSpinBox_0.setEnabled(
            self.ui.mc_checkBox_0.isChecked())
        self.mc_threshold_list = self.get_multi_contour_list()
        self.update_mesh()

    def mc_checkbox_1_toggled(self):
        self.ui.mc_doubleSpinBox_1.setEnabled(
            self.ui.mc_checkBox_1.isChecked())
        self.mc_threshold_list = self.get_multi_contour_list()
        self.update_mesh()

    def mc_checkbox_2_toggled(self):
        self.ui.mc_doubleSpinBox_2.setEnabled(
            self.ui.mc_checkBox_2.isChecked())
        self.mc_threshold_list = self.get_multi_contour_list()
        self.update_mesh()

    def mc_checkbox_3_toggled(self):
        self.ui.mc_doubleSpinBox_3.setEnabled(
            self.ui.mc_checkBox_3.isChecked())
        self.mc_threshold_list = self.get_multi_contour_list()
        self.update_mesh()

    def mc_checkbox_4_toggled(self):
        self.ui.mc_doubleSpinBox_4.setEnabled(
            self.ui.mc_checkBox_4.isChecked())
        self.mc_threshold_list = self.get_multi_contour_list()
        self.update_mesh()

    def get_multi_contour_list(self):
        multi_contour_dict = {
            0: (self.ui.mc_checkBox_0, self.ui.mc_doubleSpinBox_0),
            1: (self.ui.mc_checkBox_1, self.ui.mc_doubleSpinBox_1),
            2: (self.ui.mc_checkBox_2, self.ui.mc_doubleSpinBox_2),
            3: (self.ui.mc_checkBox_3, self.ui.mc_doubleSpinBox_3),
            4: (self.ui.mc_checkBox_4, self.ui.mc_doubleSpinBox_4),
        }
        mc_threshold_list = list()
        for num, (checkbox, spin_box) in multi_contour_dict.items():
            if checkbox.isChecked():
                mc_threshold_list.append(spin_box.value())
        return mc_threshold_list

    def contour_prob_threshold_updated(self):
        old_contour_prob_threshold = self.contour_prob_threshold
        self.contour_prob_threshold = self.ui.enclosed_prob_doubleSpinBox.value()
        if self.contour_prob_threshold != old_contour_prob_threshold:
            self.update_mesh()

    def multi_contour_prob_threshold_updated(self):
        self.mc_threshold_list = self.get_multi_contour_list()
        self.update_mesh()

    def max_opacity_updated(self):
        old_max_opacity = self.max_opacity
        self.max_opacity = self.ui.max_opacity_doubleSpinBox.value()
        if self.max_opacity != old_max_opacity:
            self.update_mesh()

    def opacity_exp_updated(self):
        old_opacity_exp = self.opacity_exp
        self.opacity_exp = self.ui.opacity_exp_doubleSpinBox.value()
        if self.opacity_exp != old_opacity_exp:
            self.update_mesh()

    def update_vis_mode(self):
        if self.ui.contour_radioButton.isChecked():
            self.vis_mode = VisMode.CONTOUR
            self.ui.mode_stackedWidget.setCurrentIndex(0)
        elif self.ui.multi_contour_radioButton.isChecked():
            self.vis_mode = VisMode.MULTI_CONTOUR
            self.ui.mode_stackedWidget.setCurrentIndex(1)
        elif self.ui.volume_radioButton.isChecked():
            self.vis_mode = VisMode.VOLUME
            self.ui.mode_stackedWidget.setCurrentIndex(2)
        self.repaint()
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
        elif self.vis_mode is VisMode.MULTI_CONTOUR:
            mesh = get_wavefunction_prob_contour_mesh(
                self.n, self.l, self.m,
                prob_threshold_list=self.mc_threshold_list,
                num_pts=100,
                mag_maps_to='a',
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
