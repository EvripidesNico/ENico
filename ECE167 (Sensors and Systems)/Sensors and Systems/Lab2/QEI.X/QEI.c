/* 
 * File:   QEI.c
 * Author: Bulls
 *
 * Created on January 29, 2024, 2:04 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include "AD.h"
#include "Ascii.h"
#include "BOARD.h"
#include "pwm.h"
#include "QEI.h"
#include "serial.h"

//defining each RGB port
#define RED PWM_PORTZ06
#define GREEN PWM_PORTY12
#define BLUE  PWM_PORTY10

//State machine states for encoder

enum states {
    up, right, down, left
};
enum states state;
volatile int count = 0;
volatile int rot = 0;

/*
 * 
 */
char QEI_Init(void) {
    CNCONbits.ON = 1; // Change Notify On
    CNENbits.CNEN15 = 1; //enable one phase
    CNENbits.CNEN16 = 1; //enable other phase
    int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
    IFS1bits.CNIF = 0; // clear interrupt flag
    IPC6bits.CNIP = 1; //set priority
    IPC6bits.CNIS = 3; // and sub priority
    IEC1bits.CNIE = 1; // enable change notify

    // the rest of the function goes here
    state = up; //init state
    count = 0;
    rot = 0;
}

void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
    static char readPort = 0;
    readPort = PORTD; // this read is required to make the interrupt work
    IFS1bits.CNIF = 0;
    int A = PORTDbits.RD6;
    int B = PORTDbits.RD7; //read bits from these ports

    //encoder angle generation SM
    switch (state) {
        case up: //if up go left if A changes go right if B changes
            QEI_GetPosition();
            if (A == 1 && B == 0) {
                state = left;
                count -= 1;
            }
            if (B == 1 && A == 0) {
                state = right;
                count += 1;
            }

            //            printf("%d\n", count);
            //            printf("rot %d\n", rot);
            break;

        case down: //if down go left if B changes go right if A changes
            if (B == 0 && A == 1) {
                state = left;
                count += 1;
            }
            if (A == 0 && B == 1) {
                state = right;
                count -= 1;
            }
            break;
        case left: //if left go up if A changes go down if B changes
            if (A == 0 && B == 0) {
                state = up;
                count += 1;
                if ((count % 4) == 0) { //check for count being a full rotation
                    //count = 0;
                    rot += 15;
                }
            }
            if (B == 1 && A == 1) {
                state = down;
                count -= 1;
            }

            break;
        case right: //if right go down if B changes go up if A changes
            if (A == 1 && B == 1) {
                state = down;
                count += 1;
            }
            if (B == 0 && A == 0) {
                state = up;
                count -= 1;
                if ((count % 4) == 0) {
                    //count = 0;
                    rot -= 15;
                }
            }
            printf("%d\n", count);  
            QEI_GetPosition();
            break;

    }
}

int QEI_GetPosition(void) {
    //set color to red
    if (abs(count % 96) > 0 && abs(count % 96) < 12) {
        PWM_SetDutyCycle(RED, 1000);
        PWM_SetDutyCycle(BLUE, 1000);
        PWM_SetDutyCycle(GREEN, 1000);
    }
    //set color to light purple
    if (abs(count % 96) > 12 && abs(count % 96) < 24) {
        PWM_SetDutyCycle(RED, 1000);
        PWM_SetDutyCycle(BLUE, 500);
        PWM_SetDutyCycle(GREEN, 500);
    }
    //set color to purple
    if (abs(count % 96) > 24 && abs(count % 96) < 36) {
        PWM_SetDutyCycle(RED, 1000);
        PWM_SetDutyCycle(BLUE, 0);
        PWM_SetDutyCycle(GREEN, 0);
    }
    //set color to light blue
    if (abs(count % 96) > 36 && abs(count % 96) < 48) {
        PWM_SetDutyCycle(RED, 0);
        PWM_SetDutyCycle(BLUE, 1000);
        PWM_SetDutyCycle(GREEN, 0);
    }
    //set color to blue
    if (abs(count % 96) > 48 && abs(count % 96) < 60) {
        PWM_SetDutyCycle(RED, 750);
        PWM_SetDutyCycle(BLUE, 1000);
        PWM_SetDutyCycle(GREEN, 750);
    }
    //set color to light green 
    if (abs(count % 96) > 60 && abs(count % 96) < 72) {
        PWM_SetDutyCycle(RED, 0);
        PWM_SetDutyCycle(BLUE, 1000);
        PWM_SetDutyCycle(GREEN, 1000);
    }
    //set color to green
    if (abs(count % 96) > 72 && abs(count % 96) < 84) {
        PWM_SetDutyCycle(RED, 500);
        PWM_SetDutyCycle(BLUE, 1000);
        PWM_SetDutyCycle(GREEN, 1000);
    }
    //set color to yellow
    if (abs(count % 96) > 84 && abs(count % 96) < 96) {
        PWM_SetDutyCycle(RED, 0);
        PWM_SetDutyCycle(BLUE, 0);
        PWM_SetDutyCycle(GREEN, 1000);
    }

}

void QEI_ResetPosition(void) {
    rot = 0;
    count = 0;
    return;
}

int main(void) {
    QEI_Init();
    BOARD_Init();
    SERIAL_Init();
    PWM_Init();
    PWM_AddPins(RED); //R
    PWM_AddPins(GREEN); //G
    PWM_AddPins(BLUE); //B
    while (1) {

    }

}

