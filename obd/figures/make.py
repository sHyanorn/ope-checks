"""Draw the figures of the registered and post hoc results.

    python -m obd.figures.make

Reads obd/results and obd/posthoc/results and writes three figures to obd/figures, each as
<name>-light.png and <name>-dark.png. With --pdf it writes each figure once, as a vector
<name>.pdf on a white page. Needs matplotlib: pip install -e ".[figures]".
"""

import argparse
import json
from pathlib import Path

import matplotlib.style
from matplotlib.figure import Figure

HERE = Path(__file__).parent
REGISTERED = HERE.parent / "results"
POSTHOC = HERE.parent / "posthoc" / "results"

WIDTH_IN, ROW_IN, DPI = 7.5, 0.3, 240  # 1,800 pixels wide
THEMES = {
    "light": {
        "surface": "#fcfcfb",
        "ink": "#0b0b0b",
        "secondary": "#52514e",
        "muted": "#898781",
        "grid": "#e1e0d9",
        "blue": "#2a78d6",
        "orange": "#eb6834",
        "aqua": "#1baf7a",
    },
    "dark": {
        "surface": "#1a1a19",
        "ink": "#f0efec",
        "secondary": "#c3c2b7",
        "muted": "#898781",
        "grid": "#2c2c2a",
        "blue": "#3987e5",
        "orange": "#d95926",
        "aqua": "#199e70",
    },
}
PRINT = THEMES["light"] | {"surface": "#ffffff"}
CAMPAIGNS = {"all": "All", "women": "Women's", "men": "Men's"}
UNITS = {
    "rows": ("rows", "orange"),
    "impressions": ("impressions", "aqua"),
    "blocks": ("ten-minute blocks (registered)", "blue"),
}


def header(label):
    return {"label": label}


def interval(label, color, quantity):
    low, high = quantity["interval"]
    return {"label": label, "color": color, "at": quantity["estimate"], "low": low, "high": high}


def bar(label, color, value):
    return {"label": label, "color": color, "value": value}


def draw(panels, xlabel, theme, note=None):
    """A figure with one axes per (title, rows) of `panels`, stacked on a shared x axis. A row
    is a `header`, an `interval` (point and line) or a `bar` from zero with its value."""
    sizes = [len(rows) for _, rows in panels]
    fig = Figure(
        figsize=(WIDTH_IN, ROW_IN * sum(sizes) + 0.45 * len(panels) + 0.8),
        dpi=DPI,
        facecolor=theme["surface"],
        layout="constrained",
    )
    axes = fig.subplots(
        len(panels), sharex=True, squeeze=False, gridspec_kw={"height_ratios": sizes}
    )
    for ax, (title, rows) in zip(axes[:, 0], panels, strict=True):
        ax.set_facecolor(theme["surface"])
        ax.set_title(title, loc="left", fontsize=9, color=theme["secondary"])
        ax.set_ylim(len(rows) - 0.5, -0.5)
        ax.set_yticks(range(len(rows)), [row["label"] for row in rows])
        ax.tick_params(length=0, labelsize=9, labelcolor=theme["secondary"])
        for tick, row in zip(ax.get_yticklabels(), rows, strict=True):
            if "color" not in row:
                tick.set(color=theme["ink"], fontweight="bold")
        ax.grid(axis="x", color=theme["grid"], linewidth=0.8)
        ax.set_axisbelow(True)
        ax.spines[:].set_visible(False)
        bars = any("value" in row for row in rows)
        ax.margins(x=0.12 if bars else 0.04)  # bars need room for their values
        for y, row in enumerate(rows):
            color = theme.get(row.get("color"))
            if "at" in row:
                ax.plot(
                    [row["low"], row["high"]],
                    [y, y],
                    color=color,
                    linewidth=1.6,
                    solid_capstyle="butt",
                )
                ax.plot(row["at"], y, "o", ms=7.5, mfc=color, mec=theme["surface"], mew=1.5)
            elif "value" in row:
                ax.barh(y, row["value"], height=0.3, color=color)
                ax.annotate(
                    f"{row['value']:.3f}",
                    (row["value"], y),
                    xytext=(6, 0),
                    textcoords="offset points",
                    va="center_baseline",
                    fontsize=8.5,
                    color=theme["ink"],
                )
        if bars:
            ax.set_xlim(left=0)
    axes[-1, 0].set_xlabel(xlabel, fontsize=9, color=theme["secondary"])
    if note:
        fig.suptitle(note, x=0.01, ha="left", fontsize=10, color=theme["ink"])
    return fig


