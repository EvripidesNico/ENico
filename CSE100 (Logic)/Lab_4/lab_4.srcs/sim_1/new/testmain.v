`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 04/27/2022 05:54:52 PM
// Design Name: 
// Module Name: testmain
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


module testmain();
    reg clkin;
    reg btnR;
    reg btnU;
    reg btnD;
    reg btnC;
    reg btnL;
    reg [15:0] sw;
    
    wire [6:0] seg;
    wire dp;
    wire [3:0] an;
    wire [15:0] led;
    
    Toplevel UUT(.clkin(clkin), .btnR(btnR), .btnU(btnU), .btnD(btnD), .btnC(btnC), .btnL(btnL), .sw(sw), .seg(seg), .dp(dp), .an(an), .led(led));
    
    parameter PERIOD = 10;
    parameter real DUTY_CYCLE = 0.5;
    parameter OFFSET = 2;

    initial    // Clock process for clkin
    begin
        #OFFSET
		  clkin = 1'b1;
        forever
        begin
            #(PERIOD-(PERIOD*DUTY_CYCLE)) clkin = ~clkin;
        end
    end
    
    initial
    begin
    //start all buttons at 0
    btnR = 1'b0;
    btnU = 1'b0;
    btnD = 1'b0;
    btnC = 1'b0;
    btnL = 1'b0;
    sw = 16'h0000;
    
    #1000 //time is 1000, clock starts
    btnD = 1'b1;
    //decrement 1 to FFFF
    #100 //time 1100
    
    btnD = 1'b0;
    #100 //time 1200
    
    btnU = 1'b1; //back to 0000
    #100 //time 1300
    
    btnU = 1'b0;
    #100 //time 1400
    //load a value
    sw = 16'ha21d;
    btnL = 1'b1;
    
    #100 //time 1500;
    btnL = 1'b0;
    
    #100 //time 1700
    btnC = 1'b1;
    //continuously count for a bit
    #500
    btnC = 1'b0;
    
    #100 
    btnU = 1'b1;
    btnD = 1'b1; 
    //nothing should happen!
    #300
    btnD = 1'b0;
    #100
    btnU = 1'b0;
    //nothing should happen here either!
    #100
    btnD = 1'b1;
    //now should count down by 1
    #100
    btnD = 1'b0;
    #100
    
    sw = 16'hfffa;
    btnL = 1'b1;
    #100 
    btnL = 1'b0;
    btnC = 1'b1;
    #500;
    btnC = 1'b0;
    //should have stopped at fffc
    
    
    end
endmodule