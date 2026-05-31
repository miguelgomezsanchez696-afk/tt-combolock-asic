# Layout Stages

This document summarizes the physical layout stages from the completed local LibreLane signoff run. The `runs/` directory is ignored and not committed, so review evidence is the exported content in `reports/`, visual screenshots in `docs/images/`, and the final GDS in `docs/gds/tt_um_combolock.gds`.

The local run tag is `RUN_2026-05-31_02-03-14`, recorded only for traceability.

## Floorplan

Floorplanning is controlled by `config.json`.

| Setting | Value |
| --- | --- |
| `FP_SIZING` | `absolute` |
| `DIE_AREA` | `0 0 161 111` |
| Die size | 161 um x 111 um |
| Die area | 17871 um^2 |
| Core bbox from metrics | `5.52 10.88 155.48 97.92` |
| Pin order | `pin_order.cfg` through `IO_PIN_ORDER_CFG` |

This stage creates the initial DEF/ODB layout, applies the die/core area, creates placement rows, and prepares the design for power grid generation and placement.

## Power Grid and IO Placement

Power connections, tap/endcap insertion, PDN generation, and explicit IO placement happen before main placement.

| Step | Evidence summary |
| --- | --- |
| Power connections | LibreLane/OpenROAD flow log in [../reports/flow.log](../reports/flow.log) |
| Tap/endcap insertion | LibreLane/OpenROAD flow log in [../reports/flow.log](../reports/flow.log) |
| PDN generation | LibreLane/OpenROAD flow log in [../reports/flow.log](../reports/flow.log) |
| Custom IO placement | `pin_order.cfg` and LibreLane/OpenROAD flow log in [../reports/flow.log](../reports/flow.log) |

`pin_order.cfg` fixes top-level pins on the north, west, east, and south sides of the macro.

## Placement

Placement is performed by OpenROAD. Final exported metrics report:

| Metric | Value |
| --- | ---: |
| Standard-cell instances | 384 |
| Total instances including physical cells | 1474 |
| Standard-cell area | 1899.32 um^2 |
| Total instance area | 13052.5 um^2 |
| Instance utilization | 0.145514 |

Committed evidence:

- [../reports/final_metrics.json](../reports/final_metrics.json)
- [../reports/flow_summary.md](../reports/flow_summary.md)
- [../reports/flow.log](../reports/flow.log)

## CTS

Clock tree synthesis is performed by OpenROAD for the `clk` domain. The final metrics report 4 clock buffer instances. Timing is checked after CTS and again after routing.

Committed evidence:

- [../reports/final_metrics.json](../reports/final_metrics.json)
- [synthesis_timing.md](synthesis_timing.md)

## Routing

LibreLane performs global routing, antenna checking and repair, and detailed routing before signoff.

Final routing metrics:

| Metric | Value |
| --- | ---: |
| Route DRC errors | 0 |
| Route wirelength | 3201 um |
| Route vias | 1007 |
| Antenna violating nets | 0 |
| Antenna violating pins | 0 |

Committed evidence:

- [../reports/final_metrics.json](../reports/final_metrics.json)
- [../reports/antenna.rpt](../reports/antenna.rpt)
- [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt)

## Extraction and Final STA

After routing, LibreLane runs fill insertion, parasitic extraction, and post-route timing analysis. The final post-route STA summary shows 0 setup violations and 0 hold violations.

Committed timing and metrics evidence:

- [synthesis_timing.md](synthesis_timing.md)
- [../reports/final_metrics.json](../reports/final_metrics.json)
- [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt)

## Streamout and Signoff Layout Files

The final GDS exported from the local run is committed for viewer inspection:

- [gds/tt_um_combolock.gds](gds/tt_um_combolock.gds)

The broader local final output included GDS, DEF, ODB, LEF, gate-level netlist, parasitics, and timing files. Those heavy local run directories are not committed; the review-facing evidence is the exported `reports/` set and the committed final GDS.

## Opening the Final Layout

If KLayout is installed, open the committed GDS:

```sh
klayout docs/gds/tt_um_combolock.gds
```

The same GDS can be opened in the TinyTapeout GDS Viewer. See [gds/README.md](gds/README.md) for viewer instructions.

## Visual Evidence

- [KLayout layout view](images/klayout_view.png)
- [TinyTapeout GDS Viewer 3D view](images/tinytapeout_3d_view.png)
- [Signoff summary](images/signoff_summary.png)
- [Manual layout inspection notes](images/README.md)
