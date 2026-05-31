# ASIC Design Flow

This project follows the course digital ASIC flow from Verilog RTL through final physical verification. The design is a 4-bit combination lock whose main interface change is a 4x4 matrix keypad on `uio` pins instead of DIP switches.

## Course Flow Mapping

| Course topic | Project implementation |
| --- | --- |
| Verilog | Synthesizable RTL in `src/tt_um_combolock.v` and `src/keypad_scanner.v`. |
| Makefile | Top-level `Makefile` provides `sim`, `cocotb`, `flow`, `reports`, and `clean` targets. |
| Cocotb | `test/cocotb/test_combolock.py` verifies the keypad-driven lock behavior. |
| Yosys | LibreLane uses Yosys for synthesis from the Verilog sources listed in `config.json`. |
| OpenSTA | LibreLane/OpenROAD performs timing analysis; timing evidence is summarized in `docs/synthesis_timing.md`. |
| LibreLane | `config.json` defines the RTL-to-GDS flow for `tt_um_combolock`. |
| Floorplanning | Die area, core area, and pin ordering are configured through `config.json` and `pin_order.cfg`. |
| Placement | LibreLane/OpenROAD places standard cells after synthesis and floorplanning. |
| CTS | OpenROAD builds the clock tree for the `clk` domain. |
| Routing | LibreLane performs global and detailed routing before final signoff. |
| DRC/LVS | Magic, KLayout, and Netgen reports are exported under `reports/`. |

## 1. Verilog RTL

The synthesizable RTL is in `src/`:

| File | Purpose |
| --- | --- |
| `src/tt_um_combolock.v` | Top-level TinyTapeout-style user module and lock state machine. |
| `src/keypad_scanner.v` | 4x4 active-low matrix keypad scanner. |

The top module uses `clk`, active-low reset `rst_n`, enable `ena`, dedicated inputs `ui_in`, dedicated outputs `uo_out`, and bidirectional `uio` signals. The keypad rows are driven on `uio[3:0]`; keypad columns are read on `uio[7:4]`.

## 2. Makefile and RTL Simulation

The top-level `Makefile` wraps the Verilog simulator command:

```sh
make sim
```

Expected result:

```text
PASS
```

The RTL testbench verifies reset behavior, keypad scanning, password setting with `*`, password checking with `#`, unlock behavior, failed-attempt counting, lockout after three failed attempts, and `uio_oe = 8'b0000_1111`.

## 3. Cocotb Verification

Cocotb is run with:

```sh
pip install -r requirements.txt
make cocotb
```

The Cocotb test compiles the same RTL and drives a behavioral keypad model by observing row scan outputs and driving column inputs. This covers the course Cocotb workflow while keeping the RTL source unchanged.

## 4. Yosys Synthesis

LibreLane runs Yosys synthesis using `config.json`.

| Setting | Value |
| --- | --- |
| `DESIGN_NAME` | `tt_um_combolock` |
| `VERILOG_FILES` | `src/tt_um_combolock.v`, `src/keypad_scanner.v` |
| `CLOCK_PORT` | `clk` |
| `CLOCK_PERIOD` | `25` ns |

Synthesis and timing notes are summarized in [synthesis_timing.md](synthesis_timing.md). Exported flow metrics are committed under [../reports/](../reports/).

## 5. OpenSTA Timing

LibreLane/OpenROAD runs static timing analysis after implementation stages. The recorded signoff summary reports no setup violations and no hold violations. See:

- [synthesis_timing.md](synthesis_timing.md)
- [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt)
- [../reports/final_metrics.json](../reports/final_metrics.json)

## 6. LibreLane RTL-to-GDS Flow

The local physical implementation command is:

```sh
make flow
```

This expands to:

```sh
librelane config.json
```

The complete signoff run was performed locally. The `runs/` directory is intentionally ignored and not committed, so GitHub review should use committed artifacts under `reports/` and the final GDS under `docs/gds/`. The local run tag `RUN_2026-05-31_02-03-14` is recorded only for traceability.

## 7. Floorplanning

The physical configuration uses an explicit die area:

```json
"DIE_AREA": "0 0 161 111"
```

This gives a 161 um x 111 um die area. Pin placement is controlled by:

```json
"IO_PIN_ORDER_CFG": "dir::pin_order.cfg"
```

The pin order file keeps the TinyTapeout-style interface and keypad pins explicit for review.

## 8. Placement

LibreLane/OpenROAD performs global placement, IO placement from `pin_order.cfg`, detailed placement, and placement-stage timing repair. Final exported metrics report 384 standard-cell instances and 1474 total instances including filler, tap, antenna, and repair cells.

Relevant committed evidence:

- [../reports/final_metrics.json](../reports/final_metrics.json)
- [layout_stages.md](layout_stages.md)

## 9. CTS

Clock Tree Synthesis is performed by OpenROAD for the `clk` domain. Final exported metrics report 4 clock buffer instances. Timing closure is summarized in:

- [synthesis_timing.md](synthesis_timing.md)
- [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt)

## 10. Routing

LibreLane performs global routing and detailed routing before final signoff. The final metrics report route DRC convergence to 0 route DRC errors, final route wirelength of 3201 um, and 1007 vias.

Routing and layout-stage notes are summarized in [layout_stages.md](layout_stages.md).

## 11. DRC and LVS

Final DRC is checked with Magic and KLayout. LVS is checked with Netgen after layout extraction.

| Check | Committed evidence |
| --- | --- |
| Magic DRC | [../reports/drc_violations.magic.rpt](../reports/drc_violations.magic.rpt) |
| KLayout DRC | [../reports/drc_violations.klayout.json](../reports/drc_violations.klayout.json) |
| Netgen LVS | [../reports/lvs.netgen.rpt](../reports/lvs.netgen.rpt) |

The recorded flow summary reports 0 Magic DRC errors, 0 KLayout DRC errors, and 0 LVS errors.

## 12. Antenna and Manufacturability

Antenna checking and repair are included in the routing and signoff flow. The configuration enables heuristic diode insertion:

```json
"RUN_HEURISTIC_DIODE_INSERTION": true
```

Committed evidence:

- [../reports/antenna.rpt](../reports/antenna.rpt)
- [../reports/manufacturability.rpt](../reports/manufacturability.rpt)
- [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt)

The manufacturability report records antenna, LVS, and DRC as passed.

## 13. Final GDS

The final GDS is committed for visual inspection:

- [gds/tt_um_combolock.gds](gds/tt_um_combolock.gds)

Viewer instructions are in [gds/README.md](gds/README.md).
