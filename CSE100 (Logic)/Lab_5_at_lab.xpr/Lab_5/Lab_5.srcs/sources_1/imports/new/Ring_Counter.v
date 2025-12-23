`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/27/2022 02:58:44 PM
// Design Name: 
// Module Name: Ring_Counter
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


module Ring_Counter(
    input clk,
    input Adv,
    output [3:0] out
    // this is here as an example to keep track of what goes into each slot
    //FDRE #(.INIT(1'b0)) Q0_FF (.C(clk), .CE(1'b1), .D(D[0]), .Q(Q[0]));

    );
    
    FDRE #(.INIT(1'b1)) count0 (.C(clk), .CE(Adv), .D(out[3]), .Q(out[0]));
    FDRE #(.INIT(1'b0)) count1 (.C(clk), .CE(Adv), .D(out[0]), .Q(out[1]));
    FDRE #(.INIT(1'b0)) count2 (.C(clk), .CE(Adv), .D(out[1]), .Q(out[2]));
    FDRE #(.INIT(1'b0)) count3 (.C(clk), .CE(Adv), .D(out[2]), .Q(out[3]));
endmodule
