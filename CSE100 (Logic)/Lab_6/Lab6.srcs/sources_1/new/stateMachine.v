`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/11/2022 01:57:25 PM
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
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module stateMachine(
    input left,
    input right,
    input clock,

    //output [6:0] test,

    output leftLed,
    output rightLed,
    output showtime,
    output reset, //reset timer
    output inc,
    output dec
    );
    wire [6:0] d; //inputs for flipflops
    wire [6:0] q; //outputs for flipflops

    //flopflips
    FDRE #(.INIT(1'b1)) s0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[0]), .Q(q[0])); //start here
    FDRE #(.INIT(1'b0)) s12345[6:1] (.C({6{clock}}), .R({6{1'b0}}), .CE({6{1'b1}}), .D(d[6:1]), .Q(q[6:1]));

    //one-hot logic
    //idle state
    assign d[0] = (q[5] & !right) | (q[6] & !left) | (q[0] & ~(left | right)) | ((q[3] || q[4]) & (~left & ~right))
                    | (q[1] & !left) | (q[2] & !right);
    //left first
    assign d[1] = (q[0] & left) | (q[3] & !right) | (q[1] & left & !right);
    //right first
    assign d[2] = (q[0] & right) | (q[4] & !left) | (q[2] & right & !left);
    //both, but left first
    assign d[3] = (q[1] & right) | (q[5] & left) | (q[3] & left & right);
    //both, but right first
    assign d[4] = (q[2] & left) | (q[6] & right) | (q[4] & left & right);
    //enter left, only right
    assign d[5] = (q[3] & !left) | (q[5] & right & !left);
    //enter right, only left
    assign d[6] = (q[4] & !right) | (q[6] & left & !right);

    //assign test[6:0] = q[6:0];

    //outputs
    //left sensor
    assign leftLed = q[0] | q[2] | q[5];
    //right sensor
    assign rightLed = q[0] | q[1] | q[6];
    //to show time
    assign showtime = ~q[0];
    //count up
    assign inc = q[6] & ~left;
    //count down
    assign dec = q[5] & ~right;
    //reset the timer...
    assign reset = (q[5] & !right) | (q[6] & !left) | (q[0] & left) | (q[3] & !right) | (q[0] & right) | (q[4] & !left)
                    | (q[1] & right) | (q[5] & left) | (q[2] & left) | (q[6] & right) | (q[3] & !left) 
                    | (q[4] & !right) | (q[1] & !left) | (q[2] & !right);

endmodule