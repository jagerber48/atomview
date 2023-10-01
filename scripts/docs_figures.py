from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
import matplotlib as mpl

from atomview.atom_wavefunction import (
    get_atomic_wavefunction, get_radial_part,
    get_wavefunction_prob_contour_mesh, get_wavefunction_volume_mesh)
from atomview.utils import complex_to_rgba

COLOR = 'white'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
mpl.rc('axes', edgecolor='white')

fig_dir = Path(Path.cwd(), 'figures', 'docs_figs')


def add_2d_fig(n, l, m, real=False, span=None,
               slice_plane='z', ax=None):
    if span is None:
        span = (1.5 * n)**2

    x_1d = np.linspace(-span, span, 100)
    y_1d = np.linspace(-span, span, 100)
    x, y = np.meshgrid(x_1d, y_1d, indexing='xy')
    z = np.zeros_like(x)

    if slice_plane == 'z':
        psi = get_atomic_wavefunction(x, y, z, n, l, m, real=real)
        x_label = 'x ($a_0$)'
        y_label = 'y ($a_0$)'
        slice_coords = '(x, y, 0)'
        x_min = -span
        x_max = +span
    elif slice_plane == 'x':
        psi = get_atomic_wavefunction(z, x, y, n, l, m, real=real)
        x_label = 'y ($a_0$)'
        y_label = 'z ($a_0$)'
        x_min = -span
        x_max = +span
        slice_coords = '(0, y, z)'
    elif slice_plane == 'y':
        psi = get_atomic_wavefunction(-x, z, y, n, l, m, real=real)
        x_label = 'x ($a_0$)'
        y_label = 'z ($a_0$)'
        x_min = +span
        x_max = -span
        slice_coords = '(x, 0, z)'
    else:
        raise ValueError

    y_min = -span
    y_max = +span

    rgba = complex_to_rgba(psi, mag_maps_to='v', zero_uniform_mag=True)

    if ax is None:
        fig, ax = plt.subplots(1, 1)
        fig.set_facecolor('black')

    ax.set_facecolor('black')
    ax.imshow(rgba, origin='lower',
              extent=[x_min, x_max, y_min, y_max])
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(fr'$\psi_{{{n},{l},{m}}}{slice_coords}$')

    return ax


def add_radial_fig(n, l, span=None, ax=None):
    if span is None:
        span = (1.5 * n)**2
    r = np.linspace(0, span, 100)
    radial_part = get_radial_part(n, l, r)
    radial_part /= max(radial_part)

    ax.plot(r, radial_part, color='r')


def intro_multi_view_3d_320_fig():
    (n, l, m) = (3, 2, 0)

    pl = pv.Plotter(shape=(1, 3), off_screen=True)

    # Contour plot
    pl.subplot(0, 0)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100,
        prob_threshold_list=(0.5,))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.camera.roll -= 20

    cam = pl.camera

    # Multi-contour plot
    pl.subplot(0, 1)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100, mag_maps_to='a',
        prob_threshold_list=(0.2, 0.5, 0.8))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.camera = cam

    # Volume plot
    pl.subplot(0, 2)
    mesh = get_wavefunction_volume_mesh(n, l, m,
                                        num_pts=100,
                                        max_opacity=0.7,
                                        opacity_exp=1.0)
    pl.set_background('black')
    pl.add_volume(mesh, scalars='rgba', mapper='gpu')
    pl.camera = cam

    pl.show(screenshot=Path(fig_dir, f'multi_view_3d_{n}{l}{m}.png'))


def radial_100_1d_fig():
    fig, ax = plt.subplots(1, 1)

    add_radial_fig(1, 0, span=3, ax=ax)

    ax.set_xlabel(f'r ($a_0$)')
    ax.set_ylabel(r'$\psi_{1, 0, 0}(r)$ (normalized)')
    ax.set_facecolor('black')
    fig.set_facecolor('black')
    fig.savefig(Path(fig_dir, '100_simple_1D.png'))

    plt.show()


def density_2d_100_2d_fig():
    n, l, m = (1, 0, 0)
    span = 2

    fig, (ax_z, ax_x) = plt.subplots(1, 2)

    add_2d_fig(n, l, m, span=span, slice_plane='z', ax=ax_z)
    add_2d_fig(n, l, m, span=span, slice_plane='x', ax=ax_x)

    ax_x.set_facecolor('black')
    ax_z.set_facecolor('black')
    fig.set_facecolor('black')

    fig.set_tight_layout(True)

    fig.savefig(Path(fig_dir, 'density_2d_100.png'))

    plt.show()


