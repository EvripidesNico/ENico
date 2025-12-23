`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:43:56 PM
// Design Name: 
// Module Name: selector
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


module selector(

    input [3:0] sel,
    input [15:0] N,
    output [3:0] H
    );


    //if sel 1000
    assign H[3:0] = (N[15:12] & {sel[3], sel[3], sel[3], sel[3]}) | 
            //sel 0100
                  (N[11:8] & {sel[2], sel[2], sel[2], sel[2]}) |
                  //sel 0010
                      (N[7:4] & {sel[1], sel[1], sel[1], sel[1]}) |
                      //sel 0001
                         (N[3:0] & {sel[0], sel[0], sel[0], sel[0]});
endmodule