# Manufacturing Readiness

This project has completed a local RTL-to-GDS hardening flow with LibreLane. The recorded run shows that the design passed the physical checks needed for final presentation.

## Hardened Design

The top-level design is `tt_um_combolock`. LibreLane was run with `config.json`, which references the synthesizable Verilog sources:

- `src/tt_um_combolock.v`
- `src/keypad_scanner.v`

The design is a small digital macro: a keypad scanner, a 4-bit password register, a 4-bit entered-code register, a 2-bit failed-attempt counter, and lock status logic.

## Fixed Die Area

The physical configuration uses an absolute die area:

```json
"DIE_AREA": "0 0 161 111"
```

This corresponds to:

| Dimension | Value |
| --- | --- |
| Width | 161 um |
| Height | 111 um |
| Area | 17871 um^2 |

This size is reasonable for a small TinyTapeout-style digital macro. The logic is compact, but the hardened block still needs space for standard cells, routing tracks, clock distribution, physical margins, and top-level pins.

## Pin Placement

All top-level pins are placed through `pin_order.cfg`. The LibreLane configuration includes:

```json
"IO_PIN_ORDER_CFG": "dir::pin_order.cfg"
```

A previous placement error occurred because the flow did not have a valid explicit placement order for the top-level pins. Adding `IO_PIN_ORDER_CFG` solved that issue by giving LibreLane a deterministic pin order for the TinyTapeout-style interface.

## Final Physical Checks

The latest recorded local flow passed:

| Check | Result |
| --- | --- |
| DRC | Passed |
| LVS | Passed |
| Antenna | Passed |
| Manufacturability | Passed |

These results indicate that the generated layout is consistent with the design netlist, follows physical design rules, has no recorded antenna violations, and passed the final manufacturability report in the recorded flow.

## Evidence

The `reports/` directory contains the evidence for the recorded run:

- `reports/flow_summary.md`
- `reports/flow_signoff_summary.txt`
- `reports/final_metrics.json`
- `reports/flow.log`
- `reports/drc_violations.magic.rpt`
- `reports/drc_violations.klayout.json`
- `reports/lvs.netgen.rpt`
- `reports/antenna.rpt`
- `reports/manufacturability.rpt`

The recorded flow summary reports 0 route DRC errors, 0 Magic DRC errors, 0 KLayout DRC errors, 0 LVS errors, and 0 antenna violating nets.
