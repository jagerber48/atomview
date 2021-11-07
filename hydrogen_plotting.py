import numpy as np
from scipy.special import genlaguerre
from scipy.special import sph_harm as sph_harm_scipy
from math import factorial
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import pyvista as pv

a0 = 1
pv.set_plot_theme("document")


def hydrogen_prefactor(n, l, atomic_number=1):  # noqa
    factor_1 = (2 * atomic_number / (n * a0)) ** (3 / 2)
    factor_2 = np.sqrt(factorial(n - l - 1) / (2 * n * factorial(n + l)))
    return factor_1 * factor_2


def hydrogen_radial_part(n, l, r, atomic_number=1):  # noqa
    rho = 2 * r * atomic_number / (n * a0)
    return np.exp(-rho / 2) * rho ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)


def sph_harm(l, m, theta, phi, real_version=False):  # noqa
    if not real_version:
        return sph_harm_scipy(m, l, phi, theta)
    else:
        if m < 0:
            prefactor = 1j / np.sqrt(2)
            term = sph_harm_scipy(m, l, phi, theta) - (-1) ** m * sph_harm_scipy(-m, l, phi, theta)
            return prefactor * term
        elif m > 0:
            prefactor = 1 / np.sqrt(2)
            term = sph_harm_scipy(-m, l, phi, theta) + (-1) ** m * sph_harm_scipy(m, l, phi, theta)
            return prefactor * term
        else:
            return sph_harm_scipy(m, l, phi, theta)


def hydrogen_angular_part(l, m, theta, phi, real_version=False):  # noqa
    return sph_harm(l, m, theta, phi, real_version=real_version)


def hydrogen_wavefunction(n, l, m, r, theta, phi, atomic_number=1, real_version=False):  # noqa
    norm = hydrogen_prefactor(n, l, atomic_number)
    radial_value = hydrogen_radial_part(n, l, r, atomic_number)
    angular_value = hydrogen_angular_part(l, m, theta, phi, real_version)
    return norm * radial_value * angular_value


def complex_array_to_hsv(array, mag_maps_to='s', return_alpha=False):
    if mag_maps_to is None:
        mag_maps_to = ''
    if 'a' in mag_maps_to and not return_alpha:
        print(f'return_alpha set to False but \'a\' is in mag_maps_to=\'{mag_maps_to}\'. Setting return_alpha=True')
        return_alpha = True

    ang = np.angle(array)

    h = (ang / (2 * np.pi)) % 1
    s = np.ones_like(array, dtype=float)
    v = np.ones_like(array, dtype=float)
    a = np.ones_like(array, dtype=float)

    if mag_maps_to != '':
        mag = np.abs(array)
        min_mag = mag.min()
        max_mag = mag.max()
        mag_range = max_mag - min_mag
        rescaled_mag = np.divide(mag - min_mag, mag_range, where=(mag_range != 0), out=np.ones_like(mag))
        if 's' in mag_maps_to:
            s = rescaled_mag
        if 'v' in mag_maps_to:
            v = rescaled_mag
        if 'a' in mag_maps_to:
            a = rescaled_mag

    if return_alpha:
        hsva = np.stack([h, s, v, a], axis=-1)
        return hsva
    else:
        hsv = np.stack([h, s, v], axis=-1)
        return hsv


def complex_array_to_rgb(array, mag_maps_to='s', return_alpha=False):
    hsv_array = complex_array_to_hsv(array, mag_maps_to=mag_maps_to, return_alpha=return_alpha)
    if not return_alpha:
        rgb = hsv_to_rgb(hsv_array)
        return rgb
    else:
        hsv = hsv_array[..., 0:3]
        a = hsv_array[..., 3]
        rgb = hsv_to_rgb(hsv)
        a_expanded = np.expand_dims(a, axis=-1)
        rgba = np.concatenate([rgb, a_expanded], axis=-1)
        return rgba


def array_prob_enclosed_to_prob_value(prob_array, prob_enclosed_list):
    sorted_prob = np.sort(prob_array.ravel())[::-1]
    integrated_prob = np.cumsum(sorted_prob)
    threshold_list = []
    for prob_enclosed in prob_enclosed_list:
        idx = np.argmax(integrated_prob > prob_enclosed)
        prob_threshold = sorted_prob[idx]
        threshold_list.append(prob_threshold)
    return threshold_list


def get_wavefunction_contour_mesh(n, l, m, atomic_number=1, prob_enclosed_list=(0.6,), n_steps=100, span=None,  # noqa
                                  real_version=False, clip=False, clip_axes='xyz', map_opacity=False):
    if span is None:
        span = (2 * n) ** 2
    grid_slice = slice(-span, +span, n_steps * 1j)
    _, dx = np.linspace(-span, +span, n_steps, retstep=True)
    dv = dx ** 3

    x, y, z = np.mgrid[(grid_slice,) * 3]
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arccos(np.divide(z, r, where=(r != 0), out=np.ones_like(r)))
    phi = np.arctan2(y, x)

    wavefunction = hydrogen_wavefunction(n, l, m, r, theta, phi, atomic_number=atomic_number,
                                         real_version=real_version)

    if map_opacity:
        mag_maps_to = 'a'
    else:
        mag_maps_to = None
    color_map = complex_array_to_rgb(wavefunction, mag_maps_to=mag_maps_to, return_alpha=map_opacity)

    prob_array = dv * np.abs(wavefunction) ** 2
    prob_threshold_list = array_prob_enclosed_to_prob_value(prob_array, prob_enclosed_list)

    grid = pv.StructuredGrid(x, y, z)

    grid['prob'] = prob_array.ravel(order='F')
    if map_opacity:
        grid['color_map'] = color_map.reshape([wavefunction.size, 4], order='F')
    else:
        grid['color_map'] = color_map.reshape([wavefunction.size, 3], order='F')

    if clip:
        if 'x' in clip_axes:
            x_mask = grid.points[:, 0] >= 0
        else:
            x_mask = np.full_like(grid.points[:, 0], True, dtype='bool')
        if 'y' in clip_axes:
            y_mask = grid.points[:, 1] >= 0
        else:
            y_mask = np.full_like(grid.points[:, 1], True, dtype='bool')
        if 'z' in clip_axes:
            z_mask = grid.points[:, 2] >= 0
        else:
            z_mask = np.full_like(grid.points[:, 2], True, dtype='bool')
        mask = x_mask & y_mask & z_mask
        grid['prob'][mask] = 0

    contour_mesh = grid.contour(prob_threshold_list, 'prob')

    return contour_mesh


