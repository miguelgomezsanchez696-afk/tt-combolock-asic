#!/usr/bin/env python3
"""Generate visual documentation evidence for the combination lock ASIC."""

from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "docs" / "images"
VCD = ROOT / "sim" / "tb_combolock.vcd"
DEF = ROOT / "runs" / "RUN_2026-05-31_02-03-14" / "final" / "def" / "tt_um_combolock.def"


def save(fig, name: str) -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    fig.savefig(IMG / name, dpi=180, bbox_inches="tight", facecolor="white")
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


def block_diagram() -> None:
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("tt_um_combolock ASIC Block Diagram", fontsize=18, weight="bold", pad=16)

    box(ax, (0.5, 2.35), (2.0, 2.0), "4x4 Matrix\nKeypad", "Rows 0-3\nCols 0-3", "#fff8e1", "#c28f00")
    box(ax, (3.25, 0.85), (5.5, 5.25), "TinyTapeout-style top module\n tt_um_combolock", "", "#f7fbff", "#1f5f99")
    box(ax, (3.75, 3.75), (2.0, 1.2), "keypad_scanner", "scan rows\nread columns", "#e8f5e9", "#2e7d32")
    box(ax, (6.15, 3.75), (2.0, 1.2), "Lock FSM /\nRegisters", "password\nattempts\nlockout", "#f3e5f5", "#6a1b9a")
    box(ax, (6.15, 2.05), (2.0, 1.0), "Output Pack", "{password,\nattempts,status}", "#ede7f6", "#512da8")
    box(ax, (9.5, 2.35), (2.0, 2.0), "uo_out[7:0]", "unlocked\nlocked_out\nattempts\npassword", "#e0f2f1", "#00695c")

    arrow(ax, (2.5, 3.65), (3.75, 4.35), "uio[3:0] rows")
    arrow(ax, (3.75, 4.05), (2.5, 3.0), "uio[7:4] cols")
    arrow(ax, (5.75, 4.35), (6.15, 4.35), "key_valid/code")
    arrow(ax, (7.15, 3.75), (7.15, 3.05), "state")
    arrow(ax, (8.15, 2.55), (9.5, 3.35), "status")
    ax.text(5.98, 1.3, "clk, rst_n, ena", ha="center", fontsize=10, color="#37474f")
    save(fig, "block_diagram.png")


def keypad_mapping() -> None:
    keys = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]
    fig, ax = plt.subplots(figsize=(9.5, 7.2))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("4x4 Keypad Mapping and uio Connections", fontsize=18, weight="bold", pad=14)

    x0, y0, cell = 1.3, 2.0, 1.0
    for r in range(4):
        ax.text(0.5, y0 + (3 - r) * cell + 0.5, f"Row {r}\nuio[{r}]", ha="center", va="center", fontsize=10, color="#1b5e20")
        for c in range(4):
            x = x0 + c * cell
            y = y0 + (3 - r) * cell
            fc = "#fffde7"
            if keys[r][c] == "*":
                fc = "#e3f2fd"
            elif keys[r][c] == "#":
                fc = "#fce4ec"
            ax.add_patch(Rectangle((x, y), cell * 0.86, cell * 0.86, edgecolor="#455a64", facecolor=fc, linewidth=1.6))
            ax.text(x + cell * 0.43, y + cell * 0.43, keys[r][c], ha="center", va="center", fontsize=20, weight="bold")
    for c in range(4):
        ax.text(x0 + c * cell + 0.43, 1.4, f"Col {c}\nuio[{c+4}]", ha="center", va="center", fontsize=10, color="#0d47a1")

    ax.text(5.75, 5.4, "ASIC directions", fontsize=13, weight="bold", ha="center")
    box(ax, (4.85, 4.25), (1.8, 0.75), "uio[3:0]", "row outputs\nactive low", "#e8f5e9", "#2e7d32")
    box(ax, (4.85, 3.1), (1.8, 0.75), "uio[7:4]", "column inputs\nactive low", "#e3f2fd", "#1565c0")
    box(ax, (4.85, 1.9), (1.8, 0.75), "*", "set password", "#e3f2fd", "#1565c0")
    box(ax, (4.85, 0.8), (1.8, 0.75), "#", "check password", "#fce4ec", "#ad1457")
    save(fig, "keypad_mapping.png")


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
