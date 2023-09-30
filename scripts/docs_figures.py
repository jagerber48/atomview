from pathlib import Path

import pyvista as pv

from atomview.atom_wavefunction import (
    get_wavefunction_prob_contour_mesh, get_wavefunction_volume_mesh)


def main():
    (n, l, m) = (3, 2, 0)
    real = True

    pl = pv.Plotter(shape=(1, 3), off_screen=True)

    pl.subplot(0, 0)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100, real=real,
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

    pl.subplot(0, 1)
    mesh = get_wavefunction_prob_contour_mesh(
        n, l, m, num_pts=100, mag_maps_to='a', real=real,
        prob_threshold_list=(0.2, 0.5, 0.8))
    pl.set_background('black')
    pl.add_mesh(mesh, scalars='rgba', rgb=True,
                smooth_shading=True,
                specular=0,
                diffuse=1,
                ambient=0.3
                )
    pl.camera = cam

    pl.subplot(0, 2)
    mesh = get_wavefunction_volume_mesh(n, l, m, real=real,
                                        num_pts=100,
                                        max_opacity=0.7,
                                        opacity_exp=1.0)
    pl.set_background('black')
    pl.add_volume(mesh, scalars='rgba', mapper='gpu')
    pl.camera = cam

    fig_dir = Path(Path.cwd(), 'figures', 'docs_figs')
    fig_dir.mkdir(parents=True, exist_ok=True)

    pl.show(screenshot=Path(fig_dir, f'{n}{l}{m}_multi_view'))


if __name__ == "__main__":
    main()
