`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/23/2022 03:44:07 PM
// Design Name: 
// Module Name: toppo
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


module toppo(
    input clkin,
    input btnL,
    input btnR,
    input btnU,
    input btnD,
    input btnC,
    
    input [15:0] sw,
    
    output [3:0] vgaRed,
    output [3:0] vgaBlue,
    output [3:0] vgaGreen,
    output Hsync,
    output Vsync,
    output [15:0] led,
    
    //output oops,
    //output rgb_oops,
    
    output dp,
    output [3:0] an,
    output [6:0] seg
    
    );
    wire [10:0] Hpixel;
    wire [10:0] Vpixel;
    
    wire digsel;
    wire clk;
    lab7_clks not_so_slow (.clkin(clkin), .greset(sw[0]), .clk(clk), .digsel(digsel));
    
    //We've got to sync the Bismarck, cause the world depends on us
    wire [4:0] btnSync;
    synchronizer syncer (.clock(clk), .d({btnU, btnD, btnL, btnR, btnC}), .q(btnSync));
    
    //CRAWLING IN MY SKIN! THESE WOUNDS THEY WILL NOT HEAL!
    wire edgec, edgeu, edged, edgel, edger;
    edgeDetector edgyc (.clock(clk), .button(btnSync[0]), .signal(edgec));
    edgeDetector edgyu (.clock(clk), .button(btnSync[4]), .signal(edgeu));
    edgeDetector edgyd (.clock(clk), .button(btnSync[3]), .signal(edged));
    edgeDetector edgyl (.clock(clk), .button(btnSync[2]), .signal(edgel));
    edgeDetector edgyr (.clock(clk), .button(btnSync[1]), .signal(edger));
    //for testing
    //assign led [4:0] = btnSync [4:0];
    wire [3:0] red, blue, green;
    
    //Mine eyes have seen the glory
    VGA_Control stuffISee (.clock(clk), .vgaRed(red), .vgaBlue(blue), .vgaGreen(green),
                            .Hsync(Hsync), .Vsync(Vsync), .Hpixel(Hpixel), .Vpixel(Vpixel));
    //imagine not running at 60fps
    wire fps;
    assign fps = (Hpixel == 10'd799) && (Vpixel == 10'd524);
    wire fps2;
    assign fps2 = (Hpixel == 10'd798) && (Vpixel == 10'd524);
                            
    //The wall just got ten feet higher
    wire border;
    theWall trump (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .green(border));
    
    wire nobirds, timeup;
    wire win, starttime, runtime;
    
    //pray to RNGeesus
    wire [7:0] rngOut;
    randomNumGen rngMachine (.clock(clk), .reset(1'b0), .out(rngOut));
    
    //nothin' but net
    wire netblue, netgreen, netred, tagzone, idle, second;
    net catcher (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .Hstart(11'd300), .Vstart(11'd225),
                .size({sw[15], sw[14]}), .frame(fps), .start(edgec), .win(win), .btn(btnSync[4:1]), .idle(idle),
                .red(netred), .blue(netblue), .green(netgreen), .fun(led[15:12]), .tagzone(tagzone), .seconds(second));
    
    
    //A bird in the hand is worth two in the bush
    wire bird1red, bird1blue, bird1tag;
    birb bird1 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd200), .Vstart(11'd120), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[0], rngOut[1]}), .red(bird1red), .blue(bird1blue), .tagged(bird1tag));
            
    wire bird2red, bird2blue, bird2tag;
    birb bird2 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd100), .Vstart(11'd120), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[3], rngOut[4]}), .red(bird2red), .blue(bird2blue), .tagged(bird2tag));    
            
    wire bird3red, bird3blue, bird3tag;
    birb bird3 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd400), .Vstart(11'd120), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[6], rngOut[5]}), .red(bird3red), .blue(bird3blue), .tagged(bird3tag));
            
    wire bird4red, bird4blue, bird4tag;
    birb bird4 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd500), .Vstart(11'd130), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[5], rngOut[7]}), .red(bird4red), .blue(bird4blue), .tagged(bird4tag)); 
            
    wire bird5red, bird5blue, bird5tag;
    birb bird5 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd600), .Vstart(11'd220), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[2], rngOut[3]}), .red(bird5red), .blue(bird5blue), .tagged(bird5tag));      
                
    wire bird6red, bird6blue, bird6tag;
    birb bird6 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd200), .Vstart(11'd420), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[1], rngOut[7]}), .red(bird6red), .blue(bird6blue), .tagged(bird6tag));            
    
    wire bird7red, bird7blue, bird7tag;
    birb bird7 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd220), .Vstart(11'd320), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[6], rngOut[2]}), .red(bird7red), .blue(bird7blue), .tagged(bird7tag)); 
    
    wire bird8red, bird8blue, bird8tag;
    birb bird8 (.clock(clk), .Hpixel(Hpixel), .Vpixel(Vpixel), .frame({fps2, fps}), .start(edgec), .timeup(timeup),
             .Hstart(11'd120), .Vstart(11'd390), .win(win), .tagzone(tagzone), .idle(idle),
            .direction({rngOut[4], rngOut[2]}), .red(bird8red), .blue(bird8blue), .tagged(bird8tag)); 
    
                
    //l'etat c'est moi
    wire alltagged, loadtime;
    gameState funStates (.clock(clk), .btnC(edgec), .timeup(timeup), .tagged(~nobirds),
                 .alltagged(alltagged), .win(win), .starttime(starttime), .idle(idle),
                 .loadtime(loadtime), .runtime(runtime), .fun(led[3:0]));
     
    //EIGHT SECONDS HAVE PASSED WRRYYYYY
    wire [15:0] secondStuff;
    //wire second;
    countUD16L seconds (.clock(clk), .Up(fps), .Dw(1'b0), .LD(second), .d(16'h0000), .q(secondStuff));
    assign second = secondStuff[5] & secondStuff[4] & secondStuff[3] & secondStuff[2]; 
    wire [15:0] timeOut;
    countUD16L timer (.clock(clk), .Up(1'b0), .Dw(second & runtime), .LD(loadtime | (runtime & timeup)), 
                        .d({8'h00, sw[11:4]}), .q(timeOut), .dtc(timeup));
     assign led[11] = timeup;   
     assign led[10] = nobirds;
     assign led[8] = second; 
     assign led[7] = runtime;   
            
    //count the birds
    wire [4:0] taggedBirds;
    wire compressTag = bird1tag | bird2tag | bird3tag | bird4tag | bird5tag | bird6tag | bird7tag | bird8tag;
    countUD5L birdCounter (.clock(clk), .Up(compressTag), .Dw(1'b0), .LD(timeup | idle), .d(5'b0), .q(taggedBirds), .dtc(nobirds));
    assign alltagged = taggedBirds[3] & ~taggedBirds[2] & ~taggedBirds[1] & ~taggedBirds[0];
    assign led[9] = alltagged;   
    
    //display the number
    wire [3:0] ringOut;
    ringCounter ring (.clock(clk), .avanti(digsel), .out(ringOut));
    wire [3:0] selectOut;
    selector select (.sel(ringOut), .N({taggedBirds [3:0],4'h0, timeOut[7:0]}), .H(selectOut));
    sevenSeg display (.n(selectOut), .seg(seg));

    
    //vga         
    assign vgaRed = red & ({4{netred}} | {4{bird1red}} | {4{bird2red}} | {4{bird3red}}| {4{bird4red}}| 
                {4{bird5red}}| {4{bird6red}}| {4{bird7red}}| {4{bird8red}});
    assign vgaBlue = blue & ({4{netblue}} | {4{bird1blue}} | {4{bird2blue}} | {4{bird3blue}} | {4{bird4blue}} | 
                    {4{bird5blue}} | {4{bird6blue}} | {4{bird7blue}} | {4{bird8blue}});
    assign vgaGreen = green & ({4{border}} | {4{netgreen & ~nobirds}});
    
    //the numbers Mason, what do they mean?!
    assign dp = 1'b1;
    
    assign an[3] = ~(ringOut[3]);
    assign an[2] =  1'b1;
    assign an[1] = ~(ringOut[1] & ~idle);
    assign an[0] = ~(ringOut[0] & ~idle);
endmodule
