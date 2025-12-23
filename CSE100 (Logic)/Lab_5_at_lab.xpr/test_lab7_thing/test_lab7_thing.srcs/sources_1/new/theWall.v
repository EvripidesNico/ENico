`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:52:18 PM
// Design Name: 
// Module Name: theWall
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


module theWall(
    input clock,
    input [10:0] Hpixel,
    input [10:0] Vpixel,

    output blue
    );

    wire top, right;
    //top wall
    assign top = (Vpixel >= 10'd0) && (Vpixel <= 10'd240);
    //bot wall
   // assign bot = (Vpixel >= 10'd472) && (Vpixel <= 10'd479);
    //left wall
   // assign left = (Hpixel >= 10'd0) && (Hpixel <= 10'd7);
    //right wall
    assign right = (Hpixel >= 10'd0) && (Hpixel <= 10'd639);

    assign blue = top | right;
endmodule
