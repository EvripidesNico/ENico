`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/06/2022 06:12:26 PM
// Design Name: 
// Module Name: bitAdder
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


module bitAdder(
    input A,
    input B,
    input C_in,
    output C_out,
    output S
    );
    
    assign C_out = (A | B) | (A & B) & C_in ;
    assign S = A ^ B ^ C_in;
    
endmodule
