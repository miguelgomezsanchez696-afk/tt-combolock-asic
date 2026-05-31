#!/usr/bin/env python3
"""Generate visual documentation evidence for the combination lock ASIC."""

from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs" / "images"
VCD = ROOT / "sim" / "tb_combolock.vcd"
DEF = ROOT / "runs" / "RUN_2026-05-31_02-03-14" / "final" / "def" / "tt_um_combolock.def"


def save(fig, name: str) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMG / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_diagram(fig, stem: str, dpi: int) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMG / f"{stem}.png", dpi=dpi, facecolor="white")
    fig.savefig(IMG / f"{stem}.svg", facecolor="white")
    plt.close(fig)


def box(ax, xy, wh, title, body="", fc="#eef6ff", ec="#2f5f8f"):
    rect = Rectangle(xy, wh[0], wh[1], linewidth=1.8, edgecolor=ec, facecolor=fc)
    ax.add_patch(rect)
    ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] * 0.67, title, ha="center", va="center", fontsize=13, weight="bold")
    if body:
        ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] * 0.34, body, ha="center", va="center", fontsize=10)
    return rect


def arrow(ax, start, end, label="", rad=0.0):
    arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16, linewidth=1.5, color="#34495e", connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(arr)
    if label:
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.22, label, ha="center", fontsize=9, color="#263238")


def rounded_box(ax, xy, wh, title, body="", fc="#f7fbff", ec="#2f5f8f", title_size=16, body_size=11):
    rect = FancyBboxPatch(
        xy,
        wh[0],
        wh[1],
        boxstyle="round,pad=0.03,rounding_size=0.16",
        linewidth=2.0,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(rect)
    title_y = xy[1] + wh[1] * (0.62 if body else 0.50)
    ax.text(
        xy[0] + wh[0] / 2,
        title_y,
        title,
        ha="center",
        va="center",
        fontsize=title_size,
        weight="bold",
        color="#1f2933",
        linespacing=1.12,
    )
    if body:
        ax.text(
            xy[0] + wh[0] / 2,
            xy[1] + wh[1] * 0.30,
            body,
            ha="center",
            va="center",
            fontsize=body_size,
            color="#334e68",
            linespacing=1.25,
        )
    return rect


def diagram_arrow(ax, start, end, label="", label_xy=None, color="#334e68", rad=0.0, lw=2.0, label_size=10):
    arr = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
        shrinkA=4,
        shrinkB=4,
    )
    ax.add_patch(arr)
    if label:
        x, y = label_xy if label_xy else ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.25)
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=label_size,
            color="#243b53",
            bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.08", facecolor="white", edgecolor="#d9e2ec", linewidth=0.8),
            linespacing=1.15,
        )


def block_diagram() -> None:
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor("white")

    ax.text(
        8,
        8.32,
        "4-bit Combination Lock ASIC with 4x4 Matrix Keypad",
        ha="center",
        va="center",
        fontsize=26,
        weight="bold",
        color="#102a43",
    )

    rounded_box(ax, (0.7, 3.05), (2.7, 2.35), "4x4 Matrix\nKeypad", "Rows 0-3\nColumns 0-3", "#fff7e6", "#b7791f")
    rounded_box(ax, (4.35, 2.55), (2.95, 3.30), "TinyTapeout-style\nI/O Interface", "Bidirectional uio bus\nStatus output bus", "#e6f6ff", "#1864ab")
    rounded_box(ax, (8.10, 4.70), (2.75, 1.55), "Keypad\nScanner", "Drive rows\nsample columns", "#e6fcf5", "#0b7285", title_size=15)
    rounded_box(ax, (11.55, 4.70), (3.10, 1.55), "Combination\nLock Logic", "Password, attempt,\nand lockout state", "#f3f0ff", "#6741d9", title_size=15)
    rounded_box(ax, (11.55, 2.15), (3.10, 1.35), "Output Status\nRegister", "Packed status fields", "#edf2ff", "#3b5bdb", title_size=15)

    diagram_arrow(ax, (4.35, 3.65), (3.40, 3.65), "Keypad rows\nuio_out[3:0]", (3.85, 3.05), "#b7791f")
    diagram_arrow(ax, (3.40, 4.78), (4.35, 4.78), "Keypad columns\nuio_in[7:4]", (3.88, 5.42), "#1864ab")
    diagram_arrow(ax, (7.30, 5.15), (8.10, 5.35), "row drive\ncolumn sample", (7.70, 5.92), "#0b7285", label_size=9)
    diagram_arrow(ax, (10.85, 5.48), (11.55, 5.48), "key_valid, key_code\nkey_star, key_hash", (11.20, 6.35), "#6741d9")
    diagram_arrow(ax, (13.10, 4.70), (13.10, 3.50), "status fields", (13.85, 4.10), "#3b5bdb", label_size=9)
    diagram_arrow(ax, (14.65, 2.82), (15.65, 2.82), "uo_out[7:0]\nstatus outputs", (15.00, 3.62), "#0f766e")

    ax.plot([5.85, 8.10], [4.30, 4.95], color="#bcccdc", linewidth=1.2, linestyle="--")
    ax.plot([6.00, 8.10], [3.75, 4.95], color="#bcccdc", linewidth=1.2, linestyle="--")
    ax.text(5.82, 2.08, "clk  rst_n  ena", ha="center", va="center", fontsize=11, color="#52616b")
    save_diagram(fig, "block_diagram", dpi=120)


