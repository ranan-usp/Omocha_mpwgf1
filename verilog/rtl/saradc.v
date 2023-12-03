module saradc(
`ifdef USE_POWER_PINS
	inout vdd,
	inout vss,
`endif
	input vinp,
	input vinn,
	output [9:0] result,
	output valid,
	input cal,
	input en,
	input clk,
	input rstn
);
endmodule