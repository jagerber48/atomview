import numpy as np
from scipy.special import genlaguerre, lpmv
from scipy.special import sph_harm as sph_harm_scipy
from math import factorial
from matplotlib.colors import hsv_to_rgb

a0 = 1


def get_dx(span, n_steps):
    dx = 2 * span / (n_steps - 1)
    return dx


def get_xyz_arrays(span, n_steps, sinh_scale=False):
    if not sinh_scale:
        array = np.linspace(-span, span, n_steps)
        x, y, z = np.meshgrid(array, array, array, indexing='ij')
        dx = get_dx(span, n_steps)
        dv = np.full_like(x, dx**3)
        return x, y, z, dv
    else:
        array_lin = np.linspace(np.arcsinh(-span), np.arcsinh(span), n_steps)
        array = np.sinh(array_lin)

        x, y, z = np.meshgrid(array, array, array, indexing='ij')
        dx = np.gradient(x, axis=0)
        dy = np.gradient(y, axis=1)
        dz = np.gradient(z, axis=2)
        dv = dx * dy * dz
        return x, y, z, dv


def get_polar_arrays(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(np.divide(z, r, where=(r != 0), out=np.ones_like(r)))
    phi = np.arctan2(y, x)
    return r, theta, phi


def get_trig_angle_arrays(x, y, z):
    rho_squared = x**2 + y**2
    rho = np.sqrt(rho_squared)
    r = np.sqrt(rho_squared + z**2)

    cos_theta = np.divide(z, r, where=(r != 0), out=np.ones_like(r))
    cos_phi = np.divide(x, rho, where=(rho != 0), out=np.ones_like(r))
    sin_phi = np.divide(y, rho, where=(rho != 0), out=np.zeros_like(r))

    return r, cos_theta, cos_phi, sin_phi


def sph_harm_real(ylm, m):
    if m == 0:
        return ylm
    elif m > 0:
        return np.sqrt(2) * (-1) ** m * np.real(ylm)
    elif m < 0:
        # Convert ylm to yl|m| before taking imaginary part. Be careful with Condon-Shortley Phase
        ylm = (-1)**m * np.conj(ylm)
        return np.sqrt(2) * (-1) ** m * np.imag(ylm)


def sph_harm_polar(l, m, theta, phi, real_version=False):  # noqa
    ylm = sph_harm_scipy(m, l, phi, theta)
    if real_version:
        ylm = sph_harm_real(ylm, m)
    return ylm


def sph_harm_trig_angles(l, m, cos_theta, cos_phi, sin_phi, real_version=False):  # noqa
    normalization_factor = np.sqrt((2 * l + 1) / (4 * np.pi) * (factorial(l-m))/(factorial(l+m)))
    legendre_part = lpmv(m, l, cos_theta)
    exponential_part = (cos_phi + 1j * sin_phi) ** m
    ylm = normalization_factor * legendre_part * exponential_part

    if real_version:
        ylm = sph_harm_real(ylm, m)
    return ylm


def hydrogen_prefactor(n, l, atomic_number=1):  # noqa
    factor_1 = (2 * atomic_number / (n * a0)) ** (3 / 2)
    factor_2 = np.sqrt(factorial(n - l - 1) / (2 * n * factorial(n + l)))
    return factor_1 * factor_2


def hydrogen_radial_part(n, l, r, atomic_number=1):  # noqa
    rho = 2 * r * atomic_number / (n * a0)
    return np.exp(-rho / 2) * rho ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)


def hydrogen_angular_part_polar(l, m, theta, phi, real_version=False):  # noqa
    return sph_harm_polar(l, m, theta, phi, real_version=real_version)


def hydrogen_angular_part_trig_angles(l, m, cos_theta, cos_phi, sin_phi, real_version=False):  # noqa
    return sph_harm_trig_angles(l, m, cos_theta, cos_phi, sin_phi, real_version=real_version)


def hydrogen_wavefunction_polar(n, l, m, r, theta, phi, atomic_number=1, real_version=False):  # noqa
    norm = hydrogen_prefactor(n, l, atomic_number)
    radial_value = hydrogen_radial_part(n, l, r, atomic_number)
    angular_value = hydrogen_angular_part_polar(l, m, theta, phi, real_version)
    return norm * radial_value * angular_value


def hydrogen_wavefunction_trig_angles(n, l, m, r, cos_theta, cos_phi, sin_phi, atomic_number=1, real_version=False):  # noqa
    norm = hydrogen_prefactor(n, l, atomic_number)
    radial_value = hydrogen_radial_part(n, l, r, atomic_number)
    angular_value = hydrogen_angular_part_trig_angles(l, m, cos_theta, cos_phi, sin_phi, real_version)
    return norm * radial_value * angular_value


def array_prob_enclosed_to_psi_squared_value(psi_squared, dv, prob_enclosed_list):
    sort_index = np.argsort(psi_squared.ravel())[::-1]
    sorted_psi = psi_squared.ravel()[sort_index]
    try:
        sorted_dv = dv.ravel()[sort_index]
    except AttributeError:
        sorted_dv = dv
    sorted_prob = sorted_psi * sorted_dv
    integrated_prob = np.cumsum(sorted_prob)
    threshold_list = []
    for prob_enclosed in prob_enclosed_list:
        idx = np.argmax(integrated_prob > prob_enclosed)
        psi_squared_threshold = sorted_psi[idx]
        threshold_list.append(psi_squared_threshold)
    return threshold_list


def array_prob_enclosed_to_prob_value(prob_array, prob_enclosed_list):
    sorted_prob = np.sort(prob_array.ravel())[::-1]
    integrated_prob = np.cumsum(sorted_prob)
    threshold_list = []
    for prob_enclosed in prob_enclosed_list:
        idx = np.argmax(integrated_prob > prob_enclosed)
        prob_threshold = sorted_prob[idx]
        threshold_list.append(prob_threshold)
    return threshold_list


def complex_array_to_hsv(array, mag_maps_to='s'):
    if mag_maps_to is None:
        mag_maps_to = ''
    return_alpha = 'a' in mag_maps_to

    ang = np.angle(array)
    h = (ang / (2 * np.pi)) % 1

    if mag_maps_to != '':
        mag = np.abs(array)
        min_mag = mag.min()
        max_mag = mag.max()
        mag_range = max_mag - min_mag
        rescaled_mag = np.divide(mag - min_mag, mag_range, where=(mag_range != 0), out=np.ones_like(mag))
        if 's' in mag_maps_to:
            s = rescaled_mag
        else:
            s = np.ones_like(array, dtype=float)
        if 'v' in mag_maps_to:
            v = rescaled_mag
        else:
            v = np.ones_like(array, dtype=float)
        if 'a' in mag_maps_to:
            a = rescaled_mag
        else:
            a = np.ones_like(array, dtype=float)
    else:
        s = np.ones_like(array, dtype=float)
        v = np.ones_like(array, dtype=float)
        a = np.ones_like(array, dtype=float)

    if return_alpha:
        hsva = np.stack([h, s, v, a], axis=-1)
        return hsva
    else:
        hsv = np.stack([h, s, v], axis=-1)
        return hsv


def complex_array_to_rgb(array, mag_maps_to='s'):
    return_alpha = 'a' in mag_maps_to
    hsv_array = complex_array_to_hsv(array, mag_maps_to=mag_maps_to)
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
