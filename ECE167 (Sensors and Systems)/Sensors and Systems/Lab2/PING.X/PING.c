/* 
 * File:   PING.c
 * Author: Bulls
 *
 * Created on January 30, 2024, 2:41 PM
 */

#include <stdio.h>
#include <stdlib.h>

#include "AD.h"
#include "Ascii.h"
#include "BOARD.h"
#include "pwm.h"
#include "PING.h"
#include "serial.h"
#include "timers.h"
#include "ToneGeneration.h"

/*
 * 
 */
#define TRIGGER PWM_PORTY10

enum states {
    Polling, NotPoll
};

enum states2 {
    ten, sixty
};
enum states State;
enum states2 section;

volatile int PingF = 0;
volatile int Pong = 0;
volatile int PongDif = 0;
volatile int milli = 0;
volatile int micro = 0;
volatile int diff_milli = 0;
volatile int diff_micro = 0;

char PING_Init(void) {
    // following block inits the timer
    T4CON = 0;
    T4CONbits.TCKPS = 0b110;
    PR4 = 3750; // this is not the timer value wanted
    T4CONbits.ON = 1;
    IFS0bits.T4IF = 0;
    IPC4bits.T4IP = 3;
    IEC0bits.T4IE = 1;

    // following block inits change notify
    CNCONbits.ON = 1; // Change Notify On
    CNENbits.CNEN14 = 1;
    int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
    IFS1bits.CNIF = 0; // clear interrupt flag
    IPC6bits.CNIP = 1; //set priority
    IPC6bits.CNIS = 3; // and sub priority
    IEC1bits.CNIE = 1; // enable change notify
    //Anything else that needs to occur goes here
    // PR4 = 0x0040;
    State = Polling; //setting state for CN statemachine
    section = sixty; //setting state for timer statemacine
    milli = TIMERS_GetMilliSeconds();
    micro = TIMERS_GetMicroSeconds();
    // PWM_SetDutyCycle(TRIGGER, 1000);
    PingF = PORTDbits.RD4; //reding echo


}

void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
    static char readPort = 0;
    readPort = PORTD; // this read is required to make the interrupt work
    IFS1bits.CNIF = 0;
    //Anything else that needs to occur goes here

    PingF = PORTDbits.RD5;
    //polling echo and trigger statemachine
    //measure the time it takes to get an echo from a trigger
    switch (State) {
        case Polling: 
            //check if trigger is sent
            //get current micro seconds
            if (PingF == 1) {
                State = NotPoll;
                Pong = TIMERS_GetMicroSeconds();


            }
            break;
        case NotPoll:
            //when echo is gotten then take the diffrerenece from pong to ping
            //that is the time it took to travel the distance 
            if (PingF != 1) {
                State = Polling;
                PongDif = (TIMERS_GetMicroSeconds() - Pong);

            }

            break;
    }
}

void __ISR(_TIMER_4_VECTOR) Timer4IntHandler(void) {
    IFS0bits.T4IF = 0;
//    Anything else that needs to occur goes here
    diff_micro = TIMERS_GetMicroSeconds() - micro;
    diff_milli = TIMERS_GetMilliSeconds() - milli;

    switch (section) {
        case ten:
            //wait 10 micro seconds to turn off trigger
            if (abs(diff_micro) >= 10) {
                PWM_SetDutyCycle(TRIGGER, 0);
                section = sixty;
            }
            break;
        case sixty:
            //wait 60 milli seconds and then turn trigger on 
            if (abs(diff_milli) >= 60) {
                PWM_SetDutyCycle(TRIGGER, 1000);
                section = ten;

                milli = TIMERS_GetMilliSeconds();
                micro = TIMERS_GetMicroSeconds();
            }
            break;
    }
}

unsigned int PING_GetDistance(void) {
    //values gotten from least square
    return (1.0722 * (PongDif / 5.8)) - 14.5092;
}

unsigned int PING_GetTimeofFlight(void) {
    return PongDif;
}

int main(void) {
    BOARD_Init();
    PING_Init();

    SERIAL_Init();
    AD_Init();
    PWM_Init();
    TIMERS_Init();
    ToneGeneration_Init();

    //trigger is the trigger for the ping setting to 1000 sets of the trigger
    PWM_AddPins(TRIGGER);
    PWM_SetDutyCycle(TRIGGER, 1000);
    ToneGeneration_ToneOn();

    while (1) {
        //setting frequency to the value of the ping distance calulated
        ToneGeneration_SetFrequency(PING_GetDistance());
        ToneGeneration_ToneOn();
                //if ping is too high then cut frequency off
                if(PING_GetDistance() > 1600){
                    ToneGeneration_ToneOff();
                }
    }

}

