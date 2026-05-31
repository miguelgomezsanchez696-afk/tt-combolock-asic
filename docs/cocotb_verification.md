# Cocotb Verification

This project includes a Cocotb testbench under `test/cocotb/` for the
`tt_um_combolock` top module.

Run it with:

```sh
make cocotb
```

If Cocotb is not installed in the active Python environment, install the local
Python requirements first:

```sh
pip install -r requirements.txt
```

The Cocotb test uses Icarus Verilog through Cocotb. It compiles the unchanged
RTL files:

- `src/tt_um_combolock.v`
- `src/keypad_scanner.v`

The test verifies reset behavior, the fixed `uio_oe` direction mask, keypad
code entry, password storage with `*`, password checking with `#`, the
`unlocked` output, failed-attempt counting, and lockout after three wrong
attempts.

The keypad model reads the DUT row scan outputs on `uio_out[3:0]` and drives
active-low column inputs on `uio_in[7:4]`, matching the 4x4 matrix keypad
interface used by the Verilog testbench.

The entered-code check is white-box because `entered_code` is an internal RTL
register and is not exposed on a top-level output.
