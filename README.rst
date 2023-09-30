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

.. figure:: ../../scripts/figures/docs_figs/320_multi_view.png
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
It can be challenging to visualize complex-valued scalar function on 3D
space but there are a few strategies we can use.

The first strategy is to
