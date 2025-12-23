/* 
 * File:   CAPTOUCH.c
 * Author: Bulls
 *
 * Created on February 5, 2024, 11:48 AM
 */

#include <stdio.h>
#include <stdlib.h>

#include "AD.h"
#include "BOARD.h"
#include "serial.h"
#include "timers.h"
#include "CAPTOUCH.h"

#define TOUCH PORTDbits.RD11
static int micro = 0;
static int Captouch = 0;
static int count = 0;
static int temp = 0;

char CAPTOUCH_Init(void) {
    // following block inits the timer
    T2CON = 0;
    T2CONbits.TCKPS = 0b011;
    PR2 = 0xFFFF;
    T2CONbits.ON = 1;

    //this block inits input capture
    IC4CON = 0;
    IC4CONbits.ICTMR = 1;
    IC4CONbits.ICM = 0b010;

    IFS0bits.IC4IF = 0;
    IPC4bits.IC4IP = 7;
    IEC0bits.IC4IE = 1;
    IC4CONbits.ON = 1;
    // whatever else you need to do to initialize your module
    TRISDbits.TRISD11 = 1;
    TIMERS_Init();
    //micro = IC4BUF;
    count = 0;
    //temp = IC4BUF;


}

void __ISR(_INPUT_CAPTURE_4_VECTOR) InputCapture_Handler(void) {
    IFS0bits.IC4IF = 0;
    // IC4BUF contains the timer value when the rising edge occurred.

    micro = temp;
    temp = IC4BUF;
    count = abs(temp - micro);



}


//char CAPTOUCH_Init(void);

char CAPTOUCH_IsTouched(void) {


    if (count > 400) {
        Captouch = 1;
    } else {
        Captouch = 0;
    }
    return Captouch;
}

int main(void) {
    BOARD_Init();
    CAPTOUCH_Init();
    int average = 0;
    while (1) {
        average = 0;
        for (int wait = 0; wait < 10000; wait++) {
            asm("NOP");
        }
            for (int num = 0; num < 50; num++) {
                average += CAPTOUCH_IsTouched();
            }
            average = average/50;
        printf("press:%d\n", average );
//                if(average == 1){
//                    printf("count:");
//                }
//                if(average != 1){
//                    printf("Not touch\n");
//                }
        //printf("count:%d\n", count);
    }
}

