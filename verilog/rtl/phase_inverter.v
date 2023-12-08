`timescale 1ns/10ps

module phase_inverter (

    `ifdef USE_POWER_PINS
        inout vdd,
        inout vss,
    `endif

    input [9:0] input_signal,  // 10-bit input signal
    output [9:0] output_signal_plus,  // Output with the same phase as the input
    output [9:0] output_signal_minus  // Inverted output
);

    // Assign the input signal directly to the output
    // assign output_signal_plus = input_signal;

    // Generate the inverted output by inverting each bit of the input signal
    // assign output_signal_minus = ~input_signal;

    always @ (input_signal) begin
        #5 output_signal_plus = input_signal;            // 5 unit time delay
        #5 output_signal_minus = ~input_signal;  // 5 unit time delay
    end

endmodule