def simple_100_volume_3d_plot():
    (n, l, m) = (1, 0, 0)
    grid_span = 2
    grid_bounds = [-grid_span, grid_span, -grid_span, grid_span, -grid_span,
                   grid_span]

    pl = pv.Plotter(off_screen=True)

    mesh = get_wavefunction_volume_mesh(n, l, m,
                                        num_pts=100,
                                        max_opacity=1.0,
                                        opacity_exp=1.0)
    pl.set_background('black')
    pl.add_volume(mesh, scalars='rgba', mapper='gpu')
    pl.show_grid(color='white', bounds=grid_bounds)

    pl.show(screenshot=Path(fig_dir, f'simple_100_volume_3d.png'))


def simple_100_contour_3d_plots():
    (n, l, m) = (1, 0, 0)
    grid_span = 2
    grid_bounds = [-grid_span, grid_span, -grid_span, grid_span, -grid_span,
                   grid_span]
    cam_scale_factor = 1.5

    pl = pv.Plotter(shape=(1, 2), off_screen=True)

    # Contour plot
    pl.subplot(0, 0)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100,
        prob_threshold_list=(0.5,))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.show_grid(color='white', bounds=grid_bounds)
    pl.camera.position = (pl.camera.position[0]*cam_scale_factor,
                          pl.camera.position[1]*cam_scale_factor,
                          pl.camera.position[2]*cam_scale_factor)

    # Multi-contour plot
    pl.subplot(0, 1)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100, mag_maps_to='a',
        prob_threshold_list=(0.2, 0.4, 0.6))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.show_grid(color='white', bounds=grid_bounds)
    pl.camera.position = (pl.camera.position[0] * cam_scale_factor,
                          pl.camera.position[1] * cam_scale_factor,
                          pl.camera.position[2] * cam_scale_factor)

    pl.show(screenshot=Path(fig_dir, f'simple_100_contour_3d_plots.png'))


def radial_210_1d_fig():
    fig, ax = plt.subplots(1, 1)

    add_radial_fig(2, 1, span=None, ax=ax)

    ax.set_xlabel(f'r ($a_0$)')
    ax.set_ylabel(r'$\psi_{2, 1, 0}(r)$ (normalized)')
    ax.set_facecolor('black')
    fig.set_facecolor('black')
    fig.savefig(Path(fig_dir, 'radial_210_1d.png'))

    plt.show()


def density_2d_210_fig():
    n, l, m = (2, 1, 0)
    span = None

    fig, (ax_z, ax_x) = plt.subplots(1, 2)

    add_2d_fig(n, l, m, span=span, slice_plane='z', ax=ax_z)
    add_2d_fig(n, l, m, span=span, slice_plane='x', ax=ax_x)

    ax_x.set_facecolor('black')
    ax_z.set_facecolor('black')
    fig.set_facecolor('black')

    fig.set_tight_layout(True)

    fig.savefig(Path(fig_dir, 'density_2d_210.png'))

    plt.show()


def multi_view_3d_210_fig():
    (n, l, m) = (2, 1, 0)
    grid_span = 4
    grid_bounds = [-grid_span, grid_span, -grid_span, grid_span, -grid_span,
                   grid_span]
    cam_scale_factor = 1.5

    pl = pv.Plotter(shape=(1, 3), off_screen=True)

    # Contour plot
    pl.subplot(0, 1)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100,
        prob_threshold_list=(0.5,))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.camera.position = (pl.camera.position[0]*cam_scale_factor,
                          pl.camera.position[1]*cam_scale_factor,
                          pl.camera.position[2]*cam_scale_factor)
    cam = pl.camera
    pl.show_grid(color='white', bounds=grid_bounds)

    # Multi-contour plot
    pl.subplot(0, 2)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100, mag_maps_to='a',
        prob_threshold_list=(0.2, 0.4, 0.6))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.camera = cam
    pl.show_grid(color='white', bounds=grid_bounds)

    # Volume plot
    pl.subplot(0, 0)
    mesh = get_wavefunction_volume_mesh(n, l, m,
                                        num_pts=100,
                                        max_opacity=0.7,
                                        opacity_exp=1.0)
    pl.set_background('black')
    pl.add_volume(mesh, scalars='rgba', mapper='gpu')
    pl.camera = cam
    pl.show_grid(color='white', bounds=grid_bounds)

    pl.show(screenshot=Path(fig_dir, f'multi_view_3d_{n}{l}{m}.png'))


def main():
    fig_dir.mkdir(parents=True, exist_ok=True)

    # intro_multi_view_3d_320_fig()
    # radial_100_1d_fig()
    # simple_100_2d_fig()
    # simple_100_volume_3d_plot()
    # simple_100_contour_3d_plots()
    # radial_210_1d_fig()
    # density_2d_210_fig()
    multi_view_3d_210_fig()


if __name__ == "__main__":
    main()
