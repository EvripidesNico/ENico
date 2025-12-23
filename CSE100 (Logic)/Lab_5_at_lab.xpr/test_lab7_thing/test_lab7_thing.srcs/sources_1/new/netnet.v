`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:39:16 PM
// Design Name: 
// Module Name: netnet
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


module netnet(
    input clock,
    input [10:0] Hpixel,
    input [10:0] Vpixel,
    input seconds,
    input win,

    input [10:0] netposx,
    input [10:0] netposy,
    input [10:0] bigout,
    input [10:0] biggerout,
    //input [1:0] size,

    output blue,
    output green,
    output red,
    output tagzone //determines the area in which a bird can be tagged
    );


   wire bluezone;
   assign bluezone = (netposx <= Hpixel & Hpixel <= (netposx + 11'd31 + bigout + biggerout)) &
             netposy <= Vpixel & (Vpixel <= (netposy + 11'd31 + bigout + biggerout));
   wire greenzone;
   assign greenzone = (netposx + 11'd8 <= Hpixel & Hpixel <= (netposx + 11'd23 + bigout + biggerout)) &
             netposy + 11'd8 <= Vpixel & (Vpixel <= (netposy + 11'd23 + bigout + biggerout));
   wire redzone;
   assign redzone = (netposx + 11'd12 <= Hpixel & Hpixel <= (netposx + 11'd19 + bigout + biggerout)) &
             netposy + 11'd12 <= Vpixel & (Vpixel <= (netposy + 11'd19 + bigout + biggerout));

   wire [3:0] victory;
   ringCounter winner (.clock(clock), .avanti(seconds), .out(victory));

   assign blue = (~win & bluezone) | (win & (bluezone & victory[1] | (greenzone & victory[2]) | (redzone & victory[3])));
   assign green = (~win & greenzone) | (win & (bluezone & victory[0] | (greenzone & victory[1]) | (redzone & victory[2])));
   assign red = (win & (bluezone & victory[3] | (greenzone & victory[0]) | (redzone & victory[1])));

   assign tagzone = blue; //area of tagzone = blue area

endmodule