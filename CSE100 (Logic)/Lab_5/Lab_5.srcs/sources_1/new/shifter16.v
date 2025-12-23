`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/04/2022 03:42:37 PM
// Design Name: 
// Module Name: shifter16
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


module shifter16(
    input clk, in,
    output [15:0] out
    );
    
    wire [15:0] carry;
    // Offset the output bits by one position, then AND with the input signal.
    // Thereby, every next bit requires the previous bit to have been HIGH before it.
    assign carry = {out[14:0], 1'b1} & {16{in}};
    
    FDRE #(.INIT(1'b0)) ff[15:0] (.C({16{clk}}), .CE({16{in}}), .D(carry), .Q(out));
    
endmodule