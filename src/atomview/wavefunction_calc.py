import numpy as np
from scipy.special import genlaguerre, factorial

from atomview.utils import sph_harm_cartesian


a0 = 1

def get_prefactor(n, l, atomic_number=1):  # noqa
    factor_1 = (2 * atomic_number / (n * a0)) ** (3 / 2)
    factor_2 = np.sqrt(
        factorial(n - l - 1, exact=False)
        / (2 * n * factorial(n + l, exact=False)))
    return factor_1 * factor_2


def get_radial_part(n, l, r, atomic_number=1):  # noqa
    rho = 2 * r * atomic_number / (n * a0)
    return np.exp(-rho / 2) * rho ** l * genlaguerre(n - l - 1, 2 * l + 1)(rho)


def get_atomic_wavefunction(x, y, z, n, l, m, atomic_number=1, real=False):
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
