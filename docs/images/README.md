# Visual Evidence Images

The PNG files in this directory are documentation evidence for the ASIC project.

Generated automatically:

- `block_diagram.png`
- `keypad_mapping.png`
- `signoff_summary.png`

Real screenshots:

- `rtl_waveform_capture.png` is a real GTKWave waveform screenshot from the RTL simulation VCD.
- `klayout_view.png` is a real KLayout screenshot of the final layout.
- `tinytapeout_3d_view.png` is a real TinyTapeout GDS Viewer 3D screenshot of the final layout.

To inspect the waveform manually:

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
