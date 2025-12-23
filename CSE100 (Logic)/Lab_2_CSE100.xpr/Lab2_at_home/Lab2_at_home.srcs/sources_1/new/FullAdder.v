`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/06/2022 06:23:26 PM
// Design Name: 
// Module Name: FullAdder
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


module FullAdder(
    input a0,
    input a1,
    input a2,
    input b0,
    input b1,
    input b2,
    input cin,
    output s0,
    output s1,
    output s2,
    output s3 //this is our final c out

    );
    wire c1, c2;
    
    bitAdder m1 ( .A(a0), .B(b0), .C_in(cin), .C_out(c1), .S(s0));
    bitAdder m2 ( .A(a1), .B(b1), .C_in(c1), .C_out(c2), .S(s1));
    bitAdder m3 ( .A(a2), .B(b2), .C_in(c2), .C_out(s3), .S(s2));
    
endmodule
