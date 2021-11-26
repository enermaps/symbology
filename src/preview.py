#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# set paths
SRCDIR = Path(__file__).parent
DATADIR = SRCDIR.parent / "data"
CLRTABLE = DATADIR / "color-tables.csv"
PREVIEW = SRCDIR / "preview.png"
SEP = ","


def get_colors(clrpath: Path) -> Dict[str, List[Tuple[float, float, float]]]:
    clrs = {}
    with open(CLRTABLE, mode="r") as clrfile:
        # skip the header
        _ = next(clrfile).split(SEP)
        for line in clrfile:
            key, *vals = line.split(SEP)
            clrs[key] = [
                tuple([int(v[2:]) / 255.0 for v in rgb.split()]) for rgb in vals
            ]
    return clrs


def palplot(pal, size=1, ax=None):
    """Plot the values in a color palette as a horizontal array.

    Parameters
    ----------
    pal : sequence of matplotlib colors
        colors, i.e. as returned by seaborn.color_palette()
    size :
        scaling factor for size of plot

    """
    n = len(pal)
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(n * size, size))
    ax.imshow(
        np.arange(n).reshape(1, n),
        cmap=mpl.colors.ListedColormap(list(pal)),
        interpolation="nearest",
        aspect="auto",
    )
    ax.set_xticks(np.arange(n) - 0.5)
    ax.set_yticks([-0.5, 0.5])
    # Ensure nice border between colors
    ax.set_xticklabels(["" for _ in range(n)])
    # The proper way to set no ticks
    ax.yaxis.set_major_locator(ticker.NullLocator())
    return ax


def plot_symbology(clrs: Dict[str, List[Tuple[float, float, float]]], fname: Path):
    keys = sorted(clrs.keys())
    n = len(clrs[keys[0]])
    size = 1
    fig, axes = plt.subplots(len(clrs), 1, figsize=(n * size + 2, size * len(keys) + 4))
    for key, ax in zip(keys, axes):
        print(f"{key}: {clrs[key]}")
        palplot(clrs[key][::-1], ax=ax)
        ax.set_ylabel(key)
    axes[0].set_title("Symbology")
    fig.tight_layout()
    fig.savefig(fname, dpi=300)


if __name__ == "__main__":
    clrs = get_colors(CLRTABLE)
    plot_symbology(clrs, PREVIEW)
