# 4-bit Combination Lock ASIC with Matrix Keypad

This repository contains a TinyTapeout-style digital ASIC project for a 4-bit combination lock. The design lets a user enter a 4-bit value, store it as the password, compare later entries against the stored password, and report unlock or lockout status on output pins.

The main project modification from a simple switch-driven lock is the input interface: this design uses a 4x4 matrix keypad on the bidirectional `uio` pins instead of DIP switches.

## Quick Start

Run the Verilog RTL simulation:

```sh
make sim
```

Expected result:

```text
PASS
```

Run the Cocotb keypad verification:

```sh
pip install -r requirements.txt
make cocotb
```

The physical flow has already been run locally. Do not rerun LibreLane just to review the repository; exported signoff evidence is committed under `reports/`, and the final GDS for viewer inspection is committed at [docs/gds/tt_um_combolock.gds](docs/gds/tt_um_combolock.gds).

## Repository Structure

| Path | Purpose |
| --- | --- |
| `src/` | Synthesizable Verilog RTL for the lock and keypad scanner. |
| `test/tb_combolock.v` | Icarus Verilog RTL testbench. |
| `test/cocotb/` | Cocotb verification for the keypad-driven lock flow. |
| `Makefile` | Local targets for simulation, Cocotb, LibreLane, report export, and cleanup. |
| `config.json` | LibreLane RTL-to-GDS configuration. |
| `pin_order.cfg` | Explicit top-level pin ordering for physical implementation. |
| `reports/` | Committed RTL and physical signoff evidence exported from the local run. |
| `docs/` | Design flow, pinout, verification, layout, timing, and review documentation. |
| `docs/images/` | Block diagram, keypad map, waveform, layout, and signoff screenshots. |
| `docs/gds/tt_um_combolock.gds` | Final GDS file for visual inspection in a GDS viewer. |
| `.github/workflows/test.yml` | GitHub Actions workflow for RTL and Cocotb checks. |

## Pinout Summary

The top module is `tt_um_combolock` and uses the TinyTapeout-style interface: `ui_in`, `uo_out`, `uio_in`, `uio_out`, `uio_oe`, `clk`, `rst_n`, and `ena`.

| Pin group | Direction | Use |
| --- | --- | --- |
| `ui_in[7:0]` | Input | Reserved and currently unused by the RTL. |
| `uo_out[0]` | Output | `unlocked` status. |
| `uo_out[1]` | Output | `locked_out` status after three failed checks. |
| `uo_out[3:2]` | Output | Failed-attempt counter. |
| `uo_out[7:4]` | Output | Stored password debug output for bring-up visibility. |
| `uio[3:0]` | Output | Active-low keypad row scan outputs. |
| `uio[7:4]` | Input | Active-low keypad column inputs with external pull-ups. |

See [docs/pinout.md](docs/pinout.md) for the full pin table and keypad mapping.

## Verification Summary

| Check | Command or evidence | Expected result |
| --- | --- | --- |
| RTL simulation | `make sim` | `PASS` |
| Cocotb verification | `make cocotb` | Cocotb keypad test passes |
| CI automation | `.github/workflows/test.yml` | Runs RTL simulation and Cocotb |
| Physical verification | `reports/` | DRC, LVS, antenna, and manufacturability passed |

The RTL testbench and Cocotb test verify reset behavior, keypad code entry, password storage with `*`, password checking with `#`, unlock behavior, failed-attempt counting, lockout after three wrong attempts, and the `uio_oe` direction mask.

## Physical Signoff Summary

The complete LibreLane signoff run was performed locally. Because `runs/` is intentionally ignored and not committed, local run paths are not used as GitHub evidence. The local run tag `RUN_2026-05-31_02-03-14` is recorded only for traceability.

Review-facing physical evidence is split into committed extracted reports and committed viewer artifacts:

