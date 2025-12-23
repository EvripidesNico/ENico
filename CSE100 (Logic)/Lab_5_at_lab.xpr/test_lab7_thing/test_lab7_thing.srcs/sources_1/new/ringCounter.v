`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:40:04 PM
// Design Name: 
// Module Name: ringCounter
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


module ringCounter(

input clock,
input avanti, //avanti means advance in Italian
output [3:0] out
    );
    /*
    wire [3:0] loop;

    assign q[0] = loop[0];
    assign q[1] = loop[1];
    assign q[2] = loop[2];
    assign q[3] = loop[3]; 
    */
    //counts in a circle
    FDRE #(.INIT(1'b1) ) ring1 (.C(clock), .CE(avanti), .R(1'b0), .D(out[3]), .Q(out[0]));
    FDRE #(.INIT(1'b0) ) ring2 (.C(clock), .CE(avanti), .R(1'b0), .D(out[0]), .Q(out[1]));
    FDRE #(.INIT(1'b0) ) ring3 (.C(clock), .CE(avanti), .R(1'b0), .D(out[1]), .Q(out[2]));
    FDRE #(.INIT(1'b0) ) ring4 (.C(clock), .CE(avanti), .R(1'b0), .D(out[2]), .Q(out[3]));


endmodule