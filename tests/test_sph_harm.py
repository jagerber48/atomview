import unittest
import timeit
import logging

import numpy as np
from numpy.testing import assert_allclose
from scipy.stats import sem
from sciform import (
    FormatOptions, ExpFormat, ExpMode, set_global_defaults, SciNumUnc
)

from src.atomview.utils import sph_harm_cartesian


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()

set_global_defaults(
    FormatOptions(
        exp_mode=ExpMode.ENGINEERING,
        exp_format=ExpFormat.PREFIX,
        ndigits=1,
        bracket_unc=True
    )
)

(n, l, m) = (3, 1, 1)
span = (1.5 * n) ** 2
n_steps = 101
single_linspace = np.linspace(-span, span, n_steps)
x, y, z = np.meshgrid(single_linspace, single_linspace,
                      single_linspace, indexing='ij')


class TestSphHarm(unittest.TestCase):
    def test_compare_scipy(self):
        ylm = sph_harm_cartesian(x, y, z, l, m, use_scipy=False)
        ylm_scipy = sph_harm_cartesian(x, y, z, l, m, use_scipy=True)

        assert_allclose(ylm, ylm_scipy)

    def test_benchmark_sph_harm_cartesian(self):
        num_trials = 10
        num_reps = 10
        t = timeit.repeat(lambda: sph_harm_cartesian(x, y, z, l, m),
                          repeat=num_reps, number=num_trials)

        mean_t = np.mean(t) / num_trials
        sem_t = sem(t) / num_trials

        logger.info(f'use_scipy=False: {SciNumUnc(mean_t, sem_t)}s')

    def test_benchmark_sph_harm_cartesian_scipy(self):
        num_trials = 10
        num_reps = 10
        t = timeit.repeat(lambda: sph_harm_cartesian(x, y, z, l, m,
                                                     use_scipy=True),
                          repeat=num_reps, number=num_trials)

        mean_t = np.mean(t) / num_trials
        sem_t = sem(t) / num_trials

        logger.info(f'use_scipy=True: {SciNumUnc(mean_t, sem_t)}s')
