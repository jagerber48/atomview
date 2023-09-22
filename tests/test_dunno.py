import numpy as np
import pyvista as pv

from src.atomview.plot_atom_wavefunction import get_xyz_arrays, complex_array_to_rgb
from src.atomview.atom_wavefunction import get_atomic_wavefunction


(n, l, m) = (3, 1, 0)
span = (1.5 * n) ** 2

n_steps = 101
opacity_exponent = 2
max_opacity = 0.5
real = False
sinh_scale = False
clip = False

x, y, z = get_xyz_arrays(span=span, n_steps=n_steps, sinh_scale=sinh_scale)

xyz = np.transpose(
    np.stack(
        [x.ravel(order='F'), y.ravel(order='F'), z.ravel(order='F')],
        axis=0
    )
)

dl = np.maximum.reduce(
    [np.gradient(x, axis=0),
     np.gradient(y, axis=1),
     np.gradient(z, axis=2)])

psi = get_atomic_wavefunction(x, y, z, n, l, m, real=real)
color_map = complex_array_to_rgb(psi, mag_maps_to='a')
color_map[:, :, :, 3] = (
        max_opacity
        * (color_map[:, :, :, 3] ** 2) ** opacity_exponent
)

rect_grid = pv.RectilinearGrid(x[:, 0, 0], y[0, :, 0], z[0, 0, :])
# rect_grid = pv.RectilinearGrid(x, y, z)
rect_grid['color_map'] = ((color_map.reshape([psi.size, 4], order='F'))*255).astype(np.uint8)

plotter = pv.Plotter()
plotter.set_background('black')
plotter.add_volume(rect_grid, scalars='color_map', mapper='gpu')
plotter.show()
