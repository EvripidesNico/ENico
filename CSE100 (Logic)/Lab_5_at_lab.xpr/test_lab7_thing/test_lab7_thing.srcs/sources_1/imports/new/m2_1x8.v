`timescale	1ns	/	1ps
//////////////////////////////////////////////////////////////////////////////////
//	Company:	
//	Engineer:	
//	
//	Create	Date:	04/13/2022	05:57:21	PM
//	Design	Name:	
//	Module	Name:	m2_1x8
//	Project	Name:	
//	Target	Devices:	
//	Tool	Versions:	
//	Description:	
//	
//	Dependencies:	
//	
//	Revision:
//	Revision	0.01	-	File	Created
//	Additional	Comments:
//	
//////////////////////////////////////////////////////////////////////////////////


module	m2_1x8(
    input [7:0] in0,
    input [7:0] in1,
    input sel,
    output [7:0] o
	);
	
	assign o[0] = (~sel & in0[0]) | (sel & in1[0]);
	assign o[1] = (~sel & in0[1]) | (sel & in1[1]);
	assign o[2] = (~sel & in0[2]) | (sel & in1[2]);
	assign o[3] = (~sel & in0[3]) | (sel & in1[3]);
	assign o[4] = (~sel & in0[4]) | (sel & in1[4]);
	assign o[5] = (~sel & in0[5]) | (sel & in1[5]);
	assign o[6] = (~sel & in0[6]) | (sel & in1[6]);
	assign o[7] = (~sel & in0[7]) | (sel & in1[7]); //not sure if i need this one but feels right :( 
	
				
endmodule