def ratio_axis(fig, theme):
    """Mark 1, where an estimate equals the on-policy click rate."""
    for ax in fig.axes:
        ax.axvline(1, color=theme["muted"], linewidth=1, zorder=1)


def resampling_units(units, theme):
    """Post hoc: the IPS ratio of H3 with its interval under three resampling units."""

    def rows(campaign):
        h3 = units[campaign]["h3"]
        marks = [interval(label, color, h3[unit]["ips"]) for unit, (label, color) in UNITS.items()]
        return [header(CAMPAIGNS[campaign]), *marks]

    fig = draw(
        [
            ("Confirmatory campaigns", rows("all") + rows("women")),
            ("Development campaign, enters no verdict", rows("men")),
        ],
        "IPS estimate over on-policy click rate\n"
        f"point, and 2.5th to 97.5th percentile of {units['replicates']:,} replicates",
        theme,
        note="Post hoc comparison of resampling units",
    )
    ratio_axis(fig, theme)
    return fig


def confirmatory_estimates(registered, theme):
    """Registered: the fixed-prior IPS ratio of H3 and the aligned estimate of H4."""
    pooled = registered["pooled"]
    weights = ", ".join(f"{pooled['weights'][c]:.2f}" for c in ("all", "women"))
    rows = []
    for name in ("all", "women", "pooled"):
        result = registered[name]
        if name == "pooled":
            label, rho = f"Pooled, weights {weights}", "h4.rho"
            widths = sorted(set(result["h4"]["widths"].values()))
        else:
            label, rho = CAMPAIGNS[name], f"h4.rho.{result['h4']['width']}"
            widths = [result["h4"]["width"]]
        aligned = f"aligned estimate, {' and '.join(map(str, widths))}-hour periods (H4)"
        rows += [
            header(label),
            interval("fixed-prior IPS (H3)", "blue", result["quantities"]["h3.ips"]),
            interval(aligned, "orange", result["quantities"][rho]),
        ]
    fig = draw(
        [("Registered results, confirmatory campaigns", rows)],
        "Estimate over on-policy click rate\n"
        f"point, and 2.5th to 97.5th percentile of {pooled['replicates']:,} block replicates",
        theme,
    )
    ratio_axis(fig, theme)
    return fig


def prior_distance(registered, theme):
    """Registered: H1's distance between the prior and the BTS log with its noise floor, and
    the distance in the first hour of the week, which enters no rule."""
    week, first = [], []
    for name in ("all", "women"):
        h1 = registered[name]["h1"]
        week += [
            header(CAMPAIGNS[name]),
            bar("prior and BTS log, by hour (D)", "blue", h1["d"]),
            bar("noise floor: alternate blocks within the hour (D0)", "muted", h1["d0"]),
        ]
        first += [header(CAMPAIGNS[name])]
        first += [bar(f"position {k}", "blue", v) for k, v in enumerate(h1["first_hour"], 1)]
    return draw(
        [
            ("Registered results, confirmatory campaigns, whole week", week),
            ("First hour of the week, prior and BTS log (no rule, no noise floor)", first),
        ],
        "Total variation distance",
        theme,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--registered", type=Path, default=REGISTERED)
    parser.add_argument("--posthoc", type=Path, default=POSTHOC)
    parser.add_argument("--out", type=Path, default=HERE)
    parser.add_argument("--pdf", action="store_true", help="vector PDF files on a white page")
    args = parser.parse_args(argv)
    registered = {
        name: json.loads((args.registered / f"{name}.json").read_text())
        for name in ("all", "women", "pooled")
    }
    units = json.loads((args.posthoc / "units.json").read_text())
    figures = {
        "resampling-units": lambda theme: resampling_units(units, theme),
        "confirmatory-estimates": lambda theme: confirmatory_estimates(registered, theme),
        "prior-distance": lambda theme: prior_distance(registered, theme),
    }
    files = (
        {".pdf": PRINT} if args.pdf else {f"-{mode}.png": theme for mode, theme in THEMES.items()}
    )
    # Default settings, whatever matplotlibrc the machine has; text in a PDF stays text
    with matplotlib.style.context("default"), matplotlib.rc_context({"pdf.fonttype": 42}):
        for name, figure in figures.items():
            for ending, theme in files.items():
                figure(theme).savefig(args.out / f"{name}{ending}")
                print(f"wrote {args.out / f'{name}{ending}'}")


if __name__ == "__main__":
    main()
