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
    input clk, 
    input adv,
    output [15:0] out
    );
    
    wire [15:0] hold;
    
    assign hold = {out[14:0], 1'b1} & {16{adv}};
    
    FDRE #(.INIT(1'b0)) shift[15:0] (.C({16{clk}}), .CE({16{adv}}), .D(hold), .Q(out));
    
endmodule