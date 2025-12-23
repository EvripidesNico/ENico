`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:51:29 PM
// Design Name: 
// Module Name: countUD5L
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


module countUD5L(
    input clock,
    input Up,
    input Dw,
    input LD,
    input [4:0] d,

    output [4:0] q,
    output utc,
    output dtc

    );

    //utc is high if counterbits are all 1
    assign utc = q[4] & q[3] & q[2] & q[1] & q[0];
    //dtc is high if counterbits are all 0
    assign dtc = ~q[4] & ~q[3] & ~q[2] & ~q[1] & ~q[0];

    wire ce;
    wire up0, up1, up2, up3, up4;
    wire down1, down2, down3, down4;

    assign ce = (Up ^ Dw) | LD;
    //up count
    assign up0 = (q[0] ^ ce);
    assign up1 = q[1] ^ (ce & q[0]);
    assign up2 = q[2] ^ (ce & q[1] & q[0]);
    assign up3 = q[3] ^ (ce & q[2] & q[1] & q[0]);
    assign up4 = q[4] ^ (ce & q[3] & q[2] & q[1] & q[0]);

    //down count
    assign down1 = q[1] ^ (ce & ~q[0]);
    assign down2 = q[2] ^ (ce & ~q[1] & ~q[0]);
    assign down3 = q[3] ^ (ce & ~q[2] & ~q[1] & ~q[0]);
    assign down4 = q[4] ^ (ce & ~q[3] & ~q[2] & ~q[1] & ~q[0]);

    wire [4:0] out;
    assign out[4] = ((((up4 & Up & ~Dw) | (down4 & ~Up & Dw)) & ~LD) | (LD & d[4]));
    assign out[3] = ((((up3 & Up & ~Dw) | (down3 & ~Up & Dw)) & ~LD) | (LD & d[3]));
    assign out[2] = ((((up2 & Up & ~Dw) | (down2 & ~Up & Dw)) & ~LD) | (LD & d[2]));
    assign out[1] = ((((up1 & Up & ~Dw) | (down1 & ~Up & Dw)) & ~LD) | (LD & d[1]));
    assign out[0] = ((((up0 & Up & ~Dw) | (up0 & ~Up & Dw)) & ~LD) | (LD & d[0]));


    FDRE #(.INIT(1'b0) ) flip4 (.C(clock), .R(1'b0), .CE(ce), .D(out[4]), .Q(q[4]));
    FDRE #(.INIT(1'b0) ) flip3 (.C(clock), .R(1'b0), .CE(ce), .D(out[3]), .Q(q[3]));
    FDRE #(.INIT(1'b0) ) flip2 (.C(clock), .R(1'b0), .CE(ce), .D(out[2]), .Q(q[2]));
    FDRE #(.INIT(1'b0) ) flip1 (.C(clock), .R(1'b0), .CE(ce), .D(out[1]), .Q(q[1]));
    FDRE #(.INIT(1'b0) ) flip0 (.C(clock), .R(1'b0), .CE(ce), .D(out[0]), .Q(q[0]));

endmodule