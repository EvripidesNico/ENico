`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/06/2022 05:27:02 PM
// Design Name: 
// Module Name: topmux
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


module topmux(
    input s0,
    input s1,
    input i0,
    input i1,
    input i2,
    input i3,
    output f
    );
    
    wire t0, t1;
    mux2to1 m1 (.s(s0), .i0(i0), .i1(i1), .y(t0));
    mux2to1 m2 (.s(s0), .i0(i2), .i1(i3), .y(t1));
    mux2to1 m3 (.s(s1), .i0(t0), .i1(t1), .y(f));
    
endmodule
