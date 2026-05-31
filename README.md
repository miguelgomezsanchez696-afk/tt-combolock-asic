# Combination Lock ASIC estilo TinyTapeout

Proyecto ASIC digital estilo TinyTapeout para un candado combinacional de 4 bits.

La diferencia principal respecto al diseno base es la entrada de usuario: este proyecto usa un teclado matricial 4x4 conectado a los pines bidireccionales `uio`, en vez de DIP switches.

## Estructura

- `src/tt_um_combolock.v`: RTL principal Verilog sintetizable.
- `src/keypad_scanner.v`: escaner sintetizable para teclado matricial 4x4.
- `test/tb_combolock.v`: testbench Verilog para simulacion funcional.
- `sim/`: scripts o resultados temporales de simulacion.
- `docs/`: documentacion del diseno.
- `reports/`: reportes de flujo fisico.
- `config.json`: configuracion inicial para LibreLane.
- `pin_order.cfg`: orden de pines top-level usado por LibreLane.

## Estado final de entrega

- Simulacion RTL con Icarus Verilog: PASS.
- Entrada por teclado matricial 4x4 usando `uio[3:0]` como filas y `uio[7:4]` como columnas.
- `pin_order.cfg` esta configurado en `config.json` mediante `IO_PIN_ORDER_CFG` para ubicar los pines top-level.
- LibreLane completo el flujo fisico en `runs/RUN_2026-05-31_02-03-14`.
- Signoff fisico: DRC Passed, LVS Passed, Antenna Passed y manufacturability Passed.

## Interfaz TinyTapeout

El modulo principal es `tt_um_combolock` y usa la interfaz TinyTapeout:

- `ui_in[7:0]`: no usados para la clave ni para comandos.
- `uo_out[0]`: `unlocked`, indica contrasena correcta.
- `uo_out[1]`: `locked_out`, indica bloqueo despues de 3 intentos fallidos.
- `uo_out[3:2]`: contador de intentos fallidos.
- `uo_out[7:4]`: contrasena almacenada, expuesta para depuracion/demo.
- `uio[3:0]`: filas del teclado, salidas desde el ASIC.
- `uio[7:4]`: columnas del teclado, entradas hacia el ASIC.
- `uio_oe`: `8'b0000_1111`.

El escaneo usa el cableado habitual de teclados 4x4 para Arduino: las columnas tienen pull-up externo, la fila activa se conduce a `0`, y una tecla presionada hace que su columna se lea como `0`.

## Mapa del teclado

| Fila | Col 0 | Col 1 | Col 2 | Col 3 |
| ---- | ----- | ----- | ----- | ----- |
| 0    | 1     | 2     | 3     | A     |
| 1    | 4     | 5     | 6     | B     |
| 2    | 7     | 8     | 9     | C     |
| 3    | *     | 0     | #     | D     |

Las teclas `0`-`9` y `A`-`D` cargan el codigo ingresado de 4 bits. La tecla `*` guarda la contrasena usando el ultimo codigo ingresado. La tecla `#` verifica la contrasena usando el ultimo codigo ingresado.

## Comportamiento

Despues de reset, la contrasena inicia en `0000`, el contador de intentos en cero y el candado queda bloqueado pero no en estado de bloqueo permanente. Un pulso `set_pass` desde `*` guarda una nueva contrasena si el diseno no esta bloqueado. Un pulso `enter` desde `#` compara el ultimo codigo ingresado con la contrasena guardada.

Despues de 3 intentos fallidos se activa `locked_out`; a partir de ese momento se ignoran nuevos intentos y cambios de contrasena hasta reset.

## Simulacion

Para reproducir la simulacion RTL con Icarus Verilog:

```sh
make sim
```

Comandos equivalentes:

```sh
iverilog -g2012 -o sim/tb_combolock.vvp test/tb_combolock.v src/*.v
vvp sim/tb_combolock.vvp
```

Resultado de simulacion: PASS.