def plot_contour_mesh(contour_mesh, show_grid=True, show=True, plotter=None, notebook=False, **kwargs):
    if plotter is None:
        plotter = pv.Plotter(notebook=notebook)

    span = contour_mesh.bounds[1]
    for position in [(2 * span, 0, 0), (0, 2 * span, 0), (0, 0, 2 * span),
                     (-2 * span, 0, 0), (0, -2 * span, 0), (0, 0, -2 * span)]:
        light = pv.Light(position=position, intensity=0.2, positional=False)
        plotter.add_light(light, only_active=True)

    plotter.add_mesh(contour_mesh, scalars='color_map', rgb=True, **kwargs)

    if show_grid:
        plotter.show_grid()
    if show:
        plotter.show(auto_close=True, interactive=True)
    return plotter


def get_wavefunction_volume_mesh(n, l, m, atomic_number=1, n_steps=100, span=None, real_version=False):  # noqa
    if span is None:
        span = (2 * n) ** 2
    grid_slice = slice(-span, +span, n_steps * 1j)
    _, dx = np.linspace(-span, +span, n_steps, retstep=True)

    x, y, z = np.mgrid[(grid_slice,) * 3]
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arccos(np.divide(z, r, where=(r != 0), out=np.ones_like(r)))
    phi = np.arctan2(y, x)

    wavefunction = hydrogen_wavefunction(n, l, m, r, theta, phi, atomic_number=atomic_number,
                                         real_version=real_version)

    color_map = complex_array_to_rgb(wavefunction, mag_maps_to='a', return_alpha=True)

    xyz = np.transpose(np.stack([x.ravel(order='F'), y.ravel(order='F'), z.ravel(order='F')], axis=0))
    poly_grid = pv.PolyData(xyz)
    poly_grid['color_map'] = color_map.reshape([wavefunction.size, 4], order='F')

    geom = pv.Cube()
    glyphs_grid = poly_grid.glyph(orient=False, geom=geom, scale=False, factor=dx)

    return glyphs_grid


def plot_glyphs_grid(glyphs_grid, show_grid=True, show=True, plotter=None, notebook=False, **kwargs):

    if plotter is None:
        plotter = pv.Plotter(notebook=notebook)

    span = glyphs_grid.bounds[1]
    for position in [(2 * span, 0, 0), (0, 2 * span, 0), (0, 0, 2 * span),
                     (-2 * span, 0, 0), (0, -2 * span, 0), (0, 0, -2 * span)]:
        light = pv.Light(position=position, intensity=0.2, positional=False)
        plotter.add_light(light, only_active=True)

    plotter.add_mesh(glyphs_grid, scalars='color_map', rgb=True, show_edges=False, **kwargs)

    if show_grid:
        plotter.show_grid()
    if show:
        plotter.show(auto_close=True, interactive=True)
    return plotter


def get_sph_harm_mesh(l, m, n_steps=101, real_version=False, radius_from_mag=True):  # noqa
    theta, phi = np.mgrid[0:np.pi:1j * n_steps, 0:2 * np.pi:1j * n_steps]
    sph_harm_data = sph_harm(l, m, theta, phi, real_version=real_version)

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

    color_map = complex_array_to_rgb(sph_harm_data, mag_maps_to=mag_maps_to,
                                     return_alpha=False)

    mesh_grid = pv.StructuredGrid(x, y, z)
    mesh_grid['color_map'] = color_map.reshape([sph_harm_data.size, 3], order='F')

    return mesh_grid


def plot_sph_harm_mesh(sph_harm_mesh, show=True, plotter=None, notebook=False, show_grid=False, **kwargs):

    if plotter is None:
        plotter = pv.Plotter(notebook=notebook)

    for position in [(2, 0, 0), (0, 2, 0), (0, 0, 2),
                     (-2, 0, 0), (0, -2, 0), (0, 0, -2)]:
        light = pv.Light(position=position, intensity=0.2, positional=False)
        plotter.add_light(light, only_active=True)

    plotter.add_mesh(sph_harm_mesh, scalars='color_map', rgb=True, **kwargs)

    if show_grid:
        plotter.show_grid()
    if show:
        plotter.show(auto_close=True, interactive=True)
    return plotter


def plot_sph_harm_mesh_2d(sph_harm_mesh, show=True, ax=None, **kwargs):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
    nx = sph_harm_mesh.dimensions[0]
    ny = sph_harm_mesh.dimensions[1]
    color_map = sph_harm_mesh['color_map'].reshape([nx, ny, 3], order='F')

    ax.imshow(color_map, extent=[0, 2, 0, 1], aspect=2, **kwargs)
    ax.grid(False)
    ax.set_xlabel('$\\phi$')
    ax.set_ylabel('$\\theta$')
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(labels=['0', '$\\pi$', '$2\\pi$'])
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(labels=['0', '$\\pi/2$', '$\\pi$'])
    if show:
        plt.show()

