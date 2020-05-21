from functools import wraps

import numpy as np
import seaborn as sn
import statsmodels.tsa.api as sm
from matplotlib import pyplot as plt

from utils import shorten_dates

sn.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (20, 10)


def plot_constructor(func):
    @wraps(func)
    def wrapper(*args, title=None, xlabel=None, ylabel=None, **kwargs):
        func(*args, **kwargs)
        plt.title(title)
        plt.legend()
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()

    return wrapper


@plot_constructor
def plot_graph(df, label):
    plt.plot(df, "-", linewidth=1, label=label)
    plt.xticks(shorten_dates(df.index.values), rotation=90)
    plt.locator_params(axis="x", nbins=10)


@plot_constructor
def plot_changes(df, label):
    plt.plot((df["rate"] - df["rate"].shift(1))[1:], "-", linewidth=1, label=label)
    plt.xticks(shorten_dates(df.index.values), rotation=90)


@plot_constructor
def plot_histogram(df, label):
    bins = 12
    hist_data = np.histogram(df["rate"].values, bins)
    plt.hist(df["rate"].values, bins, label="Гистограмма")
    plt.plot(
        hist_data[1][1:],
        hist_data[0],
        label=label,
        linestyle="--",
        color="red",
        linewidth=5
    )


@plot_constructor
def plot_std(df, label):
    plt.plot(
        df.index[::5].values,
        [df["rate"][i:i + 5].std() for i in range(0, len(df), 5)],
        linewidth=1,
        label=label
    )
    plt.xticks(shorten_dates(df.index.values), rotation=90)


def plot_decompose(df):
    sm.seasonal_decompose(df["rate"]).plot()
    plt.show()
