`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/27/2022 03:42:16 PM
// Design Name: 
// Module Name: Toplevel
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


module Toplevel(
    input clkin,
    input btnR,
    input btnU,
    input btnD,
    input btnC,
    input btnL,
    input [15:0] sw,
    
    output [6:0] seg,
    output dp,
    output [3:0] an,
    output [15:0] led

    );
    
  //  assign led = sw; //they the same pretty sure 
    
    wire clk;
    wire digsel;
    //clk lab4
    lab4_clks slowit (.clkin(clkin), .greset(btnR), .clk(clk), .digsel(digsel));
    
    //assigning edge dector
    wire eUp, eDown;
    Edge_detect down (.btn(btnD), .clk(clk), .s(eDown));
    Edge_detect up (.btn(btnU), .clk(clk), .s(eUp));
   
    //so we don't count from FFFC - FFFF
    wire count;
    wire [15:0] qOut;

    assign count = btnC & (~qOut[15] | ~qOut[14] | ~qOut[13] | ~qOut[12] | ~qOut[11] | ~qOut[10] | ~qOut[9] 
                        | ~qOut[8] | ~qOut[7] | ~qOut[6] | ~qOut[5] | ~qOut[4] | ~qOut[3] | ~qOut[2]);
                        
    // 16 bit counter implementaion 
    wire UTC, DTC;
    wire upIn;
    assign upIn = count | eUp;
    countUD16L bit16 (.clk(clk), .Up(upIn), .Dw(eDown), .LW(btnL), .d(sw), .q(qOut), .UTC(UTC), .DTC(DTC));
    
    //ring counter
    wire [3:0] Rout;
    Ring_Counter Rcounter (.clk(clk), .Adv(digsel), .out(Rout));
    
    //seven seg
    wire [3:0] sevin;
    Selector sevInseg (.sel(Rout), .N(qOut), .H(sevin));
    SevSeg display (.n(sevin), .seg(seg));
    
    //active low an so 0 makes it turn on
    assign an = ~Rout;
    assign dp = (~(DTC & Rout[0])) & (~(UTC & Rout[3]));
    
    //test for simulation
    assign led[15] = UTC;
    assign led[0] = DTC;
    
endmodule