- Extracted signoff evidence is stored in [reports/](reports/).
- The final GDS is stored in [docs/gds/tt_um_combolock.gds](docs/gds/tt_um_combolock.gds).
- Visual evidence is stored in [docs/images/](docs/images/).

Committed evidence:

| Result | Committed evidence |
| --- | --- |
| DRC passed | [reports/drc_violations.magic.rpt](reports/drc_violations.magic.rpt), [reports/drc_violations.klayout.json](reports/drc_violations.klayout.json) |
| LVS passed | [reports/lvs.netgen.rpt](reports/lvs.netgen.rpt) |
| Antenna passed | [reports/antenna.rpt](reports/antenna.rpt) |
| Manufacturability passed | [reports/manufacturability.rpt](reports/manufacturability.rpt), [reports/flow_signoff_summary.txt](reports/flow_signoff_summary.txt) |
| Flow metrics | [reports/final_metrics.json](reports/final_metrics.json), [reports/flow_summary.md](reports/flow_summary.md) |
| Final GDS | [docs/gds/tt_um_combolock.gds](docs/gds/tt_um_combolock.gds) |

## Visual Evidence

| Evidence | Link |
| --- | --- |
| Block diagram | [docs/images/block_diagram.png](docs/images/block_diagram.png) |
| Keypad mapping | [docs/images/keypad_mapping.png](docs/images/keypad_mapping.png) |
| RTL waveform | [docs/images/rtl_waveform_capture.png](docs/images/rtl_waveform_capture.png) |
| KLayout layout view | [docs/images/klayout_view.png](docs/images/klayout_view.png) |
| TinyTapeout GDS Viewer 3D view | [docs/images/tinytapeout_3d_view.png](docs/images/tinytapeout_3d_view.png) |
| Signoff summary | [docs/images/signoff_summary.png](docs/images/signoff_summary.png) |

## Course Tutorial Coverage

| Course topic | Repository evidence |
| --- | --- |
| Verilog | `src/tt_um_combolock.v`, `src/keypad_scanner.v` |
| Makefile | `Makefile` targets for `sim`, `cocotb`, `flow`, `reports`, and `clean` |
| Cocotb | `test/cocotb/test_combolock.py`, `test/cocotb/Makefile` |
| TCL | LibreLane/OpenROAD command history exported in [reports/COMMANDS](reports/COMMANDS) |
| Yosys | Synthesis and metrics evidence in [docs/synthesis_timing.md](docs/synthesis_timing.md) and `reports/` |
| OpenSTA | Timing discussion in [docs/synthesis_timing.md](docs/synthesis_timing.md) |
| LibreLane | [config.json](config.json), [reports/flow_summary.md](reports/flow_summary.md) |
| Floorplanning | [docs/design_flow.md](docs/design_flow.md), [docs/layout_stages.md](docs/layout_stages.md) |
| Placement | [docs/design_flow.md](docs/design_flow.md), [docs/layout_stages.md](docs/layout_stages.md) |
| CTS | [docs/design_flow.md](docs/design_flow.md), [docs/layout_stages.md](docs/layout_stages.md) |
| Routing | [docs/design_flow.md](docs/design_flow.md), [docs/layout_stages.md](docs/layout_stages.md) |
| DRC/LVS | [reports/drc_violations.magic.rpt](reports/drc_violations.magic.rpt), [reports/drc_violations.klayout.json](reports/drc_violations.klayout.json), [reports/lvs.netgen.rpt](reports/lvs.netgen.rpt) |

## Documentation

- [Project review checklist](docs/project_review_checklist.md)
- [User manual](docs/user_manual.md)
- [Pinout](docs/pinout.md)
- [ASIC design flow](docs/design_flow.md)
- [Verification](docs/verification.md)
- [Cocotb verification](docs/cocotb_verification.md)
- [Layout stages](docs/layout_stages.md)
- [Synthesis and timing](docs/synthesis_timing.md)
- [Manufacturing readiness](docs/manufacturing_readiness.md)
- [Final GDS viewer notes](docs/gds/README.md)
