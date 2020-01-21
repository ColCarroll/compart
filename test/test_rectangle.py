import matplotlib.pyplot as plt
import numpy as np
from numpy.testing import assert_almost_equal

from compart.marks import Rectangle, Segment


def test_points_on_edge():
    width = 3
    height = 1
    n_points = 1000
    rect = Rectangle(center=np.zeros(2), width=width, height=height)

    points = rect.gen_points(n=n_points, fuzz=0)
    max_x, max_y = points.max(axis=1).max(axis=0)
    min_x, min_y = points.min(axis=1).min(axis=0)
    assert_almost_equal(max_x, width / 2)
    assert_almost_equal(min_x, -width / 2)
    assert_almost_equal(max_y, height / 2)
    assert_almost_equal(min_y, -height / 2)
    assert points.shape[0] <= n_points


def test_plot_works():
    square = Rectangle(center=np.zeros(2), width=1, height=1)
    _, ax = plt.subplots()
    square.plot(ax=ax, color="orange")


def test_segment_works():
    seg = Segment(np.zeros(2), np.ones(2))
    _, ax = plt.subplots()
    seg.plot(ax=ax, color="orange")
