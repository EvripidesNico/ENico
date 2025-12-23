`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/04/2022 10:02:13 PM
// Design Name: 
// Module Name: SM_logic
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


module SM_logic(
    input go,
    input stop,
    input fourSec,
    input twoSec,
    input match,
    input [4:0] q,
    
    output showNub,
    output resetTime,
    output runGame,
    output scored,
    output flashBoth,
    output flashAlt,
    output [4:0] d
    );
    
    //logic bs for the statemachine
    assign showNub = (~q[0]);
    assign resetTime = stop | go;//(q[0] | q[2]);
    assign runGame = (q[2]);
    assign scored = (q[3]);
    assign flashBoth = (q[3]);
    assign flashAlt = (q[4]);
    assign d[0] = ((q[0] & (~go)) | (q[3] & fourSec) | (q[4] & fourSec));
    assign d[1] = ((q[0] & go) | (q[1] & (~twoSec)));
    assign d[2] = ((q[1] & twoSec) |( q[2] & (~stop)));
    assign d[3] = ((q[2] & stop & match) | (q[3] & (~fourSec)));
    assign d[4] = ((q[2] & stop & (~match)) |(q[4] & (~fourSec)));
    
endmodule
