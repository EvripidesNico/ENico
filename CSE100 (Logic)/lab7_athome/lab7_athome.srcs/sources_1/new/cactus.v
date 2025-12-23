`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 08:26:21 PM
// Design Name: 
// Module Name: cactus
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


module cactus(
    input [10:0] Hpixel,
    input [10:0] Vpixel,
    input pause,
    input reset,
    input clk,
    input new_frame,
    input [15:0] defaultWhore, //i am in pain
    input [3:0] rng,
    
    output [3:0] cactus,
    output scored,
    output [15:0] xpos,
    output [10:0] ypos
    );
    wire [10:0] width, height;
    wire [10:0] startH, startV;
    wire [15:0] resetVal;
    wire [10:0] shift;
    wire [10:0] new_Vert;
    wire [10:0] resetV;
    
    assign resetVal = reset ? defaultWhore : 16'd681;
    assign width = 11'd40; //40
    assign height = 11'd96; //96
    //assign startV = 11'd240;
    
    assign shift = {rng[2:0], 2'b00}; //should be getting the value in multiples of 7
    
    assign new_Vert = rng[3] ? (11'd192 + shift) : (11'd192 - shift);
    

   
    wire [15:0] cactRight; //x position 
    
    //starts at 680 and goes to 0 
    countUD16L frogcount (.clk(clk), .Up(1'b0), .Dw(new_frame & ~pause), .LW((cactRight <= 16'd3) | reset), .d(resetVal), .q(cactRight)); 
         
   // assign resetV = reset ? 16'd240 : startV;
    
    assign startV = ((cactRight <= 16'd3)) ? new_Vert: startV; //11'd240   
    //assign startV = (cactRight <= 16'd3) ? new_Vert: resetV;
        
    assign cactus[3:0] = (Vpixel >= (startV)) & (Vpixel <= (startV + height)) & (Hpixel <= (cactRight)) & (Hpixel >= (cactRight - width) | (cactRight < 16'd40)) ? (4'hf) : 4'b0;
    
    assign scored = (cactRight == 16'd119) ? 1:0;
    
    assign xpos =cactRight;
    assign ypos = startV;
    
    /*
    
    Vpixel is going to be 3 postions determined from the random number
    3 horizontal postions 
        each horizontal postion while in the running state
        is going to decrament by 3 each frame
        gotta figure out a way to find out when a new postions starts and decrament the h postion when that happens 
        
        
        TODD BEST WAY 
            find out when Vpixel and Hpixel are 0 (make sure it does it once during one clk cycle, synchronize with clock somehow?)
            
            800 * 525 is one frame
    */
endmodule
