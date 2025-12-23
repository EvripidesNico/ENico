`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 07:56:13 PM
// Design Name: 
// Module Name: frog
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


module frog(
    input [10:0] Hpixel,
    input [10:0] Vpixel,
    input clk,
    input new_frame,
    input up,
    input down,
    input reset,

    output [15:0] position,
    output [3:0] frog
    );
    
    
    countUD16L frogcount (.clk(clk), .Up(down & new_frame), .Dw(up & new_frame), .LW(reset), .d(16'd232), .q(position));
    
    
    assign frog[3:0] = (Vpixel >= position) & (Vpixel <= (position + 11'd15)) & (Hpixel >= 11'd120) & (Hpixel <= 11'd135) ? (4'hf) : 4'b0;
    
    
    /*
    // first get the frog to be at 120, 232
    keep track of position of frog
    horizontal postion is not going to change = 120
    up three pixels per frame vertical
    output color rgb all three need to be true for it to be white which will be frog
    want it to be F when vpixel is between 232 and 247, and 120 to 135 hpixel 
    247 
    */
endmodule
