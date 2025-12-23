`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/06/2022 07:31:01 PM
// Design Name: 
// Module Name: mainAdder
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


module mainAdder(
    input sw0, //cin
    input sw1, //a 1-3 
    input sw2,
    input sw3,
    input sw4, //b 1- 3
    input sw5,
    input sw6,
    
    //seven seg display output
    output Ca,
    output Cb,
    output Cc,
    output Cd,
    output Ce,
    output Cf,
    output Cg,
    
    output AN0,
    output AN1,
    output AN2,
    output AN3,
    output DP
    );
    //wires for sums
    wire w0, w1, w2, w3;
    FullAdder t1 ( .a0(sw1), .a1(sw2), .a2(sw3), .b0(sw4), .b1(sw5), .b2(sw6), .cin(sw0), . s0(w0), .s1(w1), .s2(w2), .s3(w3));
    
    SevSegConverter t2 ( .n0(w0), .n1(w1), .n2(w2), .n3(w3), .seg0(Ca), .seg1(Cb), .seg2(Cc), .seg3(Cd), .seg4(Ce), .seg5(Cf), .seg6(Cg));
    
    assign DP = 1;
    assign AN0 = 0;
    assign AN1 = 1;
    assign AN2 = 1;
    assign AN3 = 1;
endmodule
