`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/11/2022 01:58:50 PM
// Design Name: 
// Module Name: topLevel
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


module topLevel(
  input clkin,
    input btnL,
    input btnR,
    input btnU,
    
    output led8,
    output led15,
    output dp,
    output [3:0] an,
    output [6:0] seg

    );
    //le clock
    wire clock, qsec, digsel, speed;
    lab6_clks mainClock (.clkin(clkin), .greset(btnSync[0]), .clk(clock), .digsel(digsel), .qsec(qsec), .fastclk(speed));
    //sync
    wire [2:0] btnSync;
    synchronizer sync (.d({btnL, btnR, btnU}), .clock(clock), .q(btnSync));
    
    //state machine
    wire leftLed, rightLed, showtime, reset, inc, dec;
    stateMachine funStates (.left(btnSync[2]), .right(btnSync[1]), .clock(clock), .leftLed(leftLed), .rightLed(rightLed), .showtime(showtime), .reset(reset), .inc(inc), .dec(dec));
    
    //8 bit counter!
    wire negative;
    wire [7:0] turkeyOut;
    countUD8L turkeyCount (.clock(clock), .Up(inc), .Dw(dec), .LW(1'b0), .d(8'h00), .q(turkeyOut)); //.negative(negative));
    
    //sign changer
    wire [7:0] display; 
   // signChanger flip (.sign(negative), .b(turkeyOut), .d(display));
    
    //quarter second counter
    wire [3:0] qring;
    Ring_Counter quarter (.clk(clock), .Adv(qsec), .out(qring));
    
    //timer!
    wire [3:0] timeOut;
    countUD4L timer (.clk(clock), .Up(qsec & qring[2]  & showtime), .Dw(1'b0), .LW(reset & showtime), .d(4'h0), .q(timeOut));
   
    //display logic
    wire [3:0] ringOut;
    Ring_Counter anodes (.clk(clock), .Adv(digsel), .out(ringOut));
    wire [3:0] selectOut;
    Selector select (.sel({ringOut[3], 1'b0, ringOut[1], ringOut[0]}), .N({timeOut, 4'h0, display}), .H(selectOut));
    
    wire [6:0] segOut;
    SevSeg segments (.n(selectOut), .seg(segOut));
    //negative sign logic
    wire [7:0] negsign;
    m2_1x8 negativeSign (.in0(segOut), .in1({1'b0, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1}), .sel(negative & ringOut[2]), .o(seg[6:0])); 
    //assign seg[6:0] = {6{negative}} & {6{selectOut[2]}} & ({1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b1, 1'b0});
    //anode stuff
    wire an3;
    assign an3 = showtime;//(showtime & ~timeOut[2]) | (showtime & timeOut[2] & (qring[1] | qring[2]));
    assign dp = 1'b1;
    
    assign an[3] = ~(ringOut[3] & an3);
    assign an[2] = ~(ringOut[2] & negative);
    assign an[1] = ~(ringOut[1]);
    assign an[0] = ~(ringOut[0]);
    
    //LEDS
    assign led8 = rightLed;
    assign led15 = leftLed;
    
    /*
    wire [15:0] display;
    assign display[7:0] = q;
    assign display[11:8] = TimeCount;
    assign display[15:12] = {1'b0, 1'b0, 1'b0, 1'b0};
    
    wire [3:0] sel;
    wire [3:0] h;
    wire [6:0] preseg;
    RingCounter ring (.adv(digsel), .clk(clock), .Q(sel));
    Selector select (.sel(sel), .N(display), .h(h));
    
    sevseg hex(.n(h) , .seg(preseg));
    
    assign an[0] = ~sel[0];
    assign an[1] = ~sel[1];
    assign an[3] = ~sel[2] | idle; /????
    assign an[2] = ~sel[3] | ~neg;
    
    assign seg[0] = ~an[2] &~preseg[0] | an[2] & preseg[0];
    assign seg[1] = ~an[2] &~preseg[1] | an[2] & preseg[1];
    assign seg[2] = ~an[2] &~preseg[2] | an[2] & preseg[2];
    assign seg[3] = ~an[2] &~preseg[3] | an[2] & preseg[3];
    assign seg[4] = ~an[2] &~preseg[4] | an[2] & preseg[4];
    assign seg[5] = ~an[2] &~preseg[5] | an[2] & preseg[5];
    assign seg[6] = ~an[2] &~preseg[6] | an[2] & preseg[6];
    
    
    */
    
endmodule
