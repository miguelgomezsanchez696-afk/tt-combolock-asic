# Pinout

This document describes the TinyTapeout-style top-level interface used by `tt_um_combolock`.

## Dedicated Pins

| Signal | Direction | Description |
| --- | --- | --- |
| `clk` | Input | System clock. The project metadata uses 40 MHz. |
| `rst_n` | Input | Active-low reset. |
| `ena` | Input | Enable input. The lock state updates only when `ena` is high. |
| `ui_in[7:0]` | Input | Dedicated user inputs. Currently unused by the RTL and reserved. |
| `uo_out[7:0]` | Output | Dedicated user outputs for lock status, failed attempts, and debug password. |
| `uio_in[7:0]` | Input | Bidirectional input view. Used for keypad column inputs on `uio_in[7:4]`; `uio_in[3:0]` is unused. |
| `uio_out[7:0]` | Output | Bidirectional output drive values. Used for keypad row outputs on `uio_out[3:0]`; `uio_out[7:4]` is driven low. |
| `uio_oe[7:0]` | Output | Bidirectional output-enable mask. Fixed at `8'b0000_1111`. |

## Dedicated Input Pins

| Pin | Current use |
| --- | --- |
| `ui_in[0]` | Unused, reserved. |
| `ui_in[1]` | Unused, reserved. |
| `ui_in[2]` | Unused, reserved. |
| `ui_in[3]` | Unused, reserved. |
| `ui_in[4]` | Unused, reserved. |
| `ui_in[5]` | Unused, reserved. |
| `ui_in[6]` | Unused, reserved. |
| `ui_in[7]` | Unused, reserved. |

## Dedicated Output Pins

| Pin | Signal | Description |
| --- | --- | --- |
| `uo_out[0]` | `unlocked` | High after a correct password check. |
| `uo_out[1]` | `locked_out` | High after three failed password checks. |
| `uo_out[2]` | `failed_attempts[0]` | Failed-attempt counter bit 0. |
| `uo_out[3]` | `failed_attempts[1]` | Failed-attempt counter bit 1. |
| `uo_out[4]` | `debug_password[0]` | Stored password bit 0, exposed for bring-up and demo visibility. |
| `uo_out[5]` | `debug_password[1]` | Stored password bit 1, exposed for bring-up and demo visibility. |
| `uo_out[6]` | `debug_password[2]` | Stored password bit 2, exposed for bring-up and demo visibility. |
| `uo_out[7]` | `debug_password[3]` | Stored password bit 3, exposed for bring-up and demo visibility. |

The RTL assigns:

```verilog
assign uo_out = {password, attempts, locked_out, unlocked};
```

## Bidirectional Keypad Pins

| Pin | Direction | Signal | Description |
| --- | --- | --- | --- |
| `uio[0]` | Output | `keypad_row[0]` | Active-low keypad row 0. |
| `uio[1]` | Output | `keypad_row[1]` | Active-low keypad row 1. |
| `uio[2]` | Output | `keypad_row[2]` | Active-low keypad row 2. |
| `uio[3]` | Output | `keypad_row[3]` | Active-low keypad row 3. |
| `uio[4]` | Input | `keypad_col[0]` | Active-low keypad column 0 input. |
| `uio[5]` | Input | `keypad_col[1]` | Active-low keypad column 1 input. |
| `uio[6]` | Input | `keypad_col[2]` | Active-low keypad column 2 input. |
| `uio[7]` | Input | `keypad_col[3]` | Active-low keypad column 3 input. |

The RTL assigns:

```verilog
assign uio_out = {4'b0000, keypad_rows};
assign uio_oe  = 8'b0000_1111;
```

## Keypad Connection Table

| Keypad signal | ASIC pin | Notes |
| --- | --- | --- |
| Row 0 | `uio[0]` | Driven by ASIC, active low. |
| Row 1 | `uio[1]` | Driven by ASIC, active low. |
| Row 2 | `uio[2]` | Driven by ASIC, active low. |
| Row 3 | `uio[3]` | Driven by ASIC, active low. |
| Column 0 | `uio[4]` | Input to ASIC, active low, requires pull-up. |
| Column 1 | `uio[5]` | Input to ASIC, active low, requires pull-up. |
| Column 2 | `uio[6]` | Input to ASIC, active low, requires pull-up. |
| Column 3 | `uio[7]` | Input to ASIC, active low, requires pull-up. |

## Keypad Layout

| Row | Column 0 | Column 1 | Column 2 | Column 3 |
| --- | --- | --- | --- | --- |
| Row 0 | `1` | `2` | `3` | `A` |
| Row 1 | `4` | `5` | `6` | `B` |
| Row 2 | `7` | `8` | `9` | `C` |
| Row 3 | `*` | `0` | `#` | `D` |
