###############################################################################
# Created by write_sdc
# Wed Nov 29 03:38:21 2023
###############################################################################
current_design sarlogic
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name clk -period 24.0000 
set_clock_uncertainty 0.2500 clk
set_clock_latency -source -min 4.6500 [get_clocks {clk}]
set_clock_latency -source -max 5.5700 [get_clocks {clk}]
###############################################################################
# Environment
###############################################################################
set_load -pin_load 0.1900 [get_ports {clkc}]
set_load -pin_load 0.1900 [get_ports {sample}]
set_load -pin_load 0.1900 [get_ports {valid}]
set_load -pin_load 0.1900 [get_ports {ctln[9]}]
set_load -pin_load 0.1900 [get_ports {ctln[8]}]
set_load -pin_load 0.1900 [get_ports {ctln[7]}]
set_load -pin_load 0.1900 [get_ports {ctln[6]}]
set_load -pin_load 0.1900 [get_ports {ctln[5]}]
set_load -pin_load 0.1900 [get_ports {ctln[4]}]
set_load -pin_load 0.1900 [get_ports {ctln[3]}]
set_load -pin_load 0.1900 [get_ports {ctln[2]}]
set_load -pin_load 0.1900 [get_ports {ctln[1]}]
set_load -pin_load 0.1900 [get_ports {ctln[0]}]
set_load -pin_load 0.1900 [get_ports {ctlp[9]}]
set_load -pin_load 0.1900 [get_ports {ctlp[8]}]
set_load -pin_load 0.1900 [get_ports {ctlp[7]}]
set_load -pin_load 0.1900 [get_ports {ctlp[6]}]
set_load -pin_load 0.1900 [get_ports {ctlp[5]}]
set_load -pin_load 0.1900 [get_ports {ctlp[4]}]
set_load -pin_load 0.1900 [get_ports {ctlp[3]}]
set_load -pin_load 0.1900 [get_ports {ctlp[2]}]
set_load -pin_load 0.1900 [get_ports {ctlp[1]}]
set_load -pin_load 0.1900 [get_ports {ctlp[0]}]
set_load -pin_load 0.1900 [get_ports {result[9]}]
set_load -pin_load 0.1900 [get_ports {result[8]}]
set_load -pin_load 0.1900 [get_ports {result[7]}]
set_load -pin_load 0.1900 [get_ports {result[6]}]
set_load -pin_load 0.1900 [get_ports {result[5]}]
set_load -pin_load 0.1900 [get_ports {result[4]}]
set_load -pin_load 0.1900 [get_ports {result[3]}]
set_load -pin_load 0.1900 [get_ports {result[2]}]
set_load -pin_load 0.1900 [get_ports {result[1]}]
set_load -pin_load 0.1900 [get_ports {result[0]}]
set_load -pin_load 0.1900 [get_ports {trim[4]}]
set_load -pin_load 0.1900 [get_ports {trim[3]}]
set_load -pin_load 0.1900 [get_ports {trim[2]}]
set_load -pin_load 0.1900 [get_ports {trim[1]}]
set_load -pin_load 0.1900 [get_ports {trim[0]}]
set_load -pin_load 0.1900 [get_ports {trimb[4]}]
set_load -pin_load 0.1900 [get_ports {trimb[3]}]
set_load -pin_load 0.1900 [get_ports {trimb[2]}]
set_load -pin_load 0.1900 [get_ports {trimb[1]}]
set_load -pin_load 0.1900 [get_ports {trimb[0]}]
set_timing_derate -early 0.9500
set_timing_derate -late 1.0500
###############################################################################
# Design Rules
###############################################################################
set_max_transition 3.0000 [current_design]
set_max_fanout 4.0000 [current_design]
