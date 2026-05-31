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

Run the Cocotb keypad verification, if the Python requirements are installed:

```sh
make cocotb
```

The GitHub Actions workflow in `.github/workflows/test.yml` runs both `make sim` and `make cocotb`.

The physical flow was reproduced locally with LibreLane using:

```sh
make flow
```

The complete LibreLane run was local and is not rerun for repository review. The `runs/` directory is ignored, so it is not used as GitHub evidence. Extracted signoff evidence is committed under `reports/`, visual evidence is committed under `docs/images/`, and the final GDS is committed at `docs/gds/tt_um_combolock.gds`.

The recorded local flow passed DRC, LVS, antenna, and manufacturability checks. The main review entry points are:

- `README.md`
- `docs/project_review_checklist.md`
- `docs/user_manual.md`
- `docs/pinout.md`
- `reports/flow_summary.md`
- `reports/flow_signoff_summary.txt`
