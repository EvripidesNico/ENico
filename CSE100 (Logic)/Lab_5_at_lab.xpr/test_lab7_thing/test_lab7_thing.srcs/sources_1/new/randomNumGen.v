`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:36:22 PM
// Design Name: 
// Module Name: randomNumGen
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


module randomNumGen(
    input clock,
    input reset,

    output [7:0] out
    );
    //according to lab doc
    wire [7:0] rnd;
    wire d_in;

    assign d_in = rnd[0] ^ rnd[5] ^ rnd[6] ^ rnd[7];
    //flipflops
    FDRE #(.INIT(1'b1) ) rng1 (.C(clock), .CE(1'b1), .R(reset), .D(d_in), .Q(rnd[0]));
    FDRE #(.INIT(1'b0) ) rng2 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[0]), .Q(rnd[1]));
    FDRE #(.INIT(1'b0) ) rng3 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[1]), .Q(rnd[2]));
    FDRE #(.INIT(1'b0) ) rng4 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[2]), .Q(rnd[3]));
    FDRE #(.INIT(1'b0) ) rng5 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[3]), .Q(rnd[4]));
    FDRE #(.INIT(1'b0) ) rng6 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[4]), .Q(rnd[5]));
    FDRE #(.INIT(1'b0) ) rng7 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[5]), .Q(rnd[6]));
    FDRE #(.INIT(1'b0) ) rng8 (.C(clock), .CE(1'b1), .R(reset), .D(rnd[6]), .Q(rnd[7]));

    assign out[7:0] = {1'b0, rnd[6:0]}; //ignore top bit because sad

endmodule
