import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Global plotting configuration
# -----------------------------
sns.set_theme(style="ticks", context="paper")

order = [r"$\kappa=0$", r"$\kappa=5\times10^{-4}$", r"$\kappa=10^{-3}$", r"$\kappa=5\times10^{-3}$", r"$\kappa=9\times10^{-3}$"]
tick_labels = ["0", r"$5\times10^{-4}$", r"$10^{-3}$", r"$5\times10^{-3}$", r"$9\times10^{-3}$"]

# Ordered single-hue palette (light -> dark)
palette = {
    order[0]: "#DCEAF7",
    order[1]: "#9ECAE1",
    order[2]: "#4A90C2",
    order[3]: "#084A91",
    order[4]: "#002D72"
}
palette_alt = {
    order[0]: "#E5F5E0",
    order[1]: "#A1D99B",
    order[2]: "#31A354",
    order[3]: "#006D2C",
    order[4]: "#00441B"
}

_num_re = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

def to_float(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.number)):
        return float(x)
    m = _num_re.search(str(x))
    return float(m.group(0)) if m else np.nan

def load_and_metrics(path, label):
    df = pd.read_csv(path)
    for c in ["VT", "ST", "payoff", "V0", "S0", "kappa", "alpha_step", "beta_step"]:
        df[c] = df[c].map(to_float)

    df["RSE"] = (df["VT"] - df["payoff"]) / df["ST"].where(df["ST"].abs() > 1e-12)
    df["Pj"] = df["V0"] / df["S0"].where(df["S0"].abs() > 1e-12)
    df["kappa"] = label
    return df[["i","kappa", "RSE", "Pj", "alpha_step", "beta_step"]].dropna()

def plot_rse(
    df,
    ycol="RSE",
    palette=None,
    savepath="Fig_RSE.pdf"
):
    fig, ax = plt.subplots(figsize=(6, 3.8), dpi=120)

    # Default palette if none provided
    if palette is None:
        palette = {
            order[0]: "#DCEAF7",
            order[1]: "#9ECAE1",
            order[2]: "#4A90C2",
            order[3]: "#084A91",
            order[4]: "#002D72"
        }

    # Clean data
    dff = df[np.isfinite(df[ycol])].copy()
    dff["kappa"] = pd.Categorical(dff["kappa"], categories=order, ordered=True)

    # Boxplot
    sns.boxplot(
        data=dff, x="kappa", y=ycol,
        order=order, palette=palette, hue="kappa", hue_order=order,
        width=0.55, fliersize=0, linewidth=1.0, ax=ax, dodge=False, legend=False
    )

    # Points
    sns.stripplot(
        data=dff, x="kappa", y=ycol,
        order=order, ax=ax,
        color="0.15", alpha=0.4, size=2.5, jitter=0.15
    )

    # Reference line
    ax.axhline(0, color="black", ls="--", lw=0.8)

    # Labels

    ax.set(xlabel="", ylabel="")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(tick_labels)

    sns.despine(ax=ax)

    plt.savefig(savepath, bbox_inches="tight")
    plt.show()

def plot_pj_logscale(df, ycol="Pj", savepath="Fig_Pj_logscale.pdf"):
    d = df[np.isfinite(df[ycol]) & (df[ycol] > 0)].copy()
    d["kappa"] = pd.Categorical(d["kappa"], categories=order, ordered=True)

    fig, ax = plt.subplots(figsize=(6.0, 3.8), dpi=120)

    sns.boxplot(
        data=d, x="kappa", y=ycol,
        order=order, hue="kappa", hue_order=order,
        palette=palette, dodge=False, legend=False,
        width=0.55, fliersize=0, linewidth=1.0, ax=ax
    )
    sns.stripplot(
        data=d, x="kappa", y=ycol, order=order, ax=ax,
        color="0.15", alpha=0.40, size=2.6, jitter=0.14
    )

    ax.set_yscale("log")
    ax.set_ylabel("")
    ax.set_xlabel("")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(tick_labels)

    sns.despine(ax=ax)
    fig.subplots_adjust(bottom=0.16, top=0.90)
    plt.savefig(savepath, bbox_inches="tight")
    plt.show()


# Cost Impact
def compute_I(df, pj_col="Pj", kappa_col="kappa", id_col="j"):
    d = df[[id_col, kappa_col, pj_col]].copy()
    d = d[np.isfinite(d[pj_col])]
    
    # Map the LaTeX string labels back to actual numeric values for the math
    kappa_map = {
        r"$\kappa=0$": 0.0, 
        r"$\kappa=5\times10^{-4}$": 5e-4, 
        r"$\kappa=10^{-3}$": 1e-3, 
        r"$\kappa=5\times10^{-3}$": 5e-3,
        r"$\kappa=9\times10^{-3}$": 9e-3
    }
    d["kappa_numeric"] = d[kappa_col].map(kappa_map)
    d = d.dropna(subset=["kappa_numeric"])

    # baseline P^j(0)
    p0 = (d[d["kappa_numeric"] == 0.0][[id_col, pj_col]]
          .rename(columns={pj_col: "P0"}))

    out = d.merge(p0, on=id_col, how="inner")
    out = out[out["kappa_numeric"] > 0].copy()
    
    # Calculate Impact Cost
    out["I"] = (out[pj_col] - out["P0"]) / out["kappa_numeric"]
    return out

def plot_impact_cost(df_I, ycol="I", savepath="Fig_Impact_Cost.pdf"):
    # Filter only to the non-zero kappas used in calculating I
    plot_order = [r"$\kappa=5\times10^{-4}$", r"$\kappa=10^{-3}$", r"$\kappa=5\times10^{-3}$", r"$\kappa=9\times10^{-3}$"]
    plot_labels = [r"$5\times10^{-4}$", r"$10^{-3}$", r"$5\times10^{-3}$", r"$9\times10^{-3}$"]

    fig, ax = plt.subplots(figsize=(6.0, 3.8), dpi=120)

    sns.boxplot(
        data=df_I, x="kappa", y=ycol,
        order=plot_order, hue="kappa", hue_order=plot_order,
        palette=palette, dodge=False, legend=False,
        width=0.55, fliersize=0, linewidth=1.0, ax=ax
    )
    sns.stripplot(
        data=df_I, x="kappa", y=ycol, order=plot_order, ax=ax,
        color="0.15", alpha=0.40, size=2.6, jitter=0.14
    )

    ax.set_ylabel(r"Cost Impact $I^j(\kappa)$")
    ax.set_xlabel("")
    ax.set_xticks(range(len(plot_order)))
    ax.set_xticklabels(plot_labels)

    sns.despine(ax=ax)
    plt.savefig(savepath, bbox_inches="tight")
    plt.show()
