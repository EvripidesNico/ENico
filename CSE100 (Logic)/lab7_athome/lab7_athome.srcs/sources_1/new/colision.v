`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/25/2022 07:25:08 PM
// Design Name: 
// Module Name: colision
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


module col(
    input [15:0] frogpos,
    input [15:0] x1,
    input [15:0] x2,
    input [15:0] x3,
    input [10:0] y1,
    input [10:0] y2,
    input [10:0] y3,
    
    output colision

    );
    wire colision1, colision2, colision3;
    
    assign colision1 = (x1 - 16'd40 <= 16'd136) & (x1 >= 16'd120) & (frogpos + 16'd16 >=y1) & (frogpos <= y1+ 16'd96);
    
    assign colision2 = (x2 - 16'd40 <= 16'd136) & (x2 >= 16'd120) & (frogpos + 16'd16 >=y2) & (frogpos <= y2+ 16'd96);
    
    assign colision3 = (x3 - 16'd40 <= 16'd136) & (x3 >= 16'd120) & (frogpos + 16'd16 >=y3) & (frogpos <= y3+ 16'd96);
    
    assign colision = colision1 | colision2 | colision3; 
    
endmodule
