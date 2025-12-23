`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/04/2022 10:48:40 PM
// Design Name: 
// Module Name: big_boy_clk
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


module big_boy_clk(
output reg out_clk,
input clk 
    );
always @(posedge clk)
begin
     out_clk <= ~out_clk;
end
endmodule
