# 4-bit Combination Lock ASIC with 4x4 Matrix Keypad

This repository contains a TinyTapeout-style digital ASIC project for a 4-bit combination lock. The design accepts one 4-bit code at a time, can store that code as the password, compares later entries against the stored password, and reports unlock or lockout status on output pins.

The functional change from the original base Combination Lock is the user input method: this version uses a typical Arduino-style 4x4 matrix keypad instead of DIP switches.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `src/tt_um_combolock.v` | Top-level TinyTapeout-style Verilog module. |
| `src/keypad_scanner.v` | Synthesizable 4x4 matrix keypad scanner. |
| `test/tb_combolock.v` | RTL simulation testbench. |
| `sim/` | Generated simulation output files. |
| `docs/` | User, pinout, verification, and manufacturing documentation. |
| `reports/` | Recorded RTL and physical-flow evidence. |
| `config.json` | LibreLane configuration. |
| `pin_order.cfg` | Explicit top-level pin placement order for LibreLane. |
| `Makefile` | Convenience targets for simulation and physical flow. |
| `info.yaml` | TinyTapeout-style project metadata and pinout. |

## Hardware and User Interface Overview

The top module is `tt_um_combolock`. It uses the standard TinyTapeout-style ports: dedicated inputs `ui_in`, dedicated outputs `uo_out`, bidirectional pins `uio`, clock `clk`, reset `rst_n`, and enable `ena`.

The keypad is scanned through the `uio` pins:

- `uio[3:0]` are active-low row outputs driven by the ASIC.
- `uio[7:4]` are active-low column inputs read by the ASIC.
- The keypad columns should be pulled up externally. A pressed key connects the currently active-low row to one column, so the selected column reads as `0`.

The lock stores a 4-bit password. Numeric keys and `A` through `D` load the current entered code. `*` stores the current entered code as the password. `#` checks the current entered code against the stored password.

## Pinout

| Port | Direction | Meaning |
| --- | --- | --- |
| `clk` | Input | System clock. The project metadata uses 40 MHz. |
| `rst_n` | Input | Active-low reset. Clears password, entered code, failed attempts, `unlocked`, and `locked_out`. |
| `ena` | Input | TinyTapeout enable. Lock state updates only when this signal is high. |
| `ui_in[7:0]` | Input | Unused by the RTL; reserved. |
| `uo_out[0]` | Output | `unlocked`. Asserted after a correct `#` check. |
| `uo_out[1]` | Output | `locked_out`. Asserted after three failed checks. |
| `uo_out[3:2]` | Output | Failed-attempt counter. |
| `uo_out[7:4]` | Output | Stored password, exposed for bring-up and demonstration visibility. |
| `uio_in[3:0]` | Input | Unused row-side bidirectional input bits. |
| `uio_in[7:4]` | Input | Keypad column inputs, active low. |
| `uio_out[3:0]` | Output | Keypad row outputs, active low. |
| `uio_out[7:4]` | Output | Driven to `0`; not used as outputs. |
| `uio_oe[7:0]` | Output | Fixed at `8'b0000_1111`, making `uio[3:0]` outputs and `uio[7:4]` inputs. |

## Keypad Connection Table

| Keypad signal | ASIC pin | Direction at ASIC | Behavior |
| --- | --- | --- | --- |
| Row 0 | `uio[0]` | Output | Active-low scan row. |
| Row 1 | `uio[1]` | Output | Active-low scan row. |
| Row 2 | `uio[2]` | Output | Active-low scan row. |
| Row 3 | `uio[3]` | Output | Active-low scan row. |
| Column 0 | `uio[4]` | Input | Active-low column input with external pull-up. |
| Column 1 | `uio[5]` | Input | Active-low column input with external pull-up. |
| Column 2 | `uio[6]` | Input | Active-low column input with external pull-up. |
| Column 3 | `uio[7]` | Input | Active-low column input with external pull-up. |

Key layout:

| Row | Col 0 | Col 1 | Col 2 | Col 3 |
| --- | --- | --- | --- | --- |
| Row 0 | `1` | `2` | `3` | `A` |
| Row 1 | `4` | `5` | `6` | `B` |
| Row 2 | `7` | `8` | `9` | `C` |
| Row 3 | `*` | `0` | `#` | `D` |

## Key Behavior

| Key | Function |
| --- | --- |
| `0`-`9`, `A`-`D` | Load the 4-bit entered code. |
| `*` | Store the current entered code as the password, unless `locked_out` is already active. |
| `#` | Compare the current entered code against the stored password, unless `locked_out` is already active. |

## Output Behavior

| Output | Behavior |
| --- | --- |
| `unlocked` / `uo_out[0]` | Goes high after a correct password check. Cleared by reset, password update, or wrong check. |
| `locked_out` / `uo_out[1]` | Goes high after three failed checks. Cleared only by reset. |
| `failed_attempts` / `uo_out[3:2]` | Counts failed checks from 0 to 3. Reset to 0 after a correct check or password update. |
| `debug_password` / `uo_out[7:4]` | Shows the stored 4-bit password for bring-up and demo visibility. |

## RTL Simulation

Run the RTL simulation with:

```sh
make sim
```

Equivalent raw commands:

```sh
iverilog -g2012 -o sim/tb_combolock.vvp test/tb_combolock.v src/*.v
vvp sim/tb_combolock.vvp
```

Expected result:

```text
PASS
```

## LibreLane Physical Flow

The design has already completed RTL-to-GDS hardening with LibreLane. To reproduce the flow locally, use:

```sh
make flow
```

Equivalent command:

```sh
librelane config.json
```

If the default PDK path is not writable in the local environment, use:

```sh
export PDK_ROOT=/tmp/librelane-pdks
librelane config.json
```

Do not rerun the physical flow just to review this repository; recorded evidence is kept under `reports/`.

## Physical Verification Results

The latest recorded local flow passed the required signoff-style checks:

| Check | Result |
| --- | --- |
| DRC | Passed |
| LVS | Passed |
| Antenna | Passed |
| Manufacturability | Passed |

The design uses a fixed `DIE_AREA` of `0 0 161 111`, corresponding to 161 um x 111 um and 17871 um^2.

## Reports

The `reports/` directory contains the evidence exported from simulation and the LibreLane run:

- `reports/rtl_simulation_pass.txt`
- `reports/flow_summary.md`
- `reports/flow_signoff_summary.txt`
- `reports/final_metrics.json`
- `reports/drc_violations.magic.rpt`
- `reports/drc_violations.klayout.json`
- `reports/lvs.netgen.rpt`
- `reports/antenna.rpt`
- `reports/manufacturability.rpt`
- `reports/flow.log`

## GitHub Actions Status

GitHub Actions is configured in `.github/workflows/test.yml`. On push, pull request, or manual dispatch, it installs Icarus Verilog and runs:

```sh
make sim
```

The current project context records GitHub Actions as green.

## Manufacturing Readiness Summary

This design is ready for final presentation as a small hardened digital macro:

- RTL simulation passes.
- LibreLane RTL-to-GDS flow completed.
- Top-level pin placement is fixed through `pin_order.cfg` and `IO_PIN_ORDER_CFG`.
- DRC, LVS, antenna, and manufacturability checks passed in the recorded local flow.
- Reports with evidence are included in `reports/`.

## Documentation Links

- [User manual](docs/user_manual.md)
- [Pinout](docs/pinout.md)
- [Verification manual](docs/verification.md)
- [Manufacturing readiness](docs/manufacturing_readiness.md)
- [Flow summary](reports/flow_summary.md)
- [Flow signoff summary](reports/flow_signoff_summary.txt)
