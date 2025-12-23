`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:50:35 PM
// Design Name: 
// Module Name: countUD3L
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


module countUD3L(
    input clock,
    input Up,
    input Dw,
    input LD,
    input [2:0] d,

    output [2:0] q,
    output utc,
    output dtc

    );

    //utc is high if counterbits are all 1
    assign utc = q[2] & q[1] & q[0];
    //dtc is high if counterbits are all 0
    assign dtc = ~q[2] & ~q[1] & ~q[0];

    wire ce;
    wire up0, up1, up2;
    wire down1, down2;

    assign ce = (Up ^ Dw) | LD;
    //up count
    assign up0 = (q[0] ^ ce);
    assign up1 = q[1] ^ (ce & q[0]);
    assign up2 = q[2] ^ (ce & q[1] & q[0]);
    //down count
    assign down1 = q[1] ^ (ce & ~q[0]);
    assign down2 = q[2] ^ (ce & ~q[1] & ~q[0]);
    /*
    assign down1 = (ce * ~q[0] * ~q[1]) + (q[0]q[1]) + (q[1] ce);
    assign down2 = (~ce * q[2]) + (q[2] * q[0]) + (q[2] * q[1]) + (ce * ~q[2] * ~q[1] * ~q[0]);
    */

    wire [2:0] out;
    assign out[2] = ((((up2 & Up & ~Dw) | (down2 & ~Up & Dw)) & ~LD) | (LD & d[2]));
    assign out[1] = ((((up1 & Up & ~Dw) | (down1 & ~Up & Dw)) & ~LD) | (LD & d[1]));
    assign out[0] = ((((up0 & Up & ~Dw) | (up0 & ~Up & Dw)) & ~LD) | (LD & d[0]));

    FDRE #(.INIT(1'b0) ) flip2 (.C(clock), .R(1'b0), .CE(ce), .D(out[2]), .Q(q[2]));
    FDRE #(.INIT(1'b0) ) flip1 (.C(clock), .R(1'b0), .CE(ce), .D(out[1]), .Q(q[1]));
    FDRE #(.INIT(1'b0) ) flip0 (.C(clock), .R(1'b0), .CE(ce), .D(out[0]), .Q(q[0]));
endmodule