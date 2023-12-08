###############################################################################
# Created by write_sdc
# Fri Dec  8 03:38:08 2023
###############################################################################
current_design phase_inverter
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
set_load -pin_load 0.1900 [get_ports {output_signal_minus[9]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[8]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[7]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[6]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[5]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[4]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[3]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[2]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[1]}]
set_load -pin_load 0.1900 [get_ports {output_signal_minus[0]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[9]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[8]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[7]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[6]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[5]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[4]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[3]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[2]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[1]}]
set_load -pin_load 0.1900 [get_ports {output_signal_plus[0]}]
set_timing_derate -early 0.9500
set_timing_derate -late 1.0500
###############################################################################
# Design Rules
###############################################################################
set_max_transition 3.0000 [current_design]
set_max_fanout 4.0000 [current_design]
