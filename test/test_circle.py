import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_allclose

from compart.marks import Ellipse


def test_points_on_circumference():
    radius = 2
    n_points = 100
    circ = Ellipse(center=np.zeros(2), width=radius, height=radius)

    points = circ.gen_points(n=n_points, fuzz=0)

    assert points.shape == (n_points, 2, 2)
    assert_allclose(np.sum(points ** 2, axis=2), radius ** 2)


def test_plot_works():
    circ = Ellipse(center=np.zeros(2), width=1, height=1)
    fig, ax = plt.subplots()
    circ.plot(ax=ax, color="orange")
