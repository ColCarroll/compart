"""Squares, rectangles, line segments."""
import numpy as np

from .utils import rotate_in_place
from .ellipse import Ellipse


class Rectangle(Ellipse):
    """Rectangle and square class.

    Works by inscribing the rectangle in an ellipse, then using some geometry
    to throw out the chords of the ellipse that do not intersect with the
    rectangle.
    """

    @property
    def top(self):
        """Top of the rectangle."""
        return self.center[1] + self.height / 2

    @property
    def bottom(self):
        """Bottom of the rectangle."""
        return self.center[1] - self.height / 2

    @property
    def left(self):
        """Left edge of the rectangle."""
        return self.center[0] - self.width / 2

    @property
    def right(self):
        """Right edge of the rectangle."""
        return self.center[0] + self.width / 2

    def gen_points(self, *, n, fuzz, rot=None, rot_point=None):
        """Generate endpoints on the edges of the rectangle.

        Parameters
        ----------
        n: int > 0
            Number of endpoints to generate.
        fuzz: float
            How much extra noise to introduce at the endpoints.
        rot: float
            How much to rotate the rectangle around rot_point.
        rot_point: ndarray
            Point to rotate around, or center of the rectangle.

        Returns
        -------
        k x 2 x 2 ndarray,
            Note that k <= n, since we throw away any chords which do not
            intersect the rectangle.
        """
        if rot_point is None:
            rot_point = self.center
        X, Y = super().gen_points(n=n, fuzz=0, rot=None).T
        X, Y = X.T, Y.T
        times = np.empty((n, 4))

        # All lines will intersect with these four
        times[:, 0] = (self.left - X[:, 0]) / (X[:, 1] - X[:, 0])
        times[:, 1] = (self.right - X[:, 0]) / (X[:, 1] - X[:, 0])
        times[:, 2] = (self.top - Y[:, 0]) / (Y[:, 1] - Y[:, 0])
        times[:, 3] = (self.bottom - Y[:, 0]) / (Y[:, 1] - Y[:, 0])

        # Lines that intersect with the square will have to enter
        # the square with the 2nd line crossing
        times = np.sort(times, axis=1)
        new_x = X[:, 0] + (1e-7 + times[:, 1]) * (X[:, 1] - X[:, 0])
        new_y = Y[:, 0] + (1e-7 + times[:, 1]) * (Y[:, 1] - Y[:, 0])

        keep = np.all(
            np.vstack(
                (
                    (self.left < new_x) & (new_x < self.right),
                    (self.bottom < new_y) & (new_y < self.top),
                )
            ).T,
            axis=1,
        )
        times += 0.001 * fuzz * np.random.randn(*times.shape)

        X_new = np.empty(X[keep].shape)
        X_new[:, 0] = X[keep, 0] + times[keep, 1] * (X[keep, 1] - X[keep, 0])
        X_new[:, 1] = X[keep, 0] + times[keep, 2] * (X[keep, 1] - X[keep, 0])

        Y_new = np.empty(X[keep].shape)
        Y_new[:, 0] = Y[keep, 0] + times[keep, 1] * (Y[keep, 1] - Y[keep, 0])
        Y_new[:, 1] = Y[keep, 0] + times[keep, 2] * (Y[keep, 1] - Y[keep, 0])
        points = np.stack((X_new.T, Y_new.T)).T
        if rot is None:
            return points
        return rotate_in_place(points, rot_point, rot)


class Segment:
    """Line segment class.

    Wraps up some of the logic around rotating the rectangle, and parametrizing
    by start and end point, rather than center and dimensions.
    """

    def __init__(self, start, end):
        """Initialize class.

        Parameters
        ----------
        start: iterable of length 2
            Start point of the segment, (x, y)
        end: iterable of length 2
            End point of the segment, (x, y)
        """
        start, end = np.array(start), np.array(end)
        tangent = end - start
        self._length = np.sqrt((tangent ** 2).sum())
        if tangent[1] == 0:
            self._theta = np.pi / 2
        else:
            self._theta = np.arctan(tangent[0] / tangent[1])
        self.center = start + tangent / 2
        self.start = start

    def plot(self, *, ax, color, lw=1, n=1000, fuzz=4, width=0.02, **kwargs):
        """Add this plot to the axis.

        Parameters
        ----------
        ax: Axes
            Matplotlib axis to add the art to
        color: str
            Color to use. Must be readable by `matplotlib.colors.to_rgba`. Can be
            something like "black", "k", or "#ffffff".
        lw: float > 0
            Linewidth to use for chords in the segment
        n: int > 0
            Number of chords to use for the segment
        fuzz: float > 0
            How ragged edges of the segment should be
        width: float > 0
            How wide should the line segment be
        kwargs:
            Passed to `Rectangle.plot`

        Returns
        -------
        None
        """
        rect = Rectangle(center=self.center, width=width, height=self._length)
        alpha = kwargs.pop("alpha", 0.2)
        return rect.plot(
            ax=ax,
            color=color,
            rot=self._theta,
            n=n,
            lw=lw,
            fuzz=fuzz,
            alpha=alpha,
            rot_point=self.center,
            **kwargs,
        )
