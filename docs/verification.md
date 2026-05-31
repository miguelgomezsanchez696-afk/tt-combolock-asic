# Verification

This project has three verification levels recorded in the repository:

- RTL simulation with Icarus Verilog.
- Cocotb simulation with Icarus Verilog.
- Physical verification from the completed LibreLane flow.

## RTL Simulation

Run:

```sh
make sim
```

Equivalent raw commands:

```sh
iverilog -g2012 -o sim/tb_combolock.vvp test/tb_combolock.v src/*.v
vvp sim/tb_combolock.vvp
```

Expected output:

```text
PASS
```

The testbench verifies reset behavior, keypad code entry, password storage with `*`, password checking with `#`, the `unlocked` output, failed-attempt counting, lockout after three wrong attempts, and the fixed `uio_oe` direction mask.

Visual evidence:

- [RTL waveform](images/rtl_waveform.png)
- [Signoff summary](images/signoff_summary.png)
- [Manual waveform inspection commands](images/README.md)

## Cocotb Simulation

Run:

```sh
make cocotb
```

If Cocotb is not installed in the active Python environment, install:

```sh
pip install -r requirements.txt
```

The Cocotb test lives in `test/cocotb/test_combolock.py`. It compiles the unchanged RTL and models a 4x4 matrix keypad by reading `uio_out[3:0]` row scan outputs and driving active-low column inputs on `uio_in[7:4]`.

The Cocotb flow verifies reset behavior, `uio_oe == 8'b0000_1111`, entered-code updates, password storage with `*`, password checking with `#`, correct-password unlock, failed-attempt counting, and lockout after three wrong attempts. The entered-code assertion is white-box because `entered_code` is internal state rather than a top-level output.

See [Cocotb verification](cocotb_verification.md) for the focused run instructions.

## GitHub Actions

GitHub Actions is configured in `.github/workflows/test.yml`. The workflow runs on push, pull request, and manual dispatch. It installs Icarus Verilog and runs:

```sh
make sim
```

This covers the course automation and CI evidence for the RTL simulation flow.

## LibreLane Flow

The design was hardened with LibreLane using `config.json`. To reproduce the flow locally:

```sh
make flow
```

Equivalent raw command:

```sh
librelane config.json
```

If a PDK permission issue occurs because the default PDK directory is not writable, use:

```sh
export PDK_ROOT=/tmp/librelane-pdks
librelane config.json
```

The recorded flow evidence is already included under `reports/`. The physical flow does not need to be rerun for documentation review.

## OpenSTA and Timing

OpenROAD/OpenSTA timing reports are generated inside the LibreLane run directories. The completed run stores post-route STA at:

```text
runs/RUN_2026-05-31_02-03-14/56-openroad-stapostpnr/
```

The post-route summary reports 0 setup violations and 0 hold violations. See `docs/synthesis_timing.md` for synthesis and timing details.

## Physical Verification Checks

| Check | Meaning |
| --- | --- |
| DRC | Design Rule Check. Confirms that the layout follows process geometry and spacing rules. |
| LVS | Layout Versus Schematic. Confirms that the extracted layout netlist matches the synthesized design netlist. |
| Antenna check | Looks for long metal structures that could collect charge during fabrication and damage transistor gates. |
| Manufacturability | Final flow-level summary that the generated layout has passed required physical checks for fabrication readiness. |

## Latest Recorded Local Results

The latest complete recorded local flow passed:

| Check | Result |
| --- | --- |
| DRC | Passed |
| LVS | Passed |
| Antenna | Passed |
| Manufacturability | Passed |

Key evidence files:

- `reports/flow_summary.md`
- `reports/flow_signoff_summary.txt`
- `reports/rtl_simulation_pass.txt`
- `reports/drc_violations.magic.rpt`
- `reports/drc_violations.klayout.json`
- `reports/lvs.netgen.rpt`
- `reports/antenna.rpt`
- `reports/manufacturability.rpt`

Visual evidence:

- [Block diagram](images/block_diagram.png)
- [Keypad mapping](images/keypad_mapping.png)
- [Signoff summary](images/signoff_summary.png)

## Run Directory Note

The newest timestamped run directory is `runs/RUN_2026-05-31_02-17-38`, but it is incomplete and stops before final signoff output. The latest complete signoff run is `runs/RUN_2026-05-31_02-03-14`.
