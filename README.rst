########
atomview
########

|  **Repository:** `<https://github.com/jagerber48/atomview>`_

========
Overview
========

``atomview`` is an application used to visualize atomic orbitals.
``atomview`` supports visualization of a large number of complex and
real atomic orbitals and includes probability contour, multi-probability
contour, and volume density visualizations of the 3D atomic orbitals.

.. figure:: scripts/figures/docs_figs/multi_view_3d_320.png
    :align: center
    :width: 400

    ``atomview`` visualizations of the :math:`(n, l, m) = (3, 2, 0)`
    orbital.
    Left: solid contour visualization enclosing 50% probability.
    Center: Transparent multi-contour visualization enclosing 20%, 50%,
    and 80% probability.
    Right: Transparent cloud volume visualization.

============
Installation
============

Currently ``atomview`` only runs on Windows.
The executable can be
:download:`downloaded here <../../dist/AtomView.exe>`.

===============
Atomic Orbitals
===============

What are atomic orbitals?
Consider a single Hydrogen atom.
This atom consist of a small positively charged nucleus consisting of a
single proton along with a small negatively charged electron which
"orbits" the proton.
Because these particles are so small their dynamics are described by
quantum mechanics, and in particular, by the Schrödinger equation.
For a Hydrogen atom, the (time-independent) Schrödinger equation is
given by

.. TODO::

   Citation

.. math::

    E \psi = -\frac{\hbar^2}{2m} \nabla^2 \psi - \frac{e^2}{4\pi \epsilon_0 r} \psi.

Solutions :math:`\psi` to the Schrödinger differential equation are
called wavefunctions.
In the same way the state of a classical billiards ball is specified by
its position and velocity, the state of a quantum electron is described
by the wavefunction.
In the expression above :math:`E` is the energy of the system when the
electron's state is specified by the corresponding :math:`\psi`.
:math:`\hbar` is Planck's reduced constant, :math:`m` is the mass of the
electron, :math:`e` is the charge of the electron, and
:math:`\epsilon_0` is the permittivity of free space.

In the case of the Hydrogen atom, the wavefunctions are called atomic
orbitals.
In general, these wavefunctions are complex-valued functions of 3D
space :math:`\psi(x, y, z) = \psi(r, \theta, \phi)`.
Mathematically, the wavefunctions are just specific solutions to the
Schrödinger differential equation.
Physically, the squared amplitude of the wavefunction for a particle at
some point in space, :math:`|\psi(x, y, z)|^2`, is interpreted as the
probability of finding the particle at that location in space.

There are an infinite number of solutions to Schrödinger's equation for
the Hydrogen atom.
These solutions are enumerated by three integer indices, :math:`n`,
:math:`l`, and :math:`m`.
:math:`n`, :math:`l`, and :math:`m` are called the Hydrogen quantum
numbers.
:math:`n` is any (non-zero) positive integer, :math:`l` is any
non-negative integer satisfying :math:`0 \le l < n` and :math:`m` is any
integer satisfying :math:`-l \le m \le l`.
The corresponding solutions are given by

.. math::

    E_{n, l, m} =&  - \frac{me^4}{2(4\pi \epsilon_0)^2 \hbar^2} \frac{1}{n^2}\\
    \psi_{n, l, m}(r, \theta, \phi) =& \sqrt{\left(\frac{2}{2 a_0}\right)^3 \frac{(n - l - 1)!}{2n(n+l)!}}
            e^{-\rho/2} L_{n-l-1}^{2l+1}(\rho) Y_l^m(\theta, \phi)

* :math:`a_0` is the Bohr radius, equal to
  :math:`a_0 = \frac{4\pi \epsilon_0 \hbar^2}{me^2}`.
* :math:`\rho` is a rescaled radial coordinate given by
  :math:`\frac{2}{na_0} r`.
* :math:`L_{n-l-1}^{2l+1}(\rho)` is a generalized Laguerre polynomial of
  degree :math:`n-l-1`.
* :math:`Y_l^m(\theta, \phi)` is the spherical harmonic of degree
  :math:`l` and order :math:`m`.
  :math:`\theta` is the polar coordinate angle and :math:`\phi` is the
  azimuthal coordinate angle.

Note that the energy :math:`E_{n, l, m}` only depend on the :math:`n`
quantum number.
The square root term in the expression for :math:`\psi_{n, l, m}` is a
pre-factor to ensure the squared wavefunction integrates to unity when
integarting over all space (this is critical for the probability
interpretation of the wavefunction to be sensible).
The radial behavior is given by :math:`e^{-\rho/2}L_{n-l-1}^{l+1}(\rho)`
and the angular behavior is given by :math:`Y_l^m(\theta, \phi)`.

===========================
Visualizing Atomic Orbitals
===========================

`atomview` is dedicated to visualizing the Hydrogen atomic orbitals
described above.
It can be challenging to visualize a complex-valued scalar function on
3D space but there are a few strategies we can use.
In this section we will build up our understanding of different
visualization techniques to build up to an understanding of the
visualizations provided by `atomview`.

-----------------------------
The :math:`(1, 0, 0)` orbital
-----------------------------

The simplest Hydrogen atomic orbital is the :math:`\psi_{1, 0, 0}`
orbital.
This wavefunction is given by

.. math::

    \psi_{1, 0, 0}(r, \theta, \phi) = \frac{1}{\sqrt{\pi} a_0^{3/2}} e^{-r/a_0}

We see that this orbital is purely a function of :math:`r` with no
angular :math:`\theta` or :math:`\phi` dependence.
This means we can simply visualize it's behavior on a regular 1D plot:

