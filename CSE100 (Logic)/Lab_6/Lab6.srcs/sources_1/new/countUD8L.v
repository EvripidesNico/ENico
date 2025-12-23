`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/11/2022 01:52:49 PM
// Design Name: 
// Module Name: countUD8L
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


module countUD8L(
input clock,
    input Up,
    input Dw,
    input LW,
    input [7:0] d,

    output [7:0] q,
    output utc,
    output dtc,
    output negative

    );

    //its half a 16-bit counter!
    wire utc0, dtc0;
    wire utc1, dtc1;
    countUD4L count0to3 (.Up(Up), .Dw(Dw), .LW(LW), .clk(clock), .d(d[3:0]), .q(q[3:0]), .UTC(utc0), .DTC(dtc0));
    countUD4L count4to7 (.Up(Up & utc0), .Dw(Dw & dtc0), .LW(LW), .clk(clock), .d(d[7:4]), .q(q[7:4]), .UTC(utc1), .DTC(dtc1));

    assign utc = utc0 & utc1;
    assign dtc = dtc0 & dtc1;
    //let's say value is negative if value is higher than 7F
   // assign negative = q[7];
endmodule