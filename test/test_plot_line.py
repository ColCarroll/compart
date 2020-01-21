import matplotlib.pyplot as plt
import numpy as np

from compart.plots import plot_line, plot_hline, plot_vline


def test_plot_line_works():
    _, ax = plt.subplots()
    t = np.linspace(-2, 2)
    plot_line(ax, t, t * t, "orange", n=20)


def test_plot_hline_works():
    _, ax = plt.subplots()
    plot_hline(ax, 3, 2, 3, "orange")


def test_plot_vline_works():
    _, ax = plt.subplots()
    plot_vline(ax, 3, 2, 3, "orange")
