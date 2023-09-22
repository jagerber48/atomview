from hydrogen_plotting import generate_orbital_contour_plot
from scripts.spherical_harmonic_plotting import get_sph_harm_mesh

(n, l, m) = (5, 3, 1)
real_version = False


radius_from_mag = True

sph_harm_mesh = get_sph_harm_mesh(l, m, n_steps=101,
                                  real_version=real_version)

# p = plot_sph_harm_mesh_3d(sph_harm_mesh, show=True)

prob_threshold_list = (0.6,)

_ = generate_orbital_contour_plot(n, l, m, n_steps=101, prob_threshold_list=prob_threshold_list,
                                  clip=True, clip_ghost=False, clip_axes='xyz', show_grid=True,
                                  sinh_scale=True, mag_maps_to='', real_version=real_version,
                                  show=True,
                                  grid_bounds=None,
                                  camera_position=None,
                                  plot_in_notebook=False)
