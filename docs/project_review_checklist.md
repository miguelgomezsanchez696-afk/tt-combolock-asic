# Project Review Checklist

Use this checklist for a final repository review against the course Digital ASIC Design flow.

| Area | Status | Evidence |
| --- | --- | --- |
| RTL design | Complete | `src/tt_um_combolock.v`, `src/keypad_scanner.v` |
| 4x4 keypad modification | Complete | `uio[3:0]` rows, `uio[7:4]` columns, [pinout.md](pinout.md) |
| RTL verification | Complete | `test/tb_combolock.v`, `make sim`, [../reports/rtl_simulation_pass.txt](../reports/rtl_simulation_pass.txt) |
| Cocotb verification | Complete | `test/cocotb/test_combolock.py`, `make cocotb`, [cocotb_verification.md](cocotb_verification.md) |
| Makefile | Complete | Top-level `Makefile` has `sim`, `cocotb`, `flow`, `reports`, and `clean` targets |
| LibreLane RTL-to-GDS | Complete locally | `config.json`, [../reports/flow_summary.md](../reports/flow_summary.md) |
| Pin ordering | Complete | `pin_order.cfg` |
| DRC | Passed | [../reports/drc_violations.magic.rpt](../reports/drc_violations.magic.rpt), [../reports/drc_violations.klayout.json](../reports/drc_violations.klayout.json) |
| LVS | Passed | [../reports/lvs.netgen.rpt](../reports/lvs.netgen.rpt) |
| Antenna | Passed | [../reports/antenna.rpt](../reports/antenna.rpt) |
| Manufacturability | Passed | [../reports/manufacturability.rpt](../reports/manufacturability.rpt), [../reports/flow_signoff_summary.txt](../reports/flow_signoff_summary.txt) |
| Visual evidence | Complete | [images/block_diagram.png](images/block_diagram.png), [images/keypad_mapping.png](images/keypad_mapping.png), [images/rtl_waveform_capture.png](images/rtl_waveform_capture.png), [images/klayout_view.png](images/klayout_view.png), [images/tinytapeout_3d_view.png](images/tinytapeout_3d_view.png), [images/signoff_summary.png](images/signoff_summary.png) |
| GDS viewer file | Complete | [gds/tt_um_combolock.gds](gds/tt_um_combolock.gds) |
| User manual and pinout | Complete | [user_manual.md](user_manual.md), [pinout.md](pinout.md) |
| Course coverage documentation | Complete | [design_flow.md](design_flow.md), [../README.md](../README.md#course-tutorial-coverage) |
| Project review checklist | Complete | This file |
| GitHub Actions | Complete | [../.github/workflows/test.yml](../.github/workflows/test.yml) runs RTL simulation and Cocotb verification |

## Review Notes

- The complete signoff run was performed locally.
- The `runs/` directory is ignored and is not used as GitHub evidence.
- Extracted physical verification evidence is committed under `reports/`.
- The final GDS is committed under `docs/gds/tt_um_combolock.gds`.
- The local run tag `RUN_2026-05-31_02-03-14` is recorded only for traceability.