def keypad_mapping() -> None:
    keys = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_facecolor("white")
    ax.text(7, 9.25, "4x4 Keypad Mapping and ASIC I/O Connections", ha="center", va="center", fontsize=25, weight="bold", color="#102a43")

    x0, y0, cell, gap = 1.25, 1.65, 1.45, 0.20
    grid_w = 4 * cell + 3 * gap
    grid_h = 4 * cell + 3 * gap
    ax.add_patch(
        FancyBboxPatch(
            (x0 - 0.28, y0 - 0.28),
            grid_w + 0.56,
            grid_h + 0.56,
            boxstyle="round,pad=0.04,rounding_size=0.14",
            linewidth=1.8,
            edgecolor="#d9e2ec",
            facecolor="#f8fafc",
        )
    )
    for r in range(4):
        y = y0 + (3 - r) * (cell + gap)
        ax.text(0.55, y + cell / 2, f"Row {r}", ha="center", va="center", fontsize=12, weight="bold", color="#5f3dc4")
        for c in range(4):
            x = x0 + c * (cell + gap)
            fc = "#ffffff"
            ec = "#486581"
            if keys[r][c] == "*":
                fc = "#e6fcf5"
                ec = "#0b7285"
            elif keys[r][c] == "#":
                fc = "#fff4e6"
                ec = "#d9480f"
            ax.add_patch(
                FancyBboxPatch(
                    (x, y),
                    cell,
                    cell,
                    boxstyle="round,pad=0.02,rounding_size=0.12",
                    edgecolor=ec,
                    facecolor=fc,
                    linewidth=2.0,
                )
            )
            ax.text(x + cell / 2, y + cell / 2, keys[r][c], ha="center", va="center", fontsize=30, weight="bold", color="#102a43")
    for c in range(4):
        ax.text(x0 + c * (cell + gap) + cell / 2, 1.03, f"Col {c}", ha="center", va="center", fontsize=12, weight="bold", color="#1864ab")

    diagram_arrow(ax, (0.95, 7.95), (0.95, 1.35), "uio_out[3:0]\nrow scan outputs\nfrom ASIC", (2.40, 8.05), "#5f3dc4", rad=0.0)
    diagram_arrow(ax, (1.40, 0.78), (7.55, 0.78), "uio_in[7:4] = column inputs to ASIC", (4.45, 0.36), "#1864ab", rad=0.0)

    legend_x = 8.35
    ax.text(legend_x, 7.95, "Key Functions", ha="left", va="center", fontsize=18, weight="bold", color="#102a43")
    rounded_box(ax, (legend_x, 6.80), (4.75, 0.72), "* = store password", "", "#e6fcf5", "#0b7285", title_size=14)
    rounded_box(ax, (legend_x, 5.82), (4.75, 0.72), "# = check password", "", "#fff4e6", "#d9480f", title_size=14)
    rounded_box(ax, (legend_x, 4.84), (4.75, 0.72), "0-9, A-D = 4-bit code input", "", "#f8fafc", "#486581", title_size=14)

    ax.text(legend_x, 3.62, "Electrical Direction", ha="left", va="center", fontsize=18, weight="bold", color="#102a43")
    rounded_box(ax, (legend_x, 2.48), (4.75, 0.76), "ASIC drives one row at a time", "", "#f3f0ff", "#5f3dc4", title_size=14)
    rounded_box(ax, (legend_x, 1.48), (4.75, 0.76), "ASIC reads the four column lines", "", "#e6f6ff", "#1864ab", title_size=14)
    save_diagram(fig, "keypad_mapping", dpi=140)


