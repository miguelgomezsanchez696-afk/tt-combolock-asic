import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


KEY_POSITIONS = {
    0x1: (0, 0),
    0x2: (0, 1),
    0x3: (0, 2),
    0xA: (0, 3),
    0x4: (1, 0),
    0x5: (1, 1),
    0x6: (1, 2),
    0xB: (1, 3),
    0x7: (2, 0),
    0x8: (2, 1),
    0x9: (2, 2),
    0xC: (2, 3),
    "*": (3, 0),
    0x0: (3, 1),
    "#": (3, 2),
    0xD: (3, 3),
}


def signal_value(signal):
    return int(signal.value)


def assert_uo_out(dut, expected, message):
    got = signal_value(dut.uo_out)
    assert got == expected, f"{message}: expected 0b{expected:08b}, got 0b{got:08b}"


async def keypad_column_driver(dut, pressed_key):
    """Drive keypad columns from the DUT row scan outputs."""
    while True:
        await FallingEdge(dut.clk)

        value = 0xF0
        if pressed_key["down"]:
            active_row = pressed_key["row"]
            active_col = pressed_key["col"]
            rows = signal_value(dut.uio_out) & 0xF

            if ((rows >> active_row) & 0x1) == 0:
                cols = (~(1 << active_col)) & 0xF
                value = cols << 4

        dut.uio_in.value = value


async def press_key(dut, pressed_key, key):
    row, col = KEY_POSITIONS[key]

    await FallingEdge(dut.clk)
    pressed_key["row"] = row
    pressed_key["col"] = col
    pressed_key["down"] = True

    for _ in range(8):
        await FallingEdge(dut.clk)

    pressed_key["down"] = False

    for _ in range(8):
        await FallingEdge(dut.clk)


async def press_code(dut, pressed_key, code):
    await press_key(dut, pressed_key, code)


async def press_star(dut, pressed_key):
    await press_key(dut, pressed_key, "*")


async def press_hash(dut, pressed_key):
    await press_key(dut, pressed_key, "#")


async def enter_code(dut, pressed_key, code):
    await press_code(dut, pressed_key, code)
    await press_hash(dut, pressed_key)


@cocotb.test()
async def combolock_keypad_flow(dut):
    pressed_key = {"down": False, "row": 0, "col": 0}

    dut.ui_in.value = 0
    dut.uio_in.value = 0xF0
    dut.ena.value = 1
    dut.rst_n.value = 0
    dut.clk.value = 0

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    cocotb.start_soon(keypad_column_driver(dut, pressed_key))

    for _ in range(2):
        await RisingEdge(dut.clk)

    assert_uo_out(dut, 0x00, "reset state")
    assert signal_value(dut.uio_oe) == 0x0F, (
        f"uio_oe direction mask: expected 0b00001111, "
        f"got 0b{signal_value(dut.uio_oe):08b}"
    )

    dut.rst_n.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)

    assert_uo_out(dut, 0x00, "post-reset state")
    assert signal_value(dut.uio_oe) == 0x0F

    await press_code(dut, pressed_key, 0xA)
    assert signal_value(dut.entered_code) == 0xA, "key A should update entered_code"
    assert_uo_out(dut, 0x00, "code key should not change password or status")

    await press_star(dut, pressed_key)
    assert signal_value(dut.password) == 0xA, "star should store entered_code as password"
    assert_uo_out(dut, 0xA0, "password changed with star")

    await enter_code(dut, pressed_key, 0xA)
    assert_uo_out(dut, 0xA1, "correct password should unlock")

    await enter_code(dut, pressed_key, 0x3)
    assert_uo_out(dut, 0xA4, "first wrong password should increment attempts")

    await enter_code(dut, pressed_key, 0x4)
    assert_uo_out(dut, 0xA8, "second wrong password should increment attempts")

    await enter_code(dut, pressed_key, 0x5)
    assert_uo_out(dut, 0xAE, "third wrong password should lock out")

    await enter_code(dut, pressed_key, 0xA)
    assert_uo_out(dut, 0xAE, "lockout should ignore later correct password")
