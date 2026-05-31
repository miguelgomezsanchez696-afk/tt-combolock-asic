## How it works

This project implements a 4-bit combination lock for the TinyTapeout user-module interface. The functional change from the base Combination Lock is the input method: a standard Arduino-style 4x4 matrix keypad is connected to the bidirectional `uio` pins instead of using DIP switches.

The ASIC drives `uio[3:0]` as active-low keypad rows and reads `uio[7:4]` as active-low keypad columns. The column lines should have external pull-ups. Keys `0` through `9` and `A` through `D` load the current 4-bit entered code. Pressing `*` stores the current entered code as the password. Pressing `#` compares the current entered code against the stored password.

A correct check asserts `uo_out[0]` (`unlocked`). A wrong check increments the failed-attempt counter on `uo_out[3:2]`; after three failed attempts, `uo_out[1]` (`locked_out`) is asserted and further password updates or checks are ignored until reset. For bring-up and demonstration, `uo_out[7:4]` exposes the stored password. The design drives `uio_oe = 8'b0000_1111`.

## How to test

Run the RTL simulation from the repository root:

```sh
make sim
```

Expected output is `PASS`.

The physical flow was reproduced locally with LibreLane using:

```sh
make flow
```

If the local environment needs an explicit PDK location, run:

```sh
export PDK_ROOT=/tmp/librelane-pdks
librelane config.json
```

The recorded local flow passed DRC, LVS, antenna, and manufacturability checks. Evidence is kept in `reports/`, especially `reports/flow_summary.md` and `reports/flow_signoff_summary.txt`.