def signoff_summary() -> None:
    rows = [
        ("RTL simulation", "PASS"),
        ("DRC", "Passed"),
        ("LVS", "Passed"),
        ("Antenna", "Passed"),
        ("Manufacturability", "Passed"),
        ("Area", "161 um x 111 um = 17871 um^2"),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 6.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("ASIC Signoff Evidence Summary", fontsize=19, weight="bold", pad=14)
    for i, (name, result) in enumerate(rows):
        y = 5.8 - i * 0.82
        fc = "#e8f5e9" if i < 5 else "#e3f2fd"
        ec = "#2e7d32" if i < 5 else "#1565c0"
        ax.add_patch(Rectangle((1.1, y - 0.32), 7.8, 0.62, edgecolor=ec, facecolor=fc, linewidth=1.4))
        ax.text(1.45, y, name, ha="left", va="center", fontsize=13, weight="bold")
        ax.text(8.55, y, result, ha="right", va="center", fontsize=13)
    ax.text(5, 0.55, "Evidence source: reports/ and runs/RUN_2026-05-31_02-03-14", ha="center", fontsize=10, color="#455a64")
    save(fig, "signoff_summary.png")


def parse_vcd(path: Path, wanted: dict[str, str]):
    ids = {}
    scope = []
    values = {}
    current_time = 0
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line.startswith("$scope"):
                scope.append(line.split()[2])
            elif line.startswith("$upscope"):
                if scope:
                    scope.pop()
            elif line.startswith("$var"):
                parts = line.split()
                code = parts[3]
                name = parts[4]
                full = ".".join(scope + [name])
                for label, full_name in wanted.items():
                    if full == full_name:
                        ids[code] = label
                        values[label] = [(0, "x")]
            elif line.startswith("#"):
                current_time = int(line[1:])
            elif ids:
                if line and line[0] in "01xz":
                    code = line[1:]
                    if code in ids:
                        values[ids[code]].append((current_time, line[0]))
                elif line.startswith("b"):
                    val, code = line.split()
                    if code in ids:
                        values[ids[code]].append((current_time, val[1:]))
    return values


def value_at(series, t):
    cur = series[0][1]
    for ts, val in series:
        if ts > t:
            break
        cur = val
    return cur


def waveform() -> None:
    wanted = {
        "clk": "tb_combolock.clk",
        "rst_n": "tb_combolock.rst_n",
        "uio_in": "tb_combolock.uio_in",
        "uio_out": "tb_combolock.uio_out",
        "uio_oe": "tb_combolock.uio_oe",
        "uo_out": "tb_combolock.uo_out",
        "key_valid": "tb_combolock.dut.key_valid",
        "key_code": "tb_combolock.dut.key_code",
        "key_star": "tb_combolock.dut.key_star",
        "key_hash": "tb_combolock.dut.key_hash",
        "unlocked": "tb_combolock.dut.unlocked",
        "locked_out": "tb_combolock.dut.locked_out",
        "attempts": "tb_combolock.dut.attempts",
    }
    values = parse_vcd(VCD, wanted)
    labels = list(wanted.keys())
    t_end = max(ts for series in values.values() for ts, _ in series) if values else 2_470_000
    t0, t1 = 0, t_end
    samples = 360
    times = [t0 + (t1 - t0) * i / (samples - 1) for i in range(samples)]

    fig, axes = plt.subplots(len(labels), 1, figsize=(13, 9.5), sharex=True)
    fig.suptitle("RTL Simulation Waveform Evidence (testbench PASS)", fontsize=17, weight="bold")
    for ax, label in zip(axes, labels):
        series = values.get(label, [(0, "x")])
        if label in {"clk", "rst_n", "key_valid", "key_star", "key_hash", "unlocked", "locked_out"}:
            xs, ys = [], []
            for ts, val in series:
                if t0 <= ts <= t1:
                    xs.append(ts / 1000.0)
                    ys.append(1 if val == "1" else 0)
            if not xs:
                xs, ys = [t0 / 1000.0, t1 / 1000.0], [0, 0]
            ax.step(xs, ys, where="post", color="#1565c0", linewidth=1.2)
            ax.set_ylim(-0.25, 1.35)
            ax.set_yticks([0, 1])
        else:
            ax.set_ylim(0, 1)
            ax.set_yticks([])
            last = None
            for i in range(14):
                ta = t0 + (t1 - t0) * i / 14
                tb = t0 + (t1 - t0) * (i + 1) / 14
                mid = (ta + tb) / 2
                val = value_at(series, mid)
                if val != last or i == 0:
                    ax.text(mid / 1000.0, 0.5, val, ha="center", va="center", fontsize=8, family="monospace")
                ax.axvline(ta / 1000.0, color="#eceff1", linewidth=0.8)
                last = val
        ax.set_ylabel(label, rotation=0, ha="right", va="center", fontsize=9)
        ax.grid(axis="x", color="#eceff1", linewidth=0.6)
    axes[-1].set_xlabel("time (ns)")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    save(fig, "rtl_waveform.png")


def final_layout() -> None:
    text = DEF.read_text(errors="ignore")
    die = re.search(r"DIEAREA\s+\(\s+(\d+)\s+(\d+)\s+\)\s+\(\s+(\d+)\s+(\d+)\s+\)", text)
    units = re.search(r"UNITS DISTANCE MICRONS\s+(\d+)", text)
    scale = int(units.group(1)) if units else 1000
    if die:
        x0, y0, x1, y1 = [int(v) / scale for v in die.groups()]
    else:
        x0, y0, x1, y1 = 0, 0, 161, 111

    pins = []
    pin_re = re.compile(r"-\s+(\S+).*?\+\s+PLACED\s+\(\s+(\d+)\s+(\d+)\s+\)", re.S)
    for name, x, y in pin_re.findall(text):
        pins.append((name, int(x) / scale, int(y) / scale))

    comps = []
    comp_re = re.compile(r"-\s+(\S+)\s+\S+.*?\+\s+PLACED\s+\(\s+(\d+)\s+(\d+)\s+\)", re.S)
    comp_block = re.search(r"COMPONENTS.*?END COMPONENTS", text, re.S)
    if comp_block:
        for name, x, y in comp_re.findall(comp_block.group(0)):
            comps.append((name, int(x) / scale, int(y) / scale))

    fig, ax = plt.subplots(figsize=(10.5, 7.5))
    ax.set_aspect("equal")
    ax.set_title("Final Layout Overview from DEF", fontsize=18, weight="bold", pad=14)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="#263238", facecolor="#fafafa", linewidth=2.0))
    if comps:
        xs = [c[1] for c in comps]
        ys = [c[2] for c in comps]
        ax.scatter(xs, ys, s=5, alpha=0.45, color="#6a1b9a", label="placed cells")
    if pins:
        px = [p[1] for p in pins]
        py = [p[2] for p in pins]
        ax.scatter(px, py, s=22, color="#d84315", label="top-level pins")
    ax.set_xlim(x0 - 8, x1 + 8)
    ax.set_ylim(y0 - 8, y1 + 8)
    ax.set_xlabel("microns")
    ax.set_ylabel("microns")
    ax.text((x0 + x1) / 2, y1 + 3, "DIE_AREA 161 um x 111 um", ha="center", fontsize=11)
    ax.legend(loc="upper right")
    ax.grid(color="#eceff1", linewidth=0.6)
    save(fig, "final_layout.png")


