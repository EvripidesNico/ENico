`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:53:10 PM
// Design Name: 
// Module Name: birb
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


module birb(
    input clock,
    input [10:0] Hstart,
    input [10:0] Vstart,
    input [10:0] Hpixel,
    input [10:0] Vpixel,
    input [1:0] frame,
    input start,
    input timeup,
    input win,
    input idle,
    input tagzone,
    input [1:0] direction,
    
    //output [1:0] fun,
    output red,
    output blue,
    output tagged
    //output [10:0] Hpos,
    //output [10:0] Vpos
    );
    
    wire [4:0] d; //inputs for flipflops
    wire [4:0] q; //outputs for flipflops
    
    //flopflips
    FDRE #(.INIT(1'b1)) s0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[0]), .Q(q[0])); //start here
    FDRE #(.INIT(1'b0)) s1to4 [4:1] (.C({4{clock}}), .R({4{1'b0}}), .CE({4{1'b1}}), .D(d[4:1]), .Q(q[4:1]));
    
    //wall edges
    wire [10:0] Hleft, Hright;
    wire [10:0] Vtop, Vbot;
    wire [10:0] Hpos, Vpos;
    
    assign Hleft = 11'd8;
    assign Hright = 11'd615;
    assign Vtop = 11'd8;
    assign Vbot = 11'd455; 
    
    //statemachines
    //idle
    assign d[0] = (idle & (q[1] | q[2] | q[3] | q[4])) | (q[0] & ~start);
    //upleft
    assign d[1] = (q[0] & start & direction[1] & direction[0]) | (q[2] & (Hpos >= Hright) & (Vpos > Vtop)) | (q[3] & (Vpos >= Vbot) & (Hpos > Hleft)) |
                    (q[1] & (Hpos > Hleft) & (Vpos > Vtop) & ~idle) | (q[4] & Hpos >= Hright & Vpos >= Vbot);
    //upright
    assign d[2] = (q[0] & start & direction[1] & ~direction[0]) | (q[4] & (Vpos >= Vbot) & (Hpos < Hright)) | (q[1] & (Hpos <= Hleft) & (Vpos > Vtop)) |
                    (q[2] & (Hpos < Hright) & (Vpos > Vtop) & ~idle) | (q[3] & Hpos <= Hleft & Vpos >= Vbot); 
    //downleft
    assign d[3] = (q[0] & start & ~direction[1] & direction[0]) | (q[1] & (Vpos <= Vtop) & (Hpos > Hleft)) | (q[4] & (Hpos >= Hright) & (Vpos > Vtop)) |
                    (q[3] & (Hpos > Hleft) & (Vpos < Vbot) & ~idle) | (q[2] & Hpos >= Hright & Vpos <= Vtop);
    //downright
    assign d[4] = (q[0] & start & ~direction[1] & ~direction[0]) | (q[3] & (Hpos <= Hleft) & (Vpos < Vbot)) | (q[2] & (Vpos <= Vtop) & (Hpos < Hright)) |
                    (q[4] & (Hpos < Hright) & (Vpos < Vbot) & ~idle) | (q[1] & Hpos <= Hleft & Vpos <= Vtop);
    
    
    
    //output
    
    //assign red = q[0] | q[1] | q[2] | q[3] | q[4];
    //assign blue = 1'b0;
    
    wire [15:0] hin;
    wire [15:0] hout;
    wire [15:0] vin;
    wire [15:0] vout;
    
    assign hin [15:0] = {5'b0, Hstart};
    assign vin [15:0] = {5'b0, Vstart};
    
    countUD16L Horizontal (.clock(clock), .Up((frame[1] | frame[0]) & (q[2] | q[4])), .Dw((frame[1] | frame[0]) & (q[1] | q[3])), .LD((q[0] & start) | idle), .d(hin), .q(hout));
    countUD16L Vertical (.clock(clock), .Up((frame[1] | frame[0]) & (q[3] | q[4])), .Dw((frame[1] | frame[0]) & (q[1] | q[2])), .LD((q[0] & start) | idle), .d(vin), .q(vout));

    assign Hpos [10:0] = hout [10:0];
    assign Vpos [10:0] = vout [10:0];
    
    wire [10:0] hmux, vmux;
    m2_1x8 hchoose (.in0(Hstart), .in1(hout), .sel(~idle), .o(hmux));
    m2_1x8 vchoose (.in0(Vstart), .in1(vout), .sel(~idle), .o(vmux));
    
    
    wire redout, blueout;
    birb2 position (.clock(clock), .Hpixel(Hpixel), .Vpixel(Vpixel), .red(redout), .blue(blueout),
            .tagzone(tagzone), .birdposx(hmux), .birdposy(vmux), .timeup(timeup), 
            .tagged(tagged), .idle(idle));
    
    assign red = redout & (q[0] | q[1] | q[2] | q[3] | q[4]);
    assign blue = blueout & (q[0] | q[1] | q[2] | q[3] | q[4]);
    //assign fun [3:0]  =  {q[1], q[2], q[3], q[4]};
endmodule

