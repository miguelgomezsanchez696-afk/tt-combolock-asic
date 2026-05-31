TOPLEVEL_LANG := verilog
SIM ?= icarus

VERILOG_SOURCES := \
	$(abspath ../../src/tt_um_combolock.v) \
	$(abspath ../../src/keypad_scanner.v)

TOPLEVEL := tt_um_combolock
MODULE := test_combolock

include $(shell cocotb-config --makefiles)/Makefile.sim
