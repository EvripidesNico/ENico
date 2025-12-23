`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/27/2022 02:42:07 PM
// Design Name: 
// Module Name: Selector
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


module Selector(
    input [3:0] sel,
    input [15:0] N,
    output [3:0] H
    );
     // sel 1000 sel 0100  sel 0010 sel 0001
    assign H[3:0] = (N[15:12] & {sel[3], sel[3], sel[3], sel[3]}) | (N[11:8] & {sel[2], sel[2], sel[2], sel[2]}) | (N[7:4] & {sel[1], sel[1], sel[1], sel[1]}) | (N[3:0] & {sel[0], sel[0], sel[0], sel[0]});
endmodule
