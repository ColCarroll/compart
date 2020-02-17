"""Utilities for base marks."""
from matplotlib.colors import to_rgba
import numpy as np


def rotation(theta):
    """Create a 2D rotation matrix."""
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def rotate_in_place(ary, shift, rot):
    """Perform a rotation of points in an array."""
    return np.dot(ary - shift, rotation(rot)) + shift


def jittered_colors(color, n_colors, noise=50):
    """Produce colors near a chosen color.

    Parameters
    ----------
    color: str
        Valid matplotlib color string
    n_colors: int
        Number of nearby colors to produce
    noise: int
        How much to jitter the color. Default 50.

    Returns
    -------
    np.ndarray
      n_colors x 4 array of rgba values
    """
    color = np.array(to_rgba(color)) * 255
    colors = np.tile(color.reshape(-1, 1), n_colors).T
    colors[:, :3] += np.random.randint(-noise, noise, (n_colors, 3))

    return np.minimum(255, np.maximum(0, colors)) / 255
