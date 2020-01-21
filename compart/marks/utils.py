"""Utilities for base marks."""
import numpy as np


def rotation(theta):
    """Create a 2D rotation matrix."""
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def rotate_in_place(ary, shift, rot):
    """Perform a rotation of points in an array."""
    return np.dot(ary - shift, rotation(rot)) + shift
