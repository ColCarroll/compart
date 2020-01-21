"""Convenience function to plot a line."""
import numpy as np

from ..marks import Segment


def plot_line(ax, x, y, color, lw=0.05, n=150, fuzz=100, width=0.02, **kwargs):
    """Plot a line using x and y values.

    Parameters
    ----------
        ax: Axes
            Matplotlib axis to add the art to
        x: ndarray or iterable
            x-values of line
        y: ndarray or iterable
            y-values of line
        color: str
            Color to use. Must be readable by `matplotlib.colors.to_rgba`. Can be
            something like "black", "k", or "#ffffff".
        lw: float > 0
            Linewidth to use for chords in each segment
        n: int > 0
            Number of chords to use for each segment (careful!)
        fuzz: float > 0
            How ragged edges of the segment should be
        width: float > 0
            How wide should the line be
        kwargs:
            Passed to `Segment.plot`

    Returns
    -------
    None
    """
    data = np.vstack((x, y)).T
    kwargs.setdefault("alpha", 0.2)

    for start, end in zip(data, data[1:]):
        seg = Segment(start, end)
        seg.plot(ax=ax, color=color, lw=lw, n=n, fuzz=fuzz, width=width, **kwargs)


def plot_vline(ax, x, ymin, ymax, color, lw=0.05, n=150, fuzz=5, width=0.02, **kwargs):
    """Specialized vertical line plot.

    Squares look better than

    Parameters
    ----------
        ax: Axes
            Matplotlib axis to add the art to
        x: float
            x-value of vertical line
        ymin: float
            lower endpoint of line
        ymax: float
            upper endpoint of line
        color: str
            Color to use. Must be readable by `matplotlib.colors.to_rgba`. Can be
            something like "black", "k", or "#ffffff".
        lw: float > 0
            Linewidth to use for chords in each segment
        n: int > 0
            Number of chords to use for each segment (careful!)
        fuzz: float > 0
            How ragged edges of the segment should be
        width: float > 0
            How wide should the line be
        kwargs:
            Passed to `Segment.plot`

    Returns
    -------
    None
    """
    y = np.linspace(ymin, ymax, (ymax - ymin) / width)
    x = x * np.ones_like(y)
    return plot_line(ax, x, y, color, lw=lw, n=n, fuzz=fuzz, width=width, **kwargs)


def plot_hline(ax, y, xmin, xmax, color, lw=0.05, n=150, fuzz=5, width=0.02, **kwargs):
    """Specialized horizontal line plot.

    Squares look better than

    Parameters
    ----------
        ax: Axes
            Matplotlib axis to add the art to
        y: float
            y-value of horizontal line
        xmin: float
            left endpoint of line
        xmax: float
            right endpoint of line
        color: str
            Color to use. Must be readable by `matplotlib.colors.to_rgba`. Can be
            something like "black", "k", or "#ffffff".
        lw: float > 0
            Linewidth to use for chords in each segment
        n: int > 0
            Number of chords to use for each segment (careful!)
        fuzz: float > 0
            How ragged edges of the segment should be
        width: float > 0
            How wide should the line be
        kwargs:
            Passed to `Segment.plot`

    Returns
    -------
    None
    """
    x = np.linspace(xmin, xmax, int((xmax - xmin) / width))
    y = y * np.ones_like(x)
    return plot_line(ax, x, y, color, lw=lw, n=n, fuzz=fuzz, width=width, **kwargs)
