`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:49:39 PM
// Design Name: 
// Module Name: countUD16L
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


module countUD16L(
    input clock,
    input Up,
    input Dw,
    input LD,
    input [15:0] d,

    output [15:0] q,
    output utc,
    output dtc

    );

    wire utc0, utc1, utc2, utc3;
    wire dtc0, dtc1, dtc2, dtc3;


    //assign the wires that will link the counters together
    /*
    assign utc0 = utcOut0 & Up;
    assign dtc0 = dtcOut0 & Dw;

    assign utc1 = utcOut1 & utcOut0 & Up;
    assign dtc1 = dtcOut1 & dtcOut0 & Dw;

    assign utc2 = utcOut2 & utcOut1 & utcOut0 & Up;
    assign dtc2 = dtcOut2 & dtcOut1 & dtcOut0 & Dw;
    */
    countUD3L count0to2 (.Up(Up), .Dw(Dw), .LD(LD), .clock(clock), .d(d[2:0]), .q(q[2:0]), .utc(utc0), .dtc(dtc0));
    countUD5L count3to7 (.Up(Up & utc0), .Dw(Dw & dtc0), .LD(LD), .clock(clock), .d(d[7:3]), .q(q[7:3]), .utc(utc1), .dtc(dtc1));
    countUD5L count8to12 (.Up(Up & utc0 & utc1), .Dw(Dw & dtc & dtc1), .LD(LD), .clock(clock), .d(d[12:8]), .q(q[12:8]), .utc(utc2), .dtc(dtc2));
    countUD3L count13to15 (.Up(Up & utc0 & utc1 & utc2), .Dw(Dw & dtc0 & dtc1 & dtc2), .LD(LD), .clock(clock), .d(d[15:13]), .q(q[15:13]), .utc(utc3), .dtc(dtc3));


    //utc is high if counterbits are all 1
    assign utc = utc3 & utc2 & utc1 & utc0;
    //dtc is high if counterbits are all 0
    assign dtc = dtc3 & dtc2 & dtc1 & dtc0;
endmodule