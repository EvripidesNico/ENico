`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:47:00 PM
// Design Name: 
// Module Name: synchronizer
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


module synchronizer(
    input [4:0] d,
    input clock,

    output [4:0] q
    );

    FDRE #(.INIT(1'b0) ) sync0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[0]), .Q(q[0]));
    FDRE #(.INIT(1'b0) ) sync1 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[1]), .Q(q[1]));
    FDRE #(.INIT(1'b0) ) sync2 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[2]), .Q(q[2]));
    FDRE #(.INIT(1'b0) ) sync3 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[3]), .Q(q[3]));
    FDRE #(.INIT(1'b0) ) sync4 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[4]), .Q(q[4]));
endmodule