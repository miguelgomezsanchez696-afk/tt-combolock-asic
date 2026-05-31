# 4-bit Combination Lock ASIC with 4x4 Matrix Keypad

This repository contains a TinyTapeout-style digital ASIC project for a 4-bit combination lock. The design accepts one 4-bit code at a time, stores that code as the password, compares later entries against the stored password, and reports unlock or lockout status on output pins.

The user input method is a typical Arduino-style 4x4 matrix keypad connected to the `uio` pins instead of DIP switches.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `src/tt_um_combolock.v` | Top-level TinyTapeout-style Verilog module. |
| `src/keypad_scanner.v` | Synthesizable 4x4 matrix keypad scanner. |
| `test/tb_combolock.v` | RTL simulation testbench. |
| `test/cocotb/` | Cocotb verification testbench for the keypad lock flow. |
| `sim/` | Generated simulation output files. |
| `docs/` | Course-flow, user, pinout, verification, layout, timing, and manufacturing documentation. |
| `reports/` | Recorded RTL and physical-flow evidence. |
| `config.json` | LibreLane configuration. |
| `pin_order.cfg` | Explicit top-level pin placement order for LibreLane. |
| `Makefile` | Convenience targets for simulation, physical flow, report export, and cleanup. |
| `info.yaml` | TinyTapeout-style project metadata and pinout. |

## Hardware Overview

The top module is `tt_um_combolock`. It uses the standard TinyTapeout-style ports: dedicated inputs `ui_in`, dedicated outputs `uo_out`, bidirectional pins `uio`, clock `clk`, reset `rst_n`, and enable `ena`.

The keypad is scanned through the `uio` pins:

- `uio[3:0]` are active-low row outputs driven by the ASIC.
- `uio[7:4]` are active-low column inputs read by the ASIC.
- The keypad columns should be pulled up externally.

Keys `0` through `9` and `A` through `D` load the current entered 4-bit code. `*` stores the current code as the password. `#` checks the current code against the stored password.

## Quick Simulation

Run the RTL simulation with:

```sh
make sim
```

Expected result:

```text
PASS
```

Run the Cocotb verification with:

```sh
make cocotb
```

The Cocotb test uses the same RTL and models keypad presses by reading
`uio_out[3:0]` row scan outputs and driving `uio_in[7:4]` column inputs.

## Physical Flow Evidence

The design has completed RTL-to-GDS hardening with LibreLane. Recorded evidence is kept under `reports/` and the latest complete signoff run is:

```text
runs/RUN_2026-05-31_02-03-14
```

The newest timestamped run directory, `runs/RUN_2026-05-31_02-17-38`, is incomplete and has no `final/` directory, so it is not the signoff evidence source.

The latest complete recorded flow passed:

| Check | Result |
| --- | --- |
| DRC | Passed |
| LVS | Passed |
| Antenna | Passed |
| Manufacturability | Passed |

The design uses `DIE_AREA = 0 0 161 111`, corresponding to 161 um x 111 um and 17871 um^2.

## Documentation

- [ASIC design flow](docs/design_flow.md)
- [User manual](docs/user_manual.md)
- [Pinout](docs/pinout.md)
- [Verification](docs/verification.md)
- [Cocotb verification](docs/cocotb_verification.md)
- [Manufacturing readiness](docs/manufacturing_readiness.md)
- [Synthesis and timing evidence](docs/synthesis_timing.md)
- [Layout stages](docs/layout_stages.md)
- [Flow summary](reports/flow_summary.md)
- [Flow signoff summary](reports/flow_signoff_summary.txt)

## Visual Evidence

- [Block diagram](docs/images/block_diagram.png)
- [Keypad mapping](docs/images/keypad_mapping.png)
- [RTL waveform](docs/images/rtl_waveform.png)
- [Final layout overview](docs/images/final_layout.png)
- [Signoff summary](docs/images/signoff_summary.png)
- [Manual waveform and layout inspection commands](docs/images/README.md)

## Course Tutorial Coverage

| Course topic | Repository evidence |
| --- | --- |
| Verilog tutorial | `src/tt_um_combolock.v`, `src/keypad_scanner.v`, `docs/design_flow.md` |
| Makefile tutorial | `Makefile` with `sim`, `flow`, `reports`, and `clean` targets |
| Cocotb tutorial | `test/cocotb/test_combolock.py`, `test/cocotb/Makefile`, `docs/cocotb_verification.md` |
| TCL tutorial | LibreLane/OpenROAD commands are recorded in `runs/RUN_2026-05-31_02-03-14/*/COMMANDS` |
| FPGA synthesis tutorial | Project is ASIC-focused; synthesis evidence is Yosys/LibreLane in `docs/synthesis_timing.md` |
| Standard cell simulation | Gate-level netlist and SDF files are in `runs/RUN_2026-05-31_02-03-14/final/` |
| Yosys tutorial | `runs/RUN_2026-05-31_02-03-14/06-yosys-synthesis/` |
| OpenSTA | `docs/synthesis_timing.md` and `runs/RUN_2026-05-31_02-03-14/56-openroad-stapostpnr/` |
| LibreLane | `config.json`, `reports/flow_summary.md`, `reports/flow.log` |
| Floorplanning | `docs/layout_stages.md` |
| Placement | `docs/layout_stages.md` |
| CTS | `docs/layout_stages.md` |
| Routing | `docs/layout_stages.md` |
| DRC/LVS | `reports/drc_violations.magic.rpt`, `reports/drc_violations.klayout.json`, `reports/lvs.netgen.rpt` |

## GitHub Actions

GitHub Actions is configured in `.github/workflows/test.yml`. On push, pull request, or manual dispatch, it installs Icarus Verilog and runs `make sim`.
