# Synthesis and Timing Evidence

This document summarizes synthesis and timing evidence already present in `reports/` and the completed LibreLane run. LibreLane was not rerun for this documentation.

## Run Directories Checked

| Path | Status |
| --- | --- |
| `runs/RUN_2026-05-31_02-17-38` | Newest timestamped run, but incomplete. It stops at `32-openroad-repairdesignpostgpl` and has no `final/` directory. |
| `runs/RUN_2026-05-31_02-03-14` | Latest complete run with final GDS, metrics, DRC, LVS, antenna, and manufacturability reports. |

The `reports/` directory was exported from the complete `RUN_2026-05-31_02-03-14` run.

## Synthesis Evidence

Yosys synthesis artifacts are stored at:

```text
runs/RUN_2026-05-31_02-03-14/06-yosys-synthesis/
```

Important reports:

| Report | Evidence |
| --- | --- |
| `reports/stat.rpt` | Mapped design statistics and cell list inside the Yosys synthesis step. |
| `reports/chk.rpt` | Yosys design check report inside the Yosys synthesis step. |
| `reports/latch.rpt` | Inferred latch report inside the Yosys synthesis step. |
| `tt_um_combolock.nl.v` | Synthesized gate-level netlist. |

The synthesis report shows:

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

The final physical metrics in `reports/final_metrics.json` show 384 standard-cell instances after physical implementation and 1474 total instances including filler, tap, antenna, and repair cells.

## Timing Evidence

The project uses a 25 ns clock period from `config.json`, corresponding to 40 MHz.

Post-route STA evidence is stored at:

```text
runs/RUN_2026-05-31_02-03-14/56-openroad-stapostpnr/
```

The summary report shows no setup or hold timing violations:

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

`reports/final_metrics.json` also records `timing__setup_vio__count = 0`, `timing__hold_vio__count = 0`, `timing__setup__tns = 0`, and `timing__hold__tns = 0`.

## Electrical Timing Notes

The final metrics include nonzero design-rule timing metrics for maximum slew and maximum fanout:

| Metric | Value |
| --- | ---: |
| `design__max_slew_violation__count` | 48 |
| `design__max_fanout_violation__count` | 6 |
| `design__max_cap_violation__count` | 0 |

The flow still completed and the final manufacturability report passed DRC, LVS, and antenna. If the course requires all STA electrical design-rule checks to be zero, these max-slew and fanout metrics should be reviewed separately from setup and hold timing closure.

## Where LibreLane Stores Timing Files

LibreLane stores timing reports inside the run step directories rather than directly in `reports/`:

```text
runs/RUN_2026-05-31_02-03-14/12-openroad-staprepnr/
runs/RUN_2026-05-31_02-03-14/31-openroad-stamidpnr/
runs/RUN_2026-05-31_02-03-14/36-openroad-stamidpnr-1/
runs/RUN_2026-05-31_02-03-14/38-openroad-stamidpnr-2/
runs/RUN_2026-05-31_02-03-14/44-openroad-stamidpnr-3/
runs/RUN_2026-05-31_02-03-14/56-openroad-stapostpnr/
```

Useful commands to locate timing evidence:

```sh
find runs/RUN_2026-05-31_02-03-14 -name summary.rpt -o -name checks.rpt -o -name "wns.*.rpt" -o -name "tns.*.rpt"
find runs/RUN_2026-05-31_02-03-14 -path "*openroad-stapostpnr*" -type f
```
