`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 04:37:35 PM
// Design Name: 
// Module Name: net
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


module net(
    input clock,
    input [10:0] Hstart,
    input [10:0] Vstart,
    input [10:0] Hpixel,
    input [10:0] Vpixel,
    input [1:0] size,
    input [3:0] btn, //btnU, btnD, btnL, btnR
    input frame,
    input seconds,
    input idle,
    input start,
    input win,
    
    output [3:0] fun,
    output red,
    output blue,
    output green,
    output tagzone
    );
    
    //control the big size
    wire [10:0] bigout;
    wire [10:0] biggerout;
   
    m2_1x8 huge (.in0(11'b0), .in1(11'd64), .sel(size[0]), .o(bigout));
    m2_1x8 hugest (.in0(11'b0), .in1(11'd128), .sel(size[1]), .o(biggerout));
    
    wire [4:0] d; //inputs for flipflops
    wire [4:0] q; //outputs for flipflops
    //wire [2:0] d1, q1;
    //wire [2:0] d2, q2;
    
    //flopflips
    FDRE #(.INIT(1'b1)) s0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d[0]), .Q(q[0])); //start here
    FDRE #(.INIT(1'b0)) s1to4 [4:1] (.C({4{clock}}), .R({4{1'b0}}), .CE({4{1'b1}}), .D(d[4:1]), .Q(q[4:1]));
    /*
    FDRE #(.INIT(1'b1)) h0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d1[0]), .Q(q1[0])); //start here
    FDRE #(.INIT(1'b0)) h1to2 [2:1] (.C({2{clock}}), .R({2{1'b0}}), .CE({2{1'b1}}), .D(d1[2:1]), .Q(q1[2:1]));
    
    FDRE #(.INIT(1'b1)) v0 (.C(clock), .CE(1'b1), .R(1'b0), .D(d1[0]), .Q(q1[0])); //start here
    FDRE #(.INIT(1'b0)) v1to2 [2:1] (.C({2{clock}}), .R({2{1'b0}}), .CE({2{1'b1}}), .D(d2[2:1]), .Q(q2[2:1]));
    */
    //wall edges
    wire [10:0] Hleft, Hright;
    wire [10:0] Vtop, Vbot;
    wire [10:0] Hpos, Vpos;
    
    assign Hleft = 11'd7;
    assign Hright = (11'd601 - bigout - biggerout);
    assign Vtop = 11'd7;
    assign Vbot = (11'd441 - bigout - biggerout); 
    
    //state machine
    /*
    //HORIZONTAL 
    //idle
    assign d1[0] = (idle & ~q1[0]) | (q1[0] & ~start);
    //left
    assign d1[1] = (q1[0] & start) | (q1[2] & Hright >= Hpos) | (q1[2] & btn[1]) | (q1[1] & Hleft < Hpos & ~btn[0]);
    //right
    assign d1[2] = (q1[1] & Hleft <= Hpos) | (q1[1] & btn[0]) | (q1[2] & Hright > Hpos & ~btn[1]);
    
    //VERTICAL
    //idle
    assign d2[0] = (idle & ~q2[0]) | (q2[0] & ~start);
    //up
    assign d2[1] = (q2[0] & start) | (q2[2] & Vbot >= Vpos) | (q2[2] & btn[2]) | (q2[1] & Vtop < Vpos & ~btn[2]);
    //down
    assign d2[2] = (q2[1] & Vtop <= Vpos) | (q2[1] & btn[3]) | (q2[2] & Vbot > Vpos & ~btn[3]);
    */
    //idle
    assign d[0] = (idle & ~q[0]) | (q[0] & ~start);
    //up left
    assign d[1] = (q[0] & start) | (q[2] & (Hpos >= Hright) & (Vpos > Vtop)) | (q[3] & (Vpos >= Vbot) & (Hpos > Hleft)) |
                    (q[1] & ~idle & (Hpos > Hleft) & (Vpos > Vtop) & (~btn[2] & ~btn[0])) | (q[4] & (Hpos >= Hright & Vpos >= Vbot))
                    | (q[2] & btn[1]) | (q[3] & btn[3]) /* | (q[1] & (Hpos == Hright & Vpos == Vbot) */;
    //up right
    assign d[2] = (q[4] & (Vpos >= Vbot) & (Hpos < Hright)) | (q[1] & (Hpos <= Hleft) & (Vpos > Vtop)) |
                    (q[2] & ~idle & (Hpos < Hright) & (Vpos > Vtop) & (~btn[2] & ~btn[1])) | (q[3] & (Hpos <= Hleft & Vpos >= Vbot))
                    | (q[1] & btn[0]) | (q[4] & btn[3]); 
    
    //down left
    assign d[3] = (q[1] & (Vpos <= Vtop) & (Hpos > Hleft)) | (q[4] & (Hpos >= Hright) & (Vpos < Vbot)) |
                    (q[3] & ~idle & (Hpos > Hleft) & (Vpos < Vbot) & (~btn[3] & ~btn[0])) | (q[2] & (Hpos >= Hright & Vpos <= Vtop))
                    | (q[1] & btn[2]) | (q[4] & btn[1]);
    
    //down right
    assign d[4] = (q[3] & (Hpos <= Hleft) & (Vpos < Vbot)) | (q[2] & (Vpos <= Vtop) & (Hpos < Hright)) |
                    (q[4] & ~idle & (Hpos < Hright) & (Vpos < Vbot) & (~btn[3] & ~btn[1])) | (q[1] & (Hpos <= Hleft & Vpos <= Vtop))
                    | (q[2] & btn[2]) | (q[3] & btn[0]);
    
    //counter stuff
    wire [15:0] hout, vout;
    wire [15:0] hin, vin;
    
    assign hin [15:0] = {5'b0, Hstart};
    assign vin [15:0] = {5'b0, Vstart};
    
    countUD16L Horizontal (.clock(clock), .Up((Hright > Hpos) & ~win & ~idle & frame & (q[2] | q[4])), .Dw((Hleft < Hpos) & ~idle & ~win & frame & (q[1] | q[3])), .LD((start & q[0]) | idle), .d(hin), .q(hout));
    countUD16L Vertical (.clock(clock), .Up((Vpos < Vbot) & ~win & ~idle & frame & (q[3] | q[4])), .Dw((Vpos > Vtop) & ~idle & ~win & frame & (q[1] | q[2])), .LD((start & q[0])  | idle), .d(vin), .q(vout));
    //countUD16L Horizontal (.clock(clock), .Up(~win & ~idle & frame & q1[1]), .Dw(~idle & ~win & frame & q1[2]), .LD((start & q1[0]) | idle), .d(hin), .q(hout));
    //countUD16L Vertical (.clock(clock), .Up(~win & ~idle & frame & q2[2]), .Dw(~idle & ~win & frame & q2[1]), .LD((start & q2[0])  | idle), .d(vin), .q(vout));
    
    assign Hpos [10:0] = hout [10:0];
    assign Vpos [10:0] = vout [10:0];
    
    wire [10:0] hmux, vmux;
    m2_1x8 hchoose (.in0(Hstart), .in1(hout), .sel(~idle), .o(hmux));
    m2_1x8 vchoose (.in0(Vstart), .in1(vout), .sel(~idle), .o(vmux));
    
    wire blueout, greenout, redout;
    netnet position (.clock(clock), .Hpixel(Hpixel), .Vpixel(Vpixel), .netposx(hmux), .netposy(vmux), .win(win),
                    .bigout(bigout), .biggerout(biggerout), .blue(blueout), .seconds(seconds),
                    .green(greenout), .red(redout), .tagzone());
                    
    assign blue = blueout;
    assign red = redout;
    assign green = greenout;
    assign tagzone = blueout;
    
    assign fun [3:0] = {q[1] , q[2] , q[3] , q[4]};
    //assign fun [3:0] = {q1[1], q1[2], q2[1], q2[2]};
endmodule