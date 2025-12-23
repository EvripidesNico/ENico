`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: UCSC CSE100
// Engineer: Evripides Nicolaides
// 
// Create Date: 03/30/2022 05:51:01 PM
// Design Name: Simple Schematic
// Module Name: myAND
// Project Name: 
// Target Devices: basys3
// Tool Versions: 2019.1
// Description: A simple schematic using NOR, OR, and NOT logic, in order to turn on LEDs in the order of the logic table for each
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module myAND(
    //NOT bnt led 0 
    input btnC, //btn C 
    
    // Or A B for led C
    input A, //sw 0
    input B, //sw 1
    input B2, //sw2
    output D, // led 0
    output C, //led 1
    output E, //led 2
    output F  //led 3
    
    
    );
    assign D = ~btnC ;
    assign C = A | B ;
    assign E = A ^ B ;
    assign F = A | B | B2 ;
endmodule
