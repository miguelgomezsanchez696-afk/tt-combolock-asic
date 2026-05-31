# User Manual

## What the Chip Does

This chip implements a 4-bit combination lock using a TinyTapeout-style digital ASIC interface. A user enters one 4-bit value from a standard 4x4 matrix keypad. The chip can store that value as the password, compare later entries against the stored password, report when the lock is unlocked, count failed attempts, and enter a lockout state after three wrong checks.

The main user-interface difference from a basic DIP-switch combination lock is that the code is entered from a typical Arduino-style 4x4 keypad.

## How the Lock Works

The chip keeps these internal state values:

| State | Meaning |
| --- | --- |
| Stored password | The 4-bit password used for comparison. |
| Entered code | The most recent 4-bit key value pressed by the user. |
| Failed attempts | The number of wrong password checks since the last reset, password update, or correct check. |
| `unlocked` | Output flag that becomes active after a correct password check. |
| `locked_out` | Output flag that becomes active after three failed checks. |

After reset, the stored password is `0`, the entered code is `0`, the failed-attempt count is `0`, `unlocked` is low, and `locked_out` is low.

## Connecting a 4x4 Matrix Keypad

Connect the keypad rows and columns to the bidirectional `uio` pins:

| Keypad signal | ASIC signal | Direction at ASIC |
| --- | --- | --- |
| Row 0 | `uio[0]` | Output |
| Row 1 | `uio[1]` | Output |
| Row 2 | `uio[2]` | Output |
| Row 3 | `uio[3]` | Output |
| Column 0 | `uio[4]` | Input |
| Column 1 | `uio[5]` | Input |
| Column 2 | `uio[6]` | Input |
| Column 3 | `uio[7]` | Input |

The row pins are active-low outputs from the ASIC. The column pins are active-low inputs to the ASIC and should have external pull-up resistors. When no key is pressed, each column should read `1`. When a key is pressed in the active row, the matching column is pulled low and reads `0`.

The chip drives `uio_oe = 8'b0000_1111`, so `uio[3:0]` are outputs and `uio[7:4]` are inputs.

## Rows, Columns, and Key Mapping

The keypad scanner steps through one active row at a time. A key is identified by the active row and the column that is pulled low.

| Row | Column 0 | Column 1 | Column 2 | Column 3 |
| --- | --- | --- | --- | --- |
| Row 0 | `1` | `2` | `3` | `A` |
| Row 1 | `4` | `5` | `6` | `B` |
| Row 2 | `7` | `8` | `9` | `C` |
| Row 3 | `*` | `0` | `#` | `D` |

## Key Functions

| Key | Function |
| --- | --- |
| `0`-`9` | Load the matching 4-bit entered code. |
| `A` | Load entered code `0xA`. |
| `B` | Load entered code `0xB`. |
| `C` | Load entered code `0xC`. |
| `D` | Load entered code `0xD`. |
| `*` | Store the current entered code as the password. |
| `#` | Check the current entered code against the stored password. |

Only one 4-bit code is stored as the current entry. This is not a multi-digit decimal password. For example, pressing `A` loads the entered code with hexadecimal value `0xA`.

## Lock Behavior

When `#` is pressed, the chip compares the current entered code against the stored password:

| Condition | Result |
| --- | --- |
| Entered code matches stored password | `unlocked` becomes active and failed attempts return to `0`. |
| Entered code does not match stored password | `unlocked` becomes inactive and failed attempts increment. |
| Third failed attempt occurs | `locked_out` becomes active. |
| `locked_out` is active | Further password updates and checks are ignored until reset. |

Pressing `*` stores the current entered code as the password when the chip is not locked out. This also clears failed attempts and clears `unlocked`.

Reset clears the lock state. It sets the stored password and entered code back to `0`, clears failed attempts, clears `unlocked`, and clears `locked_out`.

## Reading Outputs

| ASIC output | Meaning |
| --- | --- |
| `uo_out[0]` | `unlocked`; high after a correct password check. |
| `uo_out[1]` | `locked_out`; high after three failed checks. |
| `uo_out[3:2]` | Failed-attempt count. |
| `uo_out[7:4]` | Stored password, provided as debug/status output for bring-up and demonstrations. |

## Manual Test Procedure

Use this procedure to test the chip manually with a connected keypad:

1. Drive `rst_n` low, then high again to reset the chip.
2. Keep `ena` high.
3. Press a code key such as `A`.
4. Press `*` to store `A` as the password.
5. Press `A` again.
6. Press `#` to check the entered code.
7. Observe `uo_out[0]`; `unlocked` should be high.
8. Press wrong code keys and then `#` three times.
9. Observe `uo_out[1]`; `locked_out` should be high after the third wrong check.

Example sequence:

| Step | User action | Expected result |
| --- | --- | --- |
| 1 | Reset chip | Lock state clears. |
| 2 | Press `A` | Entered code becomes `0xA`. |
| 3 | Press `*` | Password becomes `0xA`. |
| 4 | Press `A` | Entered code becomes `0xA`. |
| 5 | Press `#` | Password check succeeds. |
| 6 | Observe `unlocked` | `uo_out[0]` is high. |
| 7 | Try wrong keys three times, pressing `#` after each one | Failed attempts reach 3. |
| 8 | Observe `locked_out` | `uo_out[1]` is high. |
