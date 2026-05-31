# Verification

This project has three verification layers:

- RTL simulation with Icarus Verilog.
- Cocotb verification with an active keypad model.
- Physical verification evidence exported from a completed local LibreLane run.

## RTL Simulation

Run:

```sh
make sim
```

Equivalent raw commands:

```sh
mkdir -p sim
iverilog -g2012 -o sim/tb_combolock.vvp test/tb_combolock.v src/*.v
vvp sim/tb_combolock.vvp
```

Expected result:

```text
PASS
```

The Verilog testbench verifies reset behavior, keypad code entry, password storage with `*`, password checking with `#`, correct-password unlock, failed-attempt counting, lockout after three wrong attempts, and `uio_oe = 8'b0000_1111`.

Committed RTL evidence:

- [reports/rtl_simulation_pass.txt](../reports/rtl_simulation_pass.txt)
- [docs/images/rtl_waveform_capture.png](images/rtl_waveform_capture.png)

## Cocotb Verification

Install the local Python dependency if needed:

```sh
pip install -r requirements.txt
```

Run:

```sh
make cocotb
```

Expected result:

```text
TESTS=1 PASS=1 FAIL=0
```

The Cocotb test lives in `test/cocotb/test_combolock.py`. It compiles the unchanged RTL and models a 4x4 matrix keypad by reading active-low row scan outputs on `uio_out[3:0]` and driving active-low column inputs on `uio_in[7:4]`.

The Cocotb flow verifies reset behavior, the `uio_oe` direction mask, keypad entry, password storage, correct-password unlock, wrong-password attempts, and final lockout. The entered-code check is white-box because `entered_code` is internal state rather than a top-level output.

See [cocotb_verification.md](cocotb_verification.md) for focused Cocotb notes.

## GitHub Actions

GitHub Actions is configured in [../.github/workflows/test.yml](../.github/workflows/test.yml). The workflow runs on push, pull request, and manual dispatch. It installs Icarus Verilog, runs `make sim`, installs `requirements.txt`, and runs `make cocotb`.

LibreLane is intentionally not run in CI because it requires a full PDK and a heavier physical-design environment than the lightweight RTL checks.

## Physical Verification

The complete signoff run was performed locally with LibreLane. The `runs/` directory is ignored and not committed, so review evidence is exported into committed files under [../reports/](../reports/). The local run tag `RUN_2026-05-31_02-03-14` is retained only for traceability.

| Check | Meaning | Committed evidence |
| --- | --- | --- |
| DRC | Design Rule Check confirms that layout geometry and spacing satisfy process rules. | [Magic DRC](../reports/drc_violations.magic.rpt), [KLayout DRC](../reports/drc_violations.klayout.json) |
| LVS | Layout Versus Schematic confirms that the extracted layout netlist matches the synthesized design netlist. | [Netgen LVS](../reports/lvs.netgen.rpt) |
| Antenna | Checks for long conductors that could collect fabrication charge and damage transistor gates. | [Antenna report](../reports/antenna.rpt) |
| Manufacturability | Final flow-level readiness summary that combines required physical checks. | [Manufacturability report](../reports/manufacturability.rpt), [Signoff summary](../reports/flow_signoff_summary.txt) |

## Latest Recorded Results

| Check | Result |
| --- | --- |
| RTL simulation | Passed |
| Cocotb verification | Passed when `make cocotb` completes with `PASS=1` |
| DRC | Passed |
| LVS | Passed |
| Antenna | Passed |
| Manufacturability | Passed |

Additional report links:

- [reports/flow_summary.md](../reports/flow_summary.md)
- [reports/final_metrics.json](../reports/final_metrics.json)
- [reports/flow.log](../reports/flow.log)

Visual verification evidence:

- [Block diagram](images/block_diagram.png)
- [Keypad mapping](images/keypad_mapping.png)
- [RTL waveform](images/rtl_waveform_capture.png)
- [KLayout layout view](images/klayout_view.png)
- [TinyTapeout GDS Viewer 3D view](images/tinytapeout_3d_view.png)
- [Signoff summary](images/signoff_summary.png)
