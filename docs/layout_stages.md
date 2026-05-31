# Layout Stages

This document records the physical layout stages from the completed LibreLane run:

```text
runs/RUN_2026-05-31_02-03-14
```

The newest timestamped run, `RUN_2026-05-31_02-17-38`, is incomplete and does not contain final layout output. The complete evidence is from `RUN_2026-05-31_02-03-14` and the exported files in `reports/`.

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

Evidence:

```text
runs/RUN_2026-05-31_02-03-14/13-openroad-floorplan/
```

This stage creates the initial DEF/ODB layout, applies the die/core area, creates placement rows, and prepares the design for power grid generation and placement.

## Power Grid and IO Placement

Power connections, tap/endcap insertion, PDN generation, and explicit IO placement happen before main placement.

| Step | Directory |
| --- | --- |
| Power connections | `16-odb-setpowerconnections` |
| Tap/endcap insertion | `19-openroad-tapendcapinsertion` |
| PDN generation | `21-openroad-generatepdn` |
| Custom IO placement | `26-odb-customioplacement` |

`pin_order.cfg` fixes top-level pins on the north, west, east, and south sides of the macro.

## Placement

Placement is performed by OpenROAD:

| Step | Directory |
| --- | --- |
| Global placement | `28-openroad-globalplacement` |
| Detailed placement | `34-openroad-detailedplacement` |
| Post-placement timing repair | `32-openroad-repairdesignpostgpl` |

Final metrics:

| Metric | Value |
| --- | ---: |
| Standard-cell instances | 384 |
| Total instances including physical cells | 1474 |
| Standard-cell area | 1899.32 um^2 |
| Total instance area | 13052.5 um^2 |
| Instance utilization | 0.145514 |

## CTS

Clock tree synthesis is performed in:

```text
runs/RUN_2026-05-31_02-03-14/35-openroad-cts/
```

The final metrics report 4 clock buffer instances. Timing is checked after CTS in the mid-PNR STA stages.

## Routing

Routing is performed in:

| Step | Directory |
| --- | --- |
| Global routing | `39-openroad-globalrouting` |
| Antenna checking and repair | `40-openroad-checkantennas`, `43-openroad-repairantennas`, `47-openroad-checkantennas-1` |
| Detailed routing | `45-openroad-detailedrouting` |

Final routing metrics:

| Metric | Value |
| --- | ---: |
| Route DRC errors | 0 |
| Route wirelength | 3201 um |
| Route vias | 1007 |
| Antenna violating nets | 0 |
| Antenna violating pins | 0 |

## Extraction and Final STA

After routing, LibreLane runs fill insertion, parasitic extraction, and post-route timing analysis.

| Step | Directory |
| --- | --- |
| Fill insertion | `53-openroad-fillinsertion` |
| RC extraction | `55-openroad-rcx` |
| Post-route STA | `56-openroad-stapostpnr` |

The final post-route STA summary shows 0 setup violations and 0 hold violations.

## Streamout and Signoff Layout Files

Final layout files are saved under:

```text
runs/RUN_2026-05-31_02-03-14/final/
```

Important files:

| File | Purpose |
| --- | --- |
| `final/gds/tt_um_combolock.gds` | Final GDS layout. |
| `final/klayout_gds/tt_um_combolock.klayout.gds` | KLayout streamout GDS. |
| `final/def/tt_um_combolock.def` | Final DEF. |
| `final/odb/tt_um_combolock.odb` | Final OpenDB database. |
| `final/lef/tt_um_combolock.lef` | LEF abstract. |
| `final/nl/tt_um_combolock.nl.v` | Final gate-level netlist. |
| `final/spef/` | Extracted parasitics by corner. |
| `final/sdf/` | SDF timing files by corner. |

## Opening the Final Layout

If KLayout is installed:

```sh
klayout runs/RUN_2026-05-31_02-03-14/final/gds/tt_um_combolock.gds
```

If OpenROAD is installed:

```sh
openroad
read_db runs/RUN_2026-05-31_02-03-14/final/odb/tt_um_combolock.odb
gui::show
```

`docs/images/klayout_view.png` is a real KLayout screenshot of the final layout. `docs/images/tinytapeout_3d_view.png` is a real TinyTapeout GDS Viewer 3D screenshot of the final layout.

## Visual Evidence

- [KLayout layout view](images/klayout_view.png)
- [TinyTapeout GDS Viewer 3D view](images/tinytapeout_3d_view.png)
- [Signoff summary](images/signoff_summary.png)
- [Manual layout inspection commands](images/README.md)