.. figure:: ../../scripts/figures/docs_figs/100_simple_1D.png
    :align: center
    :width: 400

We see that the wavefunction is maximal at the origin and then the
amplitude decreases exponentially as the radius increases.

The next more sophisticated way we can visualize this wavefunction
is by plotting the amplitude of the wavefunction on a 2D slice of space
using a density plot where the brightness of the plot corresponds to the
amplitude.

.. figure:: ../../scripts/figures/docs_figs/simple_100_2d.png
    :align: center
    :width: 400

In both the :math:`z` and :math:`y` slices the wavefunction appears as a
circle that is bright at the middle and whose brightness decreases as
the radius increases.
This begins to show the spherical symmetry of this wavefunction.
In fact, the wavefunction look the same no matter which 2D slice plane
passing through the origin was chosen.

Let us now consider 3D visualization techniques.
First, we can visualize the wavefunction as a 3D cloud where each voxel
of space is transparent, with an opacity proportional to the probability
of finding a particle there.
This is similar to viewing a regular cloud where the opacity of each
voxel of space is proportional to the density of cloud-stuff in that
region.

.. figure:: ../../scripts/figures/docs_figs/simple_100_volume_3d.png
    :align: center
    :width: 400

We see that this looks like a spherical cloud that is most dense in the
center.

We now turn to 3D iso-probability contour surface visualizations.
If we have a wavefunction :math:`\psi` then the squared magnitude
:math:`|\psi|^2` is related the probability of finding a particle at a
given location.
Suppose we pick a value :math:`p < \text{max}\left(|\psi|^2\right)`.
There will be a closed and bounded 2D surface of points in 3D space
which satisfy :math:`|\psi|^2 = p`.
If we integrate up the probability contained inside this surface then
can determine the probability :math:`P` that an electron is found inside
the surface.

.. math::

    P = \int_{|\psi|^2 < p} |\psi|^2 dV

For any chosen probability :math:`P` we can numerically determine the
required value for :math:`p` such that the corresponding iso-probability
contour :math:`|\psi|^2 = p` contains :math:`P` probability.
Below we plot two types of iso-probability contour plots for the
:math:`\psi_{1,0,0}` waveform.

.. figure:: ../../scripts/figures/docs_figs/simple_100_contour_3d_plots.png
    :align: center
    :width: 400

    Left: solid iso-probability contour plot for :math:`\psi_{1, 0, 0}`
    corresponding to :math:`P=0.5`. Right: Multiple transparent
    iso-probability contours for :math:`\psi_{1, 0, 0}` corresponding to
    :math:`P=[0.2, 0.4, 0.6]`. Each iso-probability has an opacity equal
    to the relative squared magnitude of the wavefunction on that
    surface. This plot gives a similar effect to the volume desnity
    plot.

We will find that iso-probability contour surface visualizations can
give us good intuitions for the general shape of an orbital even though
they don't technically give us information about the value of the
function at all points in 3D space.

-----------------------------
The :math:`(2, 1, 0)` orbital
-----------------------------

The next most complicated orbital is the :math:`(2, 1, 0)` orbital.
This wavefunction is given by

.. math::

    \psi_{2, 1, 0} = \frac{\sqrt{2}}{8\sqrt{\pi}a_0^{3/2}}
                     \left(r/a_0\right) e^{-\frac{1}{2}(r/a_0)}
                     \cos(\theta)

This orbital has a few important features beyond those of the
:math:`\psi_{1, 0, 0}` orbital.
The first is that it now has dependence on the polar angle
:math:`\theta` given by :math:`\cos(\theta)` (though there is no
dependence on the azimuthal angle :math:`\phi`).
The second is that the wavefunction is positive in some regions of space
(:math:`0 \le \theta < \pi/2`) and negative in others
(:math:`\pi/2 < \theta <= \pi`).
Below, we will introduce strategies to incorporate this information into
our visualizations.

First, as before, even though this wavefunction has angular dependence,
we can still visualize the radial dependence on a 1D plot.

.. figure:: ../../scripts/figures/docs_figs/radial_210_1d.png
    :align: center
    :width: 400

We see that wavefunction is now zero at the origin, then has a finite
lobe of amplitude before decaying exponentially at large radii.
Note also that this wavefunction has a larger radial extent than the
:math:`\psi_{1, 0, 0}` wavefunction.
Indeed, the wavefunction radial extent scales as :math:`n^2`.

We can again plot 2D density plots of :math:`z` and :math:`x` slices:

.. figure:: ../../scripts/figures/docs_figs/density_2d_210.png
    :align: center
    :width: 400

We see there is no density along the :math:`z=0` plane because this
plane corresponds to :math:`\theta=\pi/2` and :math:`\cos(\pi/2)=0`.
However, in the :math:`x=0` plane we now see two colors.
We see red for :math:`\theta<\pi/2` where the wavefunction is positive,
but we see that blue has been used for :math:`\theta>\pi/2` where the
wavefunction is negative.
We see there is a positive red lobe above the :math:`z=0` plane and a
negative blue lobe below the :math:`z=0` plane.

Finally, we can utilize the same three 3D visualization techniques from
above, simply adopting the red/blue convention for positive/negative
parts of the wavefunction.

.. figure:: ../../scripts/figures/docs_figs/multi_view_3d_210.png
    :align: center
    :width: 400

    Left: volume density visualization for :math:`\psi_{2,1,0}`.
    Center: Solid iso-probability contour visualization for
    :math:`\psi_{2, 1, 0}` corresponding to :math:`P=0.5`.
    Right: Transparent iso-probability contour visualization for
    :math:`\psi_{2, 1, 0}` corresponding to :math:`P=[0.2, 0.4, 0.6]`.
