`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:43:02 PM
// Design Name: 
// Module Name: gameState
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


module gameState(
    input clock,
    input btnC,
    input timeup,
    input tagged,
    input alltagged,

    output [3:0] fun,

    output win,
    output loadtime,
    output starttime,
    output idle,
    output runtime
    );

    wire [3:0] d; //inputs for flipflops
    wire [3:0] q; //outputs for flipflops

    //flopflips
    FDRE #(.INIT(1'b1)) s0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[0]), .Q(q[0])); //start here
    FDRE #(.INIT(1'b0)) s1to3 [3:1] (.C({3{clock}}), .R({3{1'b0}}), .CE({3{1'b1}}), .D(d[3:1]), .Q(q[3:1]));

    //idle state
    assign d[0] = (q[3] & btnC) | (q[0] & ~btnC);
    //game running (none tagged)
    assign d[1] = (q[0] & btnC) | (q[1] & ~tagged) | (q[2] & timeup); 
    //game running (one+ tagged)
    assign d[2] = (q[1] & tagged & ~timeup) | (q[2] & (~timeup & ~alltagged));
    //win the game
    assign d[3] = (q[2] & alltagged & ~timeup) | (q[3] & ~btnC);

    //outputs
    assign win = q[3];
    assign runtime = q[2];
    assign starttime = q[1] & tagged & ~timeup;
    assign loadtime = q[1] | q[0];
    assign idle = q[0];

    assign fun = {q[0], q[1], q[2], q[3]};
endmodule
