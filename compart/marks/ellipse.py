"""Circles and ellipses."""
from matplotlib.path import Path
from matplotlib.collections import PathCollection
import numpy as np

from .utils import rotate_in_place, jittered_colors


class Ellipse:
    """Base class for most artists.

    Works by uniformly randomly selecting two angles and connecting those
    points with a straight line. Note that for circles this is equivalent to
    uniformly selecting points on the circumference, but this is not true for
    ellipses!
    """

    def __init__(self, *, center, width, height):
        """Initialize class.

        Parameters
        ----------
        center: iterable of length 2
            Center of the circle or ellipse.
        width: float > 0
            Width of ellipse
        height: float > 0
            Height of ellipse
        """
        self.center = np.array(center)
        self.width = width
        self.height = height

    def gen_points(self, *, n, fuzz, rot=None, rot_point=None):
        """Generate endpoints of the chords of the ellipse.

        Parameters
        ----------
        n: int
            Number of pairs of points to generate
        fuzz: float > 0
            How much to shift the endpoints in and out.
        rot: Optional[float]
            How much to rotate the resulting shape
        rot_point: ndarray
            Point to rotate around, or center of the rectangle.

        Returns
        -------
        n x 2 x 2 ndarray
        You can iterate over this and have an array of a startpoint and
        endpoint for chords.
        """
        if rot_point is None:
            rot_point = self.center
        thetas = 2 * np.pi * np.random.rand(n, 2)
        fuzz = 0.001 * fuzz * np.random.randn(*thetas.shape)
        X, Y = np.array(
            (
                (fuzz + self.width) * np.cos(thetas) + self.center[0],
                (fuzz + self.height) * np.sin(thetas) + self.center[1],
            )
        )
        points = np.stack((X.T, Y.T)).T
        if rot is None:
            return points
        return rotate_in_place(points, rot_point, rot)

    def plot(
        self, *, ax, color, lw=2, n=30000, fuzz=3, rot=None, rot_point=None, **kwargs
    ):
        """Add this plot to the axis.

        Parameters
        ----------
        ax: Axes
            Matplotlib axis to add the art to
        color: str
            Color to use. Must be readable by `matplotlib.colors.to_rgba`. Can be
            something like "black", "k", or "#ffffff".
        lw: float > 0
            Linewidth to use for chords
        n: int > 0
            Number of chords to use
        fuzz: float > 0
            How ragged edges should be
        rot: float
            How much to rotate the shape, in radians
        rot_point: ndarray (optional)
            What point to rotate the shape around (default is the center)
        kwargs:
            Passed to `PathCollection`

        Returns
        -------
        None
        """
        colors = jittered_colors(color, n)
        alpha = kwargs.pop("alpha", 0.05)
        colors[:, -1] = alpha
        ax.add_collection(
            PathCollection(
                [
                    Path(p)
                    for p in self.gen_points(
                        n=n, fuzz=fuzz, rot=rot, rot_point=rot_point
                    )
                ],
                linewidths=lw,
                edgecolors=colors,
                facecolors="none",
                **kwargs,
            )
        )