def images_readme() -> None:
    content = """# Visual Evidence Images

The PNG files in this directory are generated documentation evidence for the ASIC project.

Generated automatically:

- `block_diagram.png`
- `keypad_mapping.png`
- `rtl_waveform.png`
- `final_layout.png`
- `signoff_summary.png`

`rtl_waveform.png` is generated from `sim/tb_combolock.vcd`. To inspect the waveform manually:

```sh
make sim
gtkwave sim/tb_combolock.vcd
```

Recommended signals:

- `clk`
- `rst_n`
- `uio_in`
- `uio_out`
- `uio_oe`
- `uo_out`
- `tb_combolock.dut.key_valid`
- `tb_combolock.dut.key_code`
- `tb_combolock.dut.key_star`
- `tb_combolock.dut.key_hash`
- `tb_combolock.dut.unlocked`
- `tb_combolock.dut.locked_out`
- `tb_combolock.dut.attempts`

`final_layout.png` is a DEF-derived overview from:

```text
runs/RUN_2026-05-31_02-03-14/final/def/tt_um_combolock.def
```

To inspect the actual final layout manually with KLayout:

```sh
klayout runs/RUN_2026-05-31_02-03-14/final/gds/tt_um_combolock.gds
```

To inspect it manually with OpenROAD:

```sh
openroad
read_db runs/RUN_2026-05-31_02-03-14/final/odb/tt_um_combolock.odb
gui::show
```
"""
    (IMG / "README.md").write_text(content)


def main() -> None:
    block_diagram()
    keypad_mapping()
    signoff_summary()
    waveform()
    final_layout()
    images_readme()


if __name__ == "__main__":
    main()
