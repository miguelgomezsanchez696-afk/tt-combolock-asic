SIM_VVP := sim/tb_combolock.vvp
RUN_DIR ?= $(shell find runs -maxdepth 1 -type d -name 'RUN_*' | sort | tail -n 1)

.PHONY: sim cocotb flow reports clean

# RTL simulation with Icarus Verilog.
sim:
	mkdir -p sim
	iverilog -g2012 -o $(SIM_VVP) test/tb_combolock.v src/*.v
	vvp $(SIM_VVP)

# Cocotb keypad verification.
cocotb:
	make -C test/cocotb

# Local LibreLane hardening. Do not run this for documentation-only review.
flow:
	librelane config.json

# Export selected evidence from the latest local LibreLane run into reports/.
reports:
	@test -n "$(RUN_DIR)" || (echo "No LibreLane run found under runs/"; exit 1)
	@echo "Latest run: $(RUN_DIR)"
	@find $(RUN_DIR)/final -maxdepth 2 -type f | sort > reports/librelane_artifacts_list.txt
	@cp $(RUN_DIR)/final/metrics.json reports/final_metrics.json
	@cp $(RUN_DIR)/64-magic-drc/reports/drc_violations.magic.rpt reports/drc_violations.magic.rpt
	@cp $(RUN_DIR)/65-klayout-drc/reports/drc_violations.klayout.json reports/drc_violations.klayout.json
	@cp $(RUN_DIR)/70-netgen-lvs/reports/lvs.netgen.rpt reports/lvs.netgen.rpt
	@cp $(RUN_DIR)/47-openroad-checkantennas-1/reports/antenna.rpt reports/antenna.rpt
	@cp $(RUN_DIR)/76-misc-reportmanufacturability/manufacturability.rpt reports/manufacturability.rpt
	@cp $(RUN_DIR)/flow.log reports/flow.log

# Remove generated simulation artifacts only.
clean:
	$(RM) sim/tb_combolock.vvp sim/tb_combolock.vcd
