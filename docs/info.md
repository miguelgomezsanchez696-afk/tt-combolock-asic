## How it works

This project implements a 4-bit combination lock for the TinyTapeout user-module interface. A standard Arduino-style 4x4 matrix keypad is connected to the bidirectional `uio` pins: `uio[3:0]` drive the keypad rows as active-low outputs, and `uio[7:4]` read the keypad columns as active-low inputs with external pull-ups.

Keys `0` through `9` and `A` through `D` load a 4-bit code. Pressing `*` stores the current code as the password. Pressing `#` compares the current code against the stored password. A correct code asserts `uo_out[0]` (`unlocked`). An incorrect code increments the failed-attempt counter on `uo_out[3:2]`; after three failed attempts, `uo_out[1]` (`locked_out`) is asserted and further password changes or unlock attempts are ignored until reset.

For bring-up and demonstration, `uo_out[7:4]` exposes the stored password. The design drives `uio_oe = 8'b0000_1111`, making the low nibble of `uio` outputs for keypad rows and the high nibble inputs for keypad columns.

## How to test

Run the RTL simulation from the repository root:

```sh
make sim
```

The simulation uses Icarus Verilog and the testbench in `test/tb_combolock.v`. It verifies reset behavior, keypad-based password storage, correct unlock, failed-attempt counting, lockout after three failed attempts, and the fixed `uio_oe` direction mask.

The physical flow was reproduced locally with LibreLane using `config.json`:

```sh
make flow
```

If the local environment needs an explicit PDK location, run:

```sh
PDK_ROOT=/tmp/librelane-pdks make flow
```

The documented local run passed DRC, LVS, antenna, and manufacturability checks. The exported reports are kept in `reports/`; the full `runs/` directory is intentionally ignored by Git.

## External hardware

A standard 4x4 matrix keypad is expected. The keypad columns should have pull-up resistors so that an unpressed key reads as `1` and a pressed key pulls the active column low through the selected active-low row.
