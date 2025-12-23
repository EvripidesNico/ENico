`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/04/2022 03:20:42 PM
// Design Name: 
// Module Name: stateMachine
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments: want to parish
// 
//////////////////////////////////////////////////////////////////////////////////


module stateMachine(
    input clk,
    input go,
    input stop,
    input fourSec,
    input twoSec,
    input match,
    
    output showNub,
    output resetTime,
    output runGame,
    output scored,
    output flashBoth,
    output flashAlt,
    output sticky
    );
    
    wire [4:0] q;
    wire [4:0] d;
    
    SM_logic logic (.go(go), .stop(stop), .fourSec(fourSec), .twoSec(twoSec), .match(match), .showNub(showNub), .resetTime(resetTime), .runGame(runGame), .scored(scored),
                    .flashBoth(flashBoth), .flashAlt(flashAlt), .q(q), .d(d));
     FDRE #(.INIT(1'b1) ) sm0 (.C(clk), .CE(1'b1), .D(d[0]), .Q(q[0]));
     FDRE #(.INIT(1'b0) ) sm1 (.C(clk), .CE(1'b1), .D(d[1]), .Q(q[1]));
     FDRE #(.INIT(1'b0) ) sm2 (.C(clk), .CE(1'b1), .D(d[2]), .Q(q[2]));
     FDRE #(.INIT(1'b0) ) sm3 (.C(clk), .CE(1'b1), .D(d[3]), .Q(q[3]));
     FDRE #(.INIT(1'b0) ) sm4 (.C(clk), .CE(1'b1), .D(d[4]), .Q(q[4]));
     
     assign sticky = q[0];

endmodule


