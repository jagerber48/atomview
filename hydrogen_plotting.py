import numpy as np
import pyvista as pv
from hydrogen_calculations import (get_xyz_arrays, get_dx, get_trig_angle_arrays, hydrogen_wavefunction_trig_angles,
                                   complex_array_to_rgb, array_prob_enclosed_to_psi_squared_value)

pv.set_plot_theme("document")


def get_clip_mask(grid_mesh, clip_axes='xyz'):
    if 'x' in clip_axes:
        x_mask = grid_mesh.points[:, 0] >= 0
    else:
        x_mask = np.full_like(grid_mesh.points[:, 0], True, dtype='bool')
    if 'y' in clip_axes:
        y_mask = grid_mesh.points[:, 1] >= 0
    else:
        y_mask = np.full_like(grid_mesh.points[:, 1], True, dtype='bool')
    if 'z' in clip_axes:
        z_mask = grid_mesh.points[:, 2] >= 0
    else:
        z_mask = np.full_like(grid_mesh.points[:, 2], True, dtype='bool')
    mask = x_mask & y_mask & z_mask
    return mask


def generate_orbital_contour_plot(n, l, m, prob_threshold_list=(0.6,),  # noqa
                                  n_steps=101, span=None, sinh_scale=True,
                                  real_version=False, mag_maps_to='',
                                  clip=False, clip_axes='xyz', clip_ghost=False,
                                  show_grid=False, grid_bounds=None,
                                  title=None, camera_position=None,
                                  show=True, plot_in_notebook=False,
                                  save_plot=False, save_path=None):
    if span is None:
        span = (1.5 * n) ** 2

    x, y, z, dv = get_xyz_arrays(span=span, n_steps=n_steps, sinh_scale=sinh_scale)
    r, cos_theta, cos_phi, sin_phi = get_trig_angle_arrays(x, y, z)
    psi = hydrogen_wavefunction_trig_angles(n, l, m,
                                            r, cos_theta, cos_phi, sin_phi,
                                            real_version=real_version)

    psi_squared = np.abs(psi) ** 2
    psi_squared_threshold_list = array_prob_enclosed_to_psi_squared_value(psi_squared, dv, prob_threshold_list)

    color_map = complex_array_to_rgb(psi, mag_maps_to=mag_maps_to)

    grid_mesh = pv.RectilinearGrid(x, y, z)
    grid_mesh['prob'] = psi_squared.ravel(order='F')
    grid_mesh['color_map'] = color_map.reshape([psi.size, color_map.shape[3]], order='F')

    if save_plot:
        plot_in_notebook = True

    plotter = pv.Plotter(notebook=plot_in_notebook, off_screen=save_plot)

    if clip:
        clip_mask = get_clip_mask(grid_mesh, clip_axes)
        grid_mesh['prob'][clip_mask] = 0

        if clip_ghost:
            grid_mesh_ghost = pv.RectilinearGrid(x, y, z)
            grid_mesh_ghost['prob'] = psi_squared.ravel(order='F')
            grid_mesh_ghost['prob'][np.logical_not(clip_mask)] = 0
            grid_mesh_ghost['color_map'] = color_map.reshape([psi.size, color_map.shape[3]], order='F')
            contour_mesh_ghost = grid_mesh_ghost.contour(psi_squared_threshold_list, 'prob')
            plotter.add_mesh(contour_mesh_ghost, scalars='color_map', rgb=True,
                             specular=1, diffuse=1, ambient=0.3, smooth_shading=True,
                             opacity=0.4)

    contour_mesh = grid_mesh.contour(psi_squared_threshold_list, 'prob')

    plotter.add_mesh(contour_mesh, scalars='color_map', rgb=True,
                     specular=1, diffuse=1, ambient=0.3, smooth_shading=True)

    if camera_position is not None:
        plotter.camera_position = [camera_position, (0, 0, 0), (0, 0, 1)]
        plotter.camera_set = True
    if title is not None:
        plotter.add_text(title, font_size=32)
    if show_grid:
        plotter.show_grid(bounds=grid_bounds)

    if save_plot:
        plotter.render()
        plotter.screenshot(filename=save_path)
        plotter.close()
        return plotter

    if show:
        plotter.show()
    else:
        return plotter


def generate_orbital_volume_plot(n, l, m,  # noqa
                                 n_steps=101, span=None, sinh_scale=False,
                                 opacity_exponent=1, max_opacity=0.1,
                                 real_version=False,
                                 show_grid=False, grid_bounds=None,
                                 title=None, camera_position=None,
                                 show=True, plot_in_notebook=False,
                                 save_plot=False, save_path=None):
    if span is None:
        span = (1.5 * n) ** 2

    dx = get_dx(span, n_steps)
    x, y, z, dv = get_xyz_arrays(span=span, n_steps=n_steps, sinh_scale=sinh_scale)
    r, cos_theta, cos_phi, sin_phi = get_trig_angle_arrays(x, y, z)

    psi = hydrogen_wavefunction_trig_angles(n, l, m,
                                            r, cos_theta, cos_phi, sin_phi,
                                            real_version=real_version)

    color_map = complex_array_to_rgb(psi, mag_maps_to='a')
    color_map[:, :, :, 3] = max_opacity * (color_map[:, :, :, 3] ** 2) ** opacity_exponent

    xyz = np.transpose(np.stack([x.ravel(order='F'), y.ravel(order='F'), z.ravel(order='F')], axis=0))
    poly_grid = pv.PolyData(xyz)
    poly_grid['color_map'] = color_map.reshape([psi.size, 4], order='F')
    geom = pv.Cube()
    glyphs_grid = poly_grid.glyph(orient=False, geom=geom, scale=False, factor=dx)

    if save_plot:
        plot_in_notebook = True

    plotter = pv.Plotter(notebook=plot_in_notebook, off_screen=save_plot)

    plotter.add_mesh(glyphs_grid, scalars='color_map', rgb=True, show_edges=False,
                     ambient=0.3)

    if camera_position is not None:
        plotter.camera_position = [camera_position, (0, 0, 0), (0, 0, 1)]
        plotter.camera_set = True
    if title is not None:
        plotter.add_text(title, font_size=32)
    if show_grid:
        plotter.show_grid(bounds=grid_bounds)

    if save_plot:
        plotter.render()
        plotter.screenshot(filename=save_path)
        plotter.close()
        return plotter

    if show:
        plotter.show()
    else:
        return plotter
