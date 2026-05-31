# Synthesis and Timing Evidence

This document summarizes synthesis and timing evidence exported from the completed local LibreLane run. LibreLane was not rerun for this documentation polish pass.

The `runs/` directory is ignored and not committed. The local run tag `RUN_2026-05-31_02-03-14` is recorded only for traceability; GitHub review should use committed evidence under `reports/` and the final GDS under `docs/gds/`.

## Committed Evidence

| Evidence | Purpose |
| --- | --- |
| [../reports/flow_summary.md](../reports/flow_summary.md) | Human-readable flow result summary. |
| [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt) | Signoff lines showing routing DRC, Magic DRC, KLayout DRC, LVS, setup, hold, max cap, and flow completion. |
| [../reports/final_metrics.json](../reports/final_metrics.json) | Exported final metrics from LibreLane. |
| [../reports/flow.log](../reports/flow.log) | Full exported flow log from the local signoff run. |

## Synthesis Evidence

LibreLane runs Yosys synthesis from the Verilog sources listed in `config.json`:

| Setting | Value |
| --- | --- |
| `DESIGN_NAME` | `tt_um_combolock` |
| `VERILOG_FILES` | `src/tt_um_combolock.v`, `src/keypad_scanner.v` |
| `CLOCK_PORT` | `clk` |
| `CLOCK_PERIOD` | `25` ns |

The synthesis report showed:

| Metric | Value |
| --- | ---: |
| Wires | 90 |
| Wire bits | 125 |
| Ports | 8 |
| Port bits | 43 |
| Memories | 0 |
| Processes after synthesis | 0 |
| Mapped cells | 106 |
| Flip-flops | 23 `sky130_fd_sc_hd__dfrtp_2` cells |
| Yosys check problems | 0 |
| Synthesized module area | 1291.238400 um^2 |

The final physical metrics in [../reports/final_metrics.json](../reports/final_metrics.json) show 384 standard-cell instances after physical implementation and 1474 total instances including filler, tap, antenna, and repair cells.

## Timing Evidence

The project uses a 25 ns clock period from `config.json`, corresponding to 40 MHz.

The final post-route timing summary reports no setup or hold timing violations:

| Metric | Final post-route value |
| --- | ---: |
| Worst setup slack | 16.6203 ns |
| Setup TNS | 0.0000 ns |
| Setup violation count | 0 |
| Worst hold slack | 0.1078 ns |
| Hold TNS | 0.0000 ns |
| Hold violation count | 0 |
| Max capacitance violations | 0 |

Per-corner post-route summary:

| Corner | Hold slack | Setup slack | Setup violations | Hold violations |
| --- | ---: | ---: | ---: | ---: |
| `nom_tt_025C_1v80` | 0.3256 ns | 18.2358 ns | 0 | 0 |
| `nom_ss_100C_1v60` | 0.9177 ns | 16.6410 ns | 0 | 0 |
| `nom_ff_n40C_1v95` | 0.1098 ns | 18.7750 ns | 0 | 0 |
| `min_tt_025C_1v80` | 0.3224 ns | 18.2629 ns | 0 | 0 |
| `min_ss_100C_1v60` | 0.9125 ns | 16.6947 ns | 0 | 0 |
| `min_ff_n40C_1v95` | 0.1078 ns | 18.7833 ns | 0 | 0 |
| `max_tt_025C_1v80` | 0.3283 ns | 18.2226 ns | 0 | 0 |
| `max_ss_100C_1v60` | 0.9222 ns | 16.6203 ns | 0 | 0 |
| `max_ff_n40C_1v95` | 0.1117 ns | 18.7660 ns | 0 | 0 |

[../reports/final_metrics.json](../reports/final_metrics.json) also records `timing__setup_vio__count = 0`, `timing__hold_vio__count = 0`, `timing__setup__tns = 0`, and `timing__hold__tns = 0`.

## Electrical Timing Notes

The final metrics include nonzero design-rule timing metrics for maximum slew and maximum fanout:

| Metric | Value |
| --- | ---: |
| `design__max_slew_violation__count` | 48 |
| `design__max_fanout_violation__count` | 6 |
| `design__max_cap_violation__count` | 0 |

The flow completed and the final manufacturability report passed DRC, LVS, and antenna. If the course requires all STA electrical design-rule checks to be zero, these max-slew and fanout metrics should be reviewed separately from setup and hold timing closure.

## Physical Flow Context

Yosys, OpenSTA, placement, CTS, routing, extraction, and signoff are all part of the LibreLane run summarized in [design_flow.md](design_flow.md). The exported reports are sufficient for repository review without committing the ignored local run tree.
