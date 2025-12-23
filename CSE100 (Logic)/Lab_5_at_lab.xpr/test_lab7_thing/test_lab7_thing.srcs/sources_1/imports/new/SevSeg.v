`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/13/2022 07:06:00 PM
// Design Name: 
// Module Name: SevSeg
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


module sevenSeg(
    input [3:0] n,
    output [6:0] seg
    
    );
    wire knot;
    assign knot = ~n[0];
    m8_1 A( .in({1'b0,n[0],n[0],1'b0,1'b0,~n[0],1'b0,n[0]}), .sel(n[3:1]), .o(seg[0]));
    m8_1 B( .in({1'b1,~n[0],n[0],1'b0,~n[0],n[0],1'b0,1'b0}), .sel(n[3:1]), .o(seg[1]));
    m8_1 C( .in({1'b1,~n[0],1'b0,1'b0,1'b0,1'b0,~n[0],1'b0}), .sel(n[3:1]), .o(seg[2]));
    m8_1 D( .in({n[0],1'b0,~n[0],n[0],n[0],~n[0],1'b0,n[0]}), .sel(n[3:1]), .o(seg[3]));
    m8_1 E( .in({1'b0,1'b0,1'b0,n[0],n[0],1'b1,n[0],n[0]}), .sel(n[3:1]), .o(seg[4]));
    m8_1 F( .in({1'b0,n[0],1'b0,1'b0,n[0],1'b0,1'b1,n[0]}), .sel(n[3:1]), .o(seg[5]));
    m8_1 G( .in({1'b0,~n[0],1'b0,1'b0,n[0],1'b0,1'b0,1'b1}), .sel(n[3:1]),  .o(seg[6])); 
    
endmodule
