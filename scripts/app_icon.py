from pathlib import Path

import pyvista as pv

from atomview.atom_wavefunction import get_wavefunction_prob_contour_mesh


def main():
    (n, l, m) = (4, 3, -1)
    mesh = get_wavefunction_prob_contour_mesh(n, l, m, num_pts=100)

    pl = pv.Plotter(off_screen=True)
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=1,
                diffuse=1,
                ambient=0.3
                )
    pl.camera.roll -= 20
    pl.show(screenshot=Path(Path.cwd(), 'figures', 'gen_figs',
                            '311_icon'))


if __name__ == "__main__":
    main()
