# TinyTapeout 4-bit Combination Lock ASIC

Proyecto ASIC digital estilo TinyTapeout para un candado combinacional de 4 bits con entrada por teclado matricial 4x4.

## Estructura

- `src/tt_um_combolock.v`: RTL principal Verilog sintetizable.
- `src/keypad_scanner.v`: escaner sintetizable para teclado matricial 4x4.
- `test/tb_combolock.v`: testbench Verilog para simulacion funcional.
- `sim/`: scripts o resultados temporales de simulacion.
- `docs/`: documentacion del diseno.
- `reports/`: reportes de flujo fisico.
- `config.json`: configuracion inicial para LibreLane.

## Interfaz TinyTapeout

El modulo principal es `tt_um_combolock` y usa la interfaz TinyTapeout:

- `ui_in[7:0]`: no usados para la clave ni para comandos.
- `uo_out[0]`: `unlocked`, indica contrasena correcta.
- `uo_out[1]`: `locked_out`, indica bloqueo despues de 3 intentos fallidos.
- `uo_out[3:2]`: contador de intentos fallidos.
- `uo_out[7:4]`: contrasena almacenada, expuesta para depuracion/demo.
- `uio[3:0]`: filas del teclado, salidas desde el ASIC.
- `uio[7:4]`: columnas del teclado, entradas hacia el ASIC.
- `uio_oe[3:0]`: `4'b1111`.
- `uio_oe[7:4]`: `4'b0000`.

El escaneo usa el cableado habitual de teclados 4x4 para Arduino: las columnas tienen pull-up externo, la fila activa se conduce a `0`, y una tecla presionada hace que su columna se lea como `0`.

## Mapa del teclado

| Fila | Col 0 | Col 1 | Col 2 | Col 3 |
| ---- | ----- | ----- | ----- | ----- |
| 0    | 1     | 2     | 3     | A     |
| 1    | 4     | 5     | 6     | B     |
| 2    | 7     | 8     | 9     | C     |
| 3    | *     | 0     | #     | D     |

Las teclas `0`-`9` y `A`-`D` actualizan el codigo ingresado de 4 bits. La tecla `*` ejecuta `set_pass` usando el ultimo codigo ingresado. La tecla `#` ejecuta `enter` usando el ultimo codigo ingresado.

## Comportamiento

Despues de reset, la contrasena inicia en `0000`, el contador de intentos en cero y el candado queda bloqueado pero no en estado de bloqueo permanente. Un pulso `set_pass` desde `*` guarda una nueva contrasena si el diseno no esta bloqueado. Un pulso `enter` desde `#` compara el ultimo codigo ingresado con la contrasena guardada. Tres intentos fallidos activan `locked_out`; a partir de ese momento se ignoran nuevos intentos y cambios de contrasena hasta reset.

## Simulacion

No se ejecuta LibreLane en esta etapa. Para una simulacion rapida con Icarus Verilog, se puede usar:

```sh
iverilog -g2012 -o sim/tb_combolock.vvp test/tb_combolock.v src/*.v
vvp sim/tb_combolock.vvp
```
