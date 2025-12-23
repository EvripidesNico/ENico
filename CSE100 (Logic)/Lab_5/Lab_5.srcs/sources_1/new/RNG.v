`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/04/2022 02:31:09 PM
// Design Name: 
// Module Name: RNG
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


module RNG(
    input clk,
    
    output [7:0] Q
    );
    
    wire [7:0] rnd; //this is from the diagram given in the lab report
    wire D; //this is the input to all the flipflops
    
    //logic given from the lab manual
    assign D = rnd[0] ^ rnd[5] ^ rnd[6] ^ rnd[7];
    
    // all flipflops 7-0
     FDRE #(.INIT(1'b1) ) flip0 (.C(clk), .CE(1'b1), .D(D), .Q(rnd[0]));
     FDRE #(.INIT(1'b0) ) flip1 (.C(clk), .CE(1'b1), .D(rnd[0]), .Q(rnd[1]));
     FDRE #(.INIT(1'b0) ) flip2 (.C(clk), .CE(1'b1), .D(rnd[1]), .Q(rnd[2]));
     FDRE #(.INIT(1'b0) ) flip3 (.C(clk), .CE(1'b1), .D(rnd[2]), .Q(rnd[3]));
     FDRE #(.INIT(1'b0) ) flip4 (.C(clk), .CE(1'b1), .D(rnd[3]), .Q(rnd[4]));
     FDRE #(.INIT(1'b0) ) flip5 (.C(clk), .CE(1'b1), .D(rnd[4]), .Q(rnd[5]));
     FDRE #(.INIT(1'b0) ) flip6 (.C(clk), .CE(1'b1), .D(rnd[5]), .Q(rnd[6]));
     FDRE #(.INIT(1'b0) ) flip7 (.C(clk), .CE(1'b1), .D(rnd[6]), .Q(rnd[7]));
     
     // have to get rid of the last bit of rnd to assign to Q
     assign Q[7:0] = {1'b0,rnd[6:0]};
endmodule
