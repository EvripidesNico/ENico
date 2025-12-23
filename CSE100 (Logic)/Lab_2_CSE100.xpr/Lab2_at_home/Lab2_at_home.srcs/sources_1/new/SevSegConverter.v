`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/06/2022 06:59:43 PM
// Design Name: 
// Module Name: SevSegConverter
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


module SevSegConverter(
    input n0,
    input n1,
    input n2,
    input n3,
    
    output seg0,
    output seg1,
    output seg2,
    output seg3,
    output seg4,
    output seg5,
    output seg6

    );
    assign seg0 = (n3 & n2 & !n1 & n0) | (!n3 & n2 & !n1 & !n0) | (n3 & !n2 & n1 & n0) | (!n3 & !n2 & !n1 & n0);
    assign seg1 = (!n3 & n2 & n1 & !n0) | (!n3 & n2 & !n1 & n0) | (n3 & n2 & !n1 & !n0) | (n3 & !n2 & n1 & n0) | (n3 & n2 & n1 & n0) | (n3 & n2 & n1 & !n0) ;
    assign seg2 = (n3 & n2 & !n1 & !n0) | (!n3 & !n2 & n1 & !n0)  | (n3 & n2 & n1 & n0) | (n3 & n2 & n1 & !n0);
    assign seg3 = (!n3 & n2 & !n1 & !n0) | (!n3 & n2 & n1 & n0) | (!n3 & !n2 & !n1 & n0) | (n3 & !n2 & n1 & !n0) | (n3 & !n2 & !n1 & n0) | (n3 & n2 & n1 & n0);
    assign seg4 = (!n3 & !n2 & !n1 & n0) | (n3 & !n2 & !n1 & n0) | (!n3 & n2 & !n1 & !n0) | (!n3 & n2 & !n1 & n0) | (!n3 & !n2 & n1 & n0) | (!n3 & n2 & n1 & n0);
    assign seg5 = (!n3 & !n2 & n1 & n0) | (!n3 & !n2 & !n1 & n0) | (n3 & n2 & !n1 & n0) | (!n3 & !n2 & n1 & !n0) | (!n3 & n2 & n1 & n0) ;
    assign seg6 =  (!n3 & !n2 & !n1 & n0) | (n3 & n2 & !n1 & !n0) | (!n3 & n2 & n1 & n0) | (!n3 & !n2 & !n1 & !n0) ;
    
endmodule
