# Verification Manual

This project has two verification levels recorded in the repository:

- RTL simulation with Icarus Verilog.
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

## Physical Verification Checks

| Check | Meaning |
| --- | --- |
| DRC | Design Rule Check. Confirms that the layout follows the foundry process geometry and spacing rules. |
| LVS | Layout Versus Schematic. Confirms that the extracted layout netlist matches the synthesized design netlist. |
| Antenna check | Looks for long metal structures that could collect charge during fabrication and damage transistor gates. |
| Manufacturability | Final flow-level summary that the generated layout has passed required physical checks for fabrication readiness. |

## Latest Recorded Local Results

The latest recorded local flow passed:

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