GitHub Actions ejecuta esta misma verificacion con `make sim` en `.github/workflows/test.yml`. El workflow no ejecuta LibreLane/GDS por ahora porque requiere un entorno y PDK pesado; el flujo fisico se reproduce localmente con `make flow` o `PDK_ROOT=/tmp/librelane-pdks make flow`.

## Flujo fisico

El flujo fisico se reproduce con LibreLane usando `config.json`. Este comando genera una nueva corrida bajo `runs/`; no es necesario volver a ejecutarlo para revisar la entrega documentada.

```sh
make flow
```

Comando equivalente:

```sh
librelane config.json
```

Si LibreLane necesita una ruta explicita para el PDK:

```sh
PDK_ROOT=/tmp/librelane-pdks make flow
```

Resultado fisico documentado:

- LibreLane flow completed.
- DRC Passed.
- LVS Passed.
- Antenna Passed.
- manufacturability Passed.

`pin_order.cfg` se agrego para ubicar explicitamente los pines top-level. Sin este archivo, LibreLane no tenia una asignacion valida de ubicacion para los pines de la interfaz y el flujo fallaba durante placement. `config.json` referencia `pin_order.cfg` mediante `IO_PIN_ORDER_CFG`, por lo que el flujo usa ese archivo para solucionar el error de placement.

## Physical Verification

Para reproducir la simulacion RTL y el flujo fisico desde el repositorio:

```sh
make sim
make flow
```

Comandos equivalentes:

```sh
iverilog -g2012 -o sim/tb_combolock.vvp test/tb_combolock.v src/*.v
vvp sim/tb_combolock.vvp
librelane config.json
```

Si LibreLane no puede escribir el PDK en la ruta por defecto, usar:

```sh
PDK_ROOT=/tmp/librelane-pdks make flow
```

La corrida de verificacion fisica documentada es `runs/RUN_2026-05-31_02-03-14`. El flujo termino con DRC Passed, LVS Passed, Antenna Passed y manufacturability Passed. El tamano definido por `DIE_AREA` es `0 0 161 111`, equivalente a un bbox de 161 um x 111 um y un area de 17871 um^2, razonable para este macro digital pequeno estilo TinyTapeout.

`pin_order.cfg` se usa mediante `IO_PIN_ORDER_CFG` para fijar la ubicacion de los pines top-level y evitar el error de placement por pines sin ubicacion valida.

## Evidencia

La evidencia de simulacion y flujo fisico esta en `reports/`. Esta carpeta contiene reportes resumidos y logs clave exportados de la corrida documentada, sin incluir la carpeta completa `runs/`:

- `reports/rtl_simulation_pass.txt`: salida de simulacion RTL con `PASS`.
- `reports/flow_summary.md`: resumen final del run, comandos, resultados y tamano.
- `reports/flow_signoff_summary.txt`: lineas clave del log con DRC/LVS/Antenna/manufacturability.
- `reports/drc_violations.magic.rpt`: reporte Magic DRC con conteo cero.
- `reports/drc_violations.klayout.json`: reporte KLayout DRC exportado.
- `reports/manufacturability.rpt`: resumen final de Antenna/LVS/DRC.
- `reports/flow.log`: log principal de LibreLane para la corrida documentada.
- `reports/final_metrics.json`: metricas finales del flujo fisico.
- `reports/lvs.netgen.rpt`: reporte LVS.
- `reports/antenna.rpt`: reporte Antenna.
- `reports/runtime.txt`: tiempos de ejecucion.
- `reports/state_in.json` y `reports/state_out.json`: estados de entrada/salida del flujo.
- `reports/librelane_artifacts_list.txt`: lista de artefactos de la corrida LibreLane.
- `reports/config.json`: copia de configuracion usada para la corrida documentada.

## Archivos estilo TinyTapeout

- `info.yaml`: metadatos del proyecto, modulo top, fuentes, clock y pinout para revision estilo TinyTapeout.
- `docs/info.md`: descripcion corta para datasheet/documentacion.
- `.github/workflows/test.yml`: CI simple que instala Icarus Verilog y ejecuta `make sim`.
- `.gitignore`: ignora `runs/` para no subir corridas completas de LibreLane.
