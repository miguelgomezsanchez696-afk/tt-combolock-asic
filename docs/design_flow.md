# ASIC Design Flow

This project follows the course ASIC flow from RTL design through physical verification. The implemented design is a 4-bit combination lock with a 4x4 matrix keypad interface.

## 1. RTL Design

The synthesizable Verilog is in `src/`:

| File | Purpose |
| --- | --- |
| `src/tt_um_combolock.v` | Top-level TinyTapeout-style user module and lock state machine. |
| `src/keypad_scanner.v` | 4x4 active-low matrix keypad scanner. |

The top module is `tt_um_combolock`. It uses `clk`, active-low reset `rst_n`, enable `ena`, dedicated inputs `ui_in`, dedicated outputs `uo_out`, and bidirectional `uio` signals. The RTL maps the keypad to `uio[3:0]` row outputs and `uio[7:4]` column inputs.

## 2. RTL Verification

RTL simulation is performed with Icarus Verilog using `test/tb_combolock.v`.

```sh
make sim
```

The expected result is:

```text
PASS
```

The testbench verifies reset behavior, keypad scanning, password setting with `*`, password checking with `#`, unlock behavior, failed-attempt counting, lockout after three failed attempts, and `uio_oe = 8'b0000_1111`.

## 3. Synthesis

LibreLane runs Yosys synthesis using `config.json`.

| Setting | Value |
| --- | --- |
| `DESIGN_NAME` | `tt_um_combolock` |
| `VERILOG_FILES` | `src/tt_um_combolock.v`, `src/keypad_scanner.v` |
| `CLOCK_PORT` | `clk` |
| `CLOCK_PERIOD` | `25` ns |

Synthesis evidence is available in:

```text
runs/RUN_2026-05-31_02-03-14/06-yosys-synthesis/
```

The Yosys reports show 0 synthesis check errors, no inferred latches, no unmapped cells, and a mapped standard-cell netlist.

## 4. Floorplanning

The physical configuration uses absolute sizing:

```json
"DIE_AREA": "0 0 161 111"
```

This gives a 161 um x 111 um die area. The core area reported by LibreLane is `5.52 10.88 155.48 97.92`.

Top-level pin placement is fixed by:

```json
"IO_PIN_ORDER_CFG": "dir::pin_order.cfg"
```

The floorplan stage is recorded at:

```text
runs/RUN_2026-05-31_02-03-14/13-openroad-floorplan/
```

## 5. Placement

LibreLane performs global placement, custom IO placement from `pin_order.cfg`, detailed placement, and timing repair.

| Stage | Directory |
| --- | --- |
| IO/custom pin placement | `26-odb-customioplacement` |
| Global placement | `28-openroad-globalplacement` |
| Detailed placement | `34-openroad-detailedplacement` |

The final metrics report 384 standard-cell instances and 1474 total instances including filler, tap, antenna, and repair cells.

## 6. Clock Tree Synthesis

CTS is performed by OpenROAD in:

```text
runs/RUN_2026-05-31_02-03-14/35-openroad-cts/
```

The final metrics report 4 clock buffer instances. Post-CTS and post-route STA are recorded in later OpenROAD STA stages.

## 7. Routing

Routing is performed in two main steps:

| Routing step | Directory |
| --- | --- |
| Global routing | `39-openroad-globalrouting` |
| Detailed routing | `45-openroad-detailedrouting` |

The final metrics show route DRC convergence to 0 route DRC errors and final route wirelength of 3201 um with 1007 vias.

## 8. DRC

Final DRC is checked with Magic and KLayout.

| Check | Evidence |
| --- | --- |
| Magic DRC | `reports/drc_violations.magic.rpt` |
| KLayout DRC | `reports/drc_violations.klayout.json` |

The recorded flow summary reports 0 Magic DRC errors and 0 KLayout DRC errors.

## 9. LVS

LVS is run with Netgen after Magic extraction.

Evidence:

```text
reports/lvs.netgen.rpt
runs/RUN_2026-05-31_02-03-14/70-netgen-lvs/reports/lvs.netgen.rpt
```

The recorded flow summary reports 0 LVS errors.

## 10. Antenna

Antenna checks and repair are included in the route/signoff flow. The configuration enables heuristic diode insertion:

```json
"RUN_HEURISTIC_DIODE_INSERTION": true
```

Evidence:

```text
reports/antenna.rpt
```

The recorded flow summary reports 0 antenna violating nets.

## 11. Manufacturability

LibreLane generated the final manufacturability report:

```text
reports/manufacturability.rpt
runs/RUN_2026-05-31_02-03-14/76-misc-reportmanufacturability/manufacturability.rpt
```

The report records:

| Check | Result |
| --- | --- |
| Antenna | Passed |
| LVS | Passed |
| DRC | Passed |

## Run Note

The newest timestamped run directory in this repository is `runs/RUN_2026-05-31_02-17-38`, but that run stops at `32-openroad-repairdesignpostgpl` and does not contain a `final/` directory. The latest complete signoff evidence is therefore the completed `runs/RUN_2026-05-31_02-03-14` run and the exported `reports/` files.
