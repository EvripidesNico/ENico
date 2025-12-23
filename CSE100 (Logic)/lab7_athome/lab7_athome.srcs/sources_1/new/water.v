`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 05:50:44 PM
// Design Name: 
// Module Name: water
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


module water(
//    input clock,
//    input [10:0] Hpixel,
//    input [10:0] Vpixel,

//    output blue
      input [10:0] Vpixel,
      output [3:0] water
    );

      wire [10:0] height;
      wire [3:0] dark;
      
      assign height = Vpixel - 11'd240;
      assign water[3:0] = Vpixel >= 11'd240 ? (4'hf - height[7:4]) : 4'b0;
      
//    assign blue = top | right | bot | left;

endmodule