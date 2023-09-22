import numpy as np
from scipy.special import genlaguerre, factorial
import pyvista as pv

from atomview.utils import sph_harm_cartesian, complex_to_rgba

a0 = 1

def get_prefactor(n, l, atomic_number=1):  # noqa
    factor_1 = (2 * atomic_number / (n * a0)) ** (3 / 2)
    factor_2 = np.sqrt(
        factorial(n - l - 1, exact=False)
        / (2 * n * factorial(n + l, exact=False)))
    return factor_1 * factor_2


def get_radial_part(n, l, r, atomic_number=1):
    rho = 2 * r * atomic_number / (n * a0)
    return np.exp(-rho / 2) * rho ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)


def get_atomic_wavefunction(x, y, z,
                            n, l, m,
                            atomic_number=1,
                            real=False):
    prefactor = get_prefactor(n, l, atomic_number)

    r = np.sqrt(x**2 + y**2 + z**2)

    if real:
        calc_m = abs(m)
    else:
        calc_m = m

    angular_factor = sph_harm_cartesian(x, y, z, l, calc_m, r=r)
    radial_factor = get_radial_part(n, l, r, atomic_number)

    psi = prefactor * radial_factor * angular_factor

    if real:
        if m > 0:
            psi = np.sqrt(2) * (-1)**m * np.real(psi)
        elif m < 0:
            psi = np.sqrt(2) * (-1)**m * np.imag(psi)

    return psi


def get_psi_squared_threshold_val(psi_squared, dv, prob_enclosed_list):

    sort_index = np.argsort(psi_squared.ravel())

    sorted_psi_squared = psi_squared.ravel()[sort_index]
    sorted_dv = dv.ravel()[sort_index]
    sorted_prob = sorted_dv * sorted_psi_squared
    integrated_prob = np.cumsum(sorted_prob)
    psi_squared_thresh_list = []
    for prob_enclosed in prob_enclosed_list:
        idx = np.searchsorted(integrated_prob, prob_enclosed)
        psi_squared_threshold = sorted_psi_squared[idx]
        psi_squared_thresh_list.append(psi_squared_threshold)
    return psi_squared_thresh_list


def get_wavefunction_prob_contour_mesh(n, l, m, real=False,
                                       num_pts=50,
                                       prob_threshold_list=(0.6,),
                                       mag_maps_to='',
                                       clip=False,
                                       clip_ghost=False,
                                       ghost_opacity=0.2):
    span = (1.5 * n) ** 2

    r_1d = np.sinh(np.linspace(0, np.arcsinh(span), num_pts))
    theta_1d = np.linspace(0, np.pi, num_pts, endpoint=True)
    phi_1d = np.linspace(0, 2 * np.pi, num_pts, endpoint=True)

    r, theta, phi = np.meshgrid(r_1d, theta_1d, phi_1d, indexing='ij')

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    dv = (r**2 * np.sin(theta)
          * np.gradient(r, axis=0)
          * np.gradient(theta, axis=1)
          * np.gradient(phi, axis=2))

    psi = get_atomic_wavefunction(x, y, z, n, l, m, real=real)
    psi_squared = np.abs(psi) ** 2

    psi_squared_thresh_list = get_psi_squared_threshold_val(
        psi_squared, dv, prob_threshold_list)

    rgba = complex_to_rgba(
        psi,
        mag_maps_to=mag_maps_to
    )

    mesh = pv.StructuredGrid(x, y, z)
    mesh['psi_squared'] = psi_squared.ravel(order='F')
    mesh['rgba'] = rgba.reshape(psi.size, 4, order='F')

    if clip:
        clip_mask = ((phi > 0)
                     & (phi < np.pi/2)
                     & (theta < np.pi/2)).ravel(order='F')

        if clip_ghost:
            ghost_clip_mask = ((phi > 0)
                               & (phi > np.pi / 2)
                               & (theta > np.pi / 2)).ravel(order='F')

            ghost_mesh = mesh.copy()
            ghost_mesh['psi_squared'][ghost_clip_mask] = 0
            ghost_mesh['rgba'][:, 3] = ghost_opacity
            ghost_contour_mesh = ghost_mesh.contour(psi_squared_thresh_list,
                                                    scalars='psi_squared')

        mesh['psi_squared'][clip_mask] = 0

    contour_mesh = mesh.contour(psi_squared_thresh_list,
                                scalars='psi_squared')

    if clip and clip_ghost:
        return contour_mesh, ghost_contour_mesh
    else:
        return contour_mesh


def get_wavefunction_volume_mesh(n, l, m, real=False,
                                 num_pts=50,
                                 max_opacity=0.2,
                                 clip=False):
    span = (1.5 * n) ** 2

    single_ax_array = np.sinh(
        np.linspace(
            np.arcsinh(-span),
            np.arcsinh(span),
            num_pts
        )
    )

    single_ax_array = np.linspace(
            -span,
            span,
            num_pts
        )

    x, y, z = np.meshgrid(single_ax_array,
                          single_ax_array,
                          single_ax_array,
                          indexing='ij')

    psi = get_atomic_wavefunction(x, y, z, n, l, m, real=real)
    if clip:
        clip_mask = ((x > 0)
                     & (y > 0)
                     & (z > 0))
        psi[clip_mask] = 0

    rgba = complex_to_rgba(
        np.abs(psi) * psi,
        mag_maps_to='a'
    )

    rgba[:, :, :, 3] *= max_opacity
    rgba_uint8 = (255 * rgba).astype(np.uint8)

    mesh = pv.RectilinearGrid(single_ax_array,
                              single_ax_array,
                              single_ax_array)

    mesh['rgba'] = rgba_uint8.reshape((psi.size, 4), order='F')

    return mesh


def main():
    (n, l, m) = (2, 1, 1)
    real = True

    contour_mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, real=real, num_pts=150,
        prob_threshold_list=(0.5,),
        mag_maps_to='',
        clip=False)
    volume_mesh = get_wavefunction_volume_mesh(
        n, l, m, real=real, num_pts=100, max_opacity=0.4, clip=False
    )

    pl = pv.Plotter()
    pl.set_background('black')
    # pl.add_mesh(
    #     contour_mesh,
    #     scalars='rgba',
    #     rgb=True,
    #     specular=1,
    #     diffuse=1,
    #     ambient=0.3)
    pl.add_volume(
        volume_mesh,
        scalars='rgba',
        mapper='gpu'
    )
    pl.show()


if __name__ == "__main__":
    main()
