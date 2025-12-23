`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/27/2022 03:07:33 PM
// Design Name: 
// Module Name: Edge_detect
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


module Edge_detect(
    input btn,
    input clk,
    output s

    );
    
    wire [1:0] q;
    //if q0 is 0 and q1 is 1 while btn is pressed then the signal will be high for one cycle
    FDRE #(.INIT(1'b0)) e0 (.CE(1'b1), .C(clk) , .D(btn), .Q(q[0]));
    FDRE #(.INIT(1'b0) ) e1 (.CE(1'b1), .C(clk), .D(q[0]), .Q(q[1]));
    // btn high with both q0 q1 being low will be true for s
    assign s = btn & ~q[0] & ~q[1];
endmodule
