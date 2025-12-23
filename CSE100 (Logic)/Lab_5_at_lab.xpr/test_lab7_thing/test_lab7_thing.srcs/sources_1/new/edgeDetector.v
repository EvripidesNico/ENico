`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:32:33 PM
// Design Name: 
// Module Name: edgeDetector
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module edgeDetector(
    input button,
    input clock,
    //input ce, //always running

    output signal

    );
    //generate a signal only if past two inputs are two zero's followed by a one
    wire q0, q1;

    //if button C is pressed, q0 -> 1, and then q1 -> 1;
    FDRE #(.INIT(1'b0) ) edge1 (.CE(1'b1), .C(clock), .R(), .D(button), .Q(q0));
    FDRE #(.INIT(1'b0) ) edge2 (.CE(1'b1), .C(clock), .R(), .D(q0), .Q(q1));
    //thus, if q0 is 0, and q1 is 1, then we should dget a high signal
    assign signal = button & ~q0 & ~q1;

endmodule