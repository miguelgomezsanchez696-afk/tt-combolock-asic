# Visual Evidence Images

The PNG files in this directory are generated documentation evidence for the ASIC project.

Generated automatically:

- `block_diagram.png`
- `keypad_mapping.png`
- `rtl_waveform.png`
- `final_layout.png`
- `signoff_summary.png`

`rtl_waveform.png` is generated from `sim/tb_combolock.vcd`. To inspect the waveform manually:

```sh
make sim
gtkwave sim/tb_combolock.vcd
```

Recommended signals:

- `clk`
- `rst_n`
- `uio_in`
- `uio_out`
- `uio_oe`
- `uo_out`
- `tb_combolock.dut.key_valid`
- `tb_combolock.dut.key_code`
- `tb_combolock.dut.key_star`
- `tb_combolock.dut.key_hash`
- `tb_combolock.dut.unlocked`
- `tb_combolock.dut.locked_out`
- `tb_combolock.dut.attempts`

`final_layout.png` is a DEF-derived overview from:

```text
runs/RUN_2026-05-31_02-03-14/final/def/tt_um_combolock.def
```

To inspect the actual final layout manually with KLayout:

```sh
klayout runs/RUN_2026-05-31_02-03-14/final/gds/tt_um_combolock.gds
```

To inspect it manually with OpenROAD:

```sh
openroad
read_db runs/RUN_2026-05-31_02-03-14/final/odb/tt_um_combolock.odb
gui::show
```
