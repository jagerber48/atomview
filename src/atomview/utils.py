import numpy as np
from matplotlib.colors import hsv_to_rgb
from scipy.special import sph_harm as sph_harm_scipy
from scipy.special import factorial, lpmv


def sph_harm_cartesian(x, y, z, l, m, use_scipy=False,  # noqa
                       r=None):
    rho_squared = x ** 2 + y ** 2
    if r is None:
        r = np.sqrt(rho_squared + z ** 2)
    cos_theta = np.divide(z, r,
                          where=(r != 0),
                          out=np.ones_like(z))

    if use_scipy:
        phi = np.arctan2(y, x)
        theta = np.arccos(cos_theta)
        sph_harm = sph_harm_scipy(m, l, phi, theta)
    else:
        rho = np.sqrt(rho_squared)
        cos_phi = np.divide(x, rho,
                            where=(rho != 0),
                            out=np.ones_like(r)
                            )
        sin_phi = np.divide(y, rho,
                            where=(rho != 0),
                            out=np.zeros_like(r)
                            )

        normalization_factor = np.sqrt(
            (((2 * l + 1) / (4 * np.pi))
             * (factorial(l - m, exact=False) / factorial(l + m, exact=False)))
        )
        legendre_part = lpmv(m, l, cos_theta)
        exponential_part = (cos_phi + 1j * sin_phi) ** m
        sph_harm = normalization_factor * legendre_part * exponential_part

    return sph_harm


def complex_to_rgba(arr, mag_maps_to='', zero_uniform_mag=False):
    h = (np.angle(arr) / (2 * np.pi)) % 1
    s = np.ones_like(arr, dtype=float)
    v = np.ones_like(arr, dtype=float)
    a = np.ones_like(arr, dtype=float)

    if mag_maps_to != '':
        mag = np.abs(arr)
        if not zero_uniform_mag:
            out = np.ones_like(mag)
        else:
            out = np.zeros_like(mag)
        scaled_mag = np.divide(
            mag - np.min(mag),
            np.max(mag) - np.min(mag),
            where=(np.max(mag) - np.min(mag) != 0),
            out=out)
        if 's' in mag_maps_to:
            s *= scaled_mag
        if 'v' in mag_maps_to:
            v *= scaled_mag
        if 'a' in mag_maps_to:
            a *= scaled_mag

    hsv = np.stack([h, s, v], axis=-1)
    rgb = hsv_to_rgb(hsv)

    rgba = np.concatenate((rgb, np.expand_dims(a, -1)), axis=-1)

    return rgba
