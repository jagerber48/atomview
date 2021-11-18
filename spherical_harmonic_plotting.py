import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv
from hydrogen_calculations import sph_harm_polar, complex_array_to_rgb

pv.set_plot_theme("document")


def get_sph_harm_mesh(l, m, n_steps=101, real_version=False, radius_from_mag=True):  # noqa
    theta, phi = np.mgrid[0:np.pi:1j * n_steps, 0:2 * np.pi:1j * n_steps]
    sph_harm_data = sph_harm_polar(l, m, theta, phi, real_version=real_version)

    if radius_from_mag:
        mag = np.abs(sph_harm_data)
        r = mag / mag.max()
        mag_maps_to = ''
    else:
        r = 1
        mag_maps_to = 's'

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    color_map = complex_array_to_rgb(sph_harm_data, mag_maps_to=mag_maps_to)

    mesh_grid = pv.StructuredGrid(x, y, z)
    mesh_grid['color_map'] = color_map.reshape([sph_harm_data.size, 3], order='F')

    return mesh_grid


def plot_sph_harm_mesh_3d(sph_harm_mesh, show=True, plotter=None, notebook=False, show_grid=False, **kwargs):

    if plotter is None:
        plotter = pv.Plotter(notebook=notebook)

    plotter.add_mesh(sph_harm_mesh, scalars='color_map', rgb=True,
                     specular=0, diffuse=1, ambient=0.3, smooth_shading=True,
                     **kwargs)

    if show_grid:
        plotter.show_grid()
    if show:
        plotter.show(auto_close=True, interactive=True, jupyter_backend='static')
    return plotter


def plot_sph_harm_mesh_2d(sph_harm_mesh, show=True, ax=None, **kwargs):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    nx = sph_harm_mesh.dimensions[0]
    ny = sph_harm_mesh.dimensions[1]
    color_map = sph_harm_mesh['color_map'].reshape([nx, ny, 3], order='F')

    ax.imshow(color_map, extent=[0, 2, 1, 0], aspect=2, **kwargs)
    ax.grid(False)
    ax.set_xlabel('$\\phi$')
    ax.set_ylabel('$\\theta$')
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(labels=['0', '$\\pi$', '$2\\pi$'])
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(labels=['0', '$\\pi/2$', '$\\pi$'])
    if show:
        plt.show()
