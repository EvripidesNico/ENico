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
// OPTIONALK COMPILATION 
#define PING_TEST_MAIN 0 // OPTIONAL COMPILE FOR MAIN IN THIS FILE

#define SERVO_PWM PWM_PORTZ06 //port3
#define TRIGGER PORTDbits.RD2 //port6
#define TRIGGER2 PORTDbits.RD1 //port5
//#define TRIGGER PWM_PORTY10 //port6
//#define TRIGGER2 PWM_PORTY12 //port5
//#define DELAY(wait) {for(int del = 0; del < wait; del++) {asm("nop");}}//y12 port5
//z06 port3

#define SERVO_MIN 36 // Minimum duty cycle at which rotations begin
#define SERVO_MAX 263 // Maximum duty cycle at which the servo does not rotate

enum states {
    Polling, NotPoll
};

enum states2 {
    ten, sixty
};

enum ServoState {
    servo, pingRead
};
enum currentTrigger{
    TRIGGER_SENSOR1, TRIGGER_SENSOR2
};
enum currentTrigger currentTrigger;

enum states State;
enum states State2;
enum states2 section;
enum ServoState ServoSSM;

volatile int PingF = 0;
volatile int PingF2 = 0;
volatile int Pong = 0;
volatile int PongDif = 0;
volatile int milli = 0;
volatile int micro = 0;
volatile int diff_milli = 0;
volatile int diff_micro = 0;
volatile int Pong2 = 0;
volatile int PongDif2 = 0;
volatile int milli2 = 0;
volatile int micro2 = 0;
volatile int diff_milli2 = 0;
volatile int diff_micro2 = 0;
volatile int flag = 0;
volatile int flag2 = 0;
volatile int servoDir = 0;
volatile int servoPWM = 0;
static volatile uint8_t ping1NewData; // Effectively Booleans, checking for new data
static volatile uint8_t ping2NewData;

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
    CNENbits.CNEN14 = 1; //activates RD5
    CNENbits.CNEN15 = 1; //enable one phase RD6

    int temp = PORTD; // this is intentional to ensure a interrupt occur immediately upon enabling
    IFS1bits.CNIF = 0; // clear interrupt flag
    IPC6bits.CNIP = 1; //set priority
    IPC6bits.CNIS = 3; // and sub priority
    IEC1bits.CNIE = 1; // enable change notify
    //Anything else that needs to occur goes here
    // PR4 = 0x0040;
    State = Polling; //setting state for CN statemachine
    State2 = Polling;
    section = sixty; //setting state for timer statemacine
    milli = TIMERS_GetMilliSeconds();
    micro = TIMERS_GetMicroSeconds();
    // PWM_SetDutyCycle(TRIGGER, 1000);
    PingF = PORTDbits.RD5; //reding echo
    PingF2 = PORTDbits.RD6;

    //PWM_Init();
    //PWM_AddPins(TRIGGER);
    //PWM_AddPins(TRIGGER2);
    TRISDbits.TRISD1 = 0;
    TRISDbits.TRISD2 = 0;
}

void statemachine(void) {
    switch (State) {

        case Polling:
            //check if trigger is sent
            //get current micro seconds

            if (PingF == 1 && flag == 0) {
                State = NotPoll;
                Pong = TIMERS_GetMicroSeconds();
                flag = 1;
                


            }
            break;
        case NotPoll:
            //when echo is gotten then take the difference from pong to ping
            //that is the time it took to travel the distance 
            if (PingF != 1 && flag == 1) {
                State = Polling;
                PongDif = (TIMERS_GetMicroSeconds() - Pong);
                flag = 0;
                ping1NewData = 1;


            }

            break;
    }
}

void statemachine2(void) {
    switch (State2) {
        case Polling:
            //check if trigger is sent
            //get current micro seconds
            if (PingF2 == 1 && flag2 == 0) {
                State2 = NotPoll;
                Pong2 = TIMERS_GetMicroSeconds();
                flag2 = 1;
            }
            break;
        case NotPoll:
            //when echo is gotten then take the difference from pong to ping
            //that is the time it took to travel the distance 
            if (PingF2 != 1 && flag2 == 1) {
                State2 = Polling;
                PongDif2 = (TIMERS_GetMicroSeconds() - Pong2);
                flag2 = 0;
                ping2NewData = 1;

            }

            break;
    }
}

void __ISR(_CHANGE_NOTICE_VECTOR) ChangeNotice_Handler(void) {
    static char readPort = 0;
    readPort = PORTD; // this read is required to make the interrupt work
    IFS1bits.CNIF = 0;
    //Anything else that needs to occur goes here

    PingF = PORTDbits.RD5;
    PingF2 = PORTDbits.RD6;
    //polling echo and trigger state machine
    //measure the time it takes to get an echo from a trigger
    //state machine(rd5
    /// statemahice rd6)

    statemachine();
    statemachine2();


}

void __ISR(_TIMER_4_VECTOR) Timer4IntHandler(void) {
    IFS0bits.T4IF = 0; // Clear Timer 4 interrupt flag

    // Calculate time differences
    diff_micro = TIMERS_GetMicroSeconds() - micro;
    diff_milli = TIMERS_GetMilliSeconds() - milli;

    // Perform actions based on the current state
    switch (currentTrigger) {
        case TRIGGER_SENSOR1:
            // Wait 10 microseconds before triggering sensor 1
            if (abs(diff_micro) >= 10) {
                //PWM_SetDutyCycle(TRIGGER, 1000); // Trigger sensor 1
                TRIGGER = 1;
                currentTrigger = TRIGGER_SENSOR2; // Switch to trigger sensor 2 next
                milli = TIMERS_GetMilliSeconds();
                micro = TIMERS_GetMicroSeconds();
            }
            break;
        case TRIGGER_SENSOR2:
            // Wait 60 milliseconds before triggering sensor 2
            if (abs(diff_milli) >= 60) {
                //PWM_SetDutyCycle(TRIGGER2, 1000); // Trigger sensor 2
                TRIGGER2 = 1;
                currentTrigger = TRIGGER_SENSOR1; // Switch back to trigger sensor 1
                milli = TIMERS_GetMilliSeconds();
                micro = TIMERS_GetMicroSeconds();
            }
            break;
    }

    // Turn off trigger signals after a certain duration
    if (currentTrigger == TRIGGER_SENSOR1 && abs(diff_micro) >=     10) {
        TRIGGER = 0;
        //PWM_SetDutyCycle(TRIGGER, 0); // Turn off txrigger for sensor 1 after 20 microseconds
    } else if (currentTrigger == TRIGGER_SENSOR2 && abs(diff_milli) >= 10) {
        TRIGGER2 = 0;
        //PWM_SetDutyCycle(TRIGGER2, 0); // Turn off trigger for sensor 2 after 120 milliseconds
    }
}


unsigned int PING_GetDistance_P1() {
    // constants gotten from least square
    // Returns distance calculation from ping constants    
    unsigned int dist = (0.9945 * (PongDif / 5.8)) + 24.8403;
    return dist;
}

unsigned int PING_GetDistance_P2() {
    // constants gotten from least square, not accurate calibration
    // Returns distance calculation from ping constants 
    unsigned int dist2 = (0.9945 * (PongDif2 / 5.8)) + 24.8403;
    //ping2NewData = 0; // Data called, data is no longer new
    return dist2;
}

unsigned int PING_GetTimeofFlight_P1(void) {
    return PongDif;
}

unsigned int PING_GetTimeofFlight_P2(void) {
    return PongDif;
}

uint8_t PING_P1_NewDataAvailable(void) {
    if (ping1NewData == 1) {
        ping1NewData = 0;
        return 1;
    }
    return 0;
}

uint8_t PING_P2_NewDataAvailable(void) {
    if (ping2NewData == 1) {
        ping2NewData = 0;
        return 1;
    }
    return 0;
}

#if PING_TEST_MAIN

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
    PWM_AddPins(TRIGGER2);
    PWM_SetDutyCycle(TRIGGER, 1000);
    PWM_SetDutyCycle(TRIGGER2, 1000);

    //setting up servo pin 
    PWM_SetFrequency(MIN_PWM_FREQ);
    PWM_AddPins(SERVO_PWM);
    PWM_SetDutyCycle(SERVO_PWM, SERVO_MIN);
    servoPWM = SERVO_MIN;
    servoDir = 0; //controls direction for servo
    flag2 = 0;
    flag = 0;
    
    unsigned int timeCheck = TIMERS_GetMilliSeconds();


    while (1) {

        switch (ServoSSM) {
            case servo:
                if (servoDir == 0) {
                    servoPWM += 1;
                    PWM_SetDutyCycle(SERVO_PWM, servoPWM);
                    if (servoPWM >= SERVO_MAX) {
                        servoDir = 1;
                    }
                }
                if (servoDir == 1) {
                    servoPWM -= 1;
                    PWM_SetDutyCycle(SERVO_PWM, servoPWM);
                    if (servoPWM <= SERVO_MIN) {
                        servoDir = 0;
                    }
                }
                ServoSSM = pingRead;


                break;
            case pingRead:
                printf("%d,%d,%d\n\r",  PING_GetDistance_P1(),PING_GetDistance_P2(), servoPWM);

                ServoSSM = servo;
                while(TIMERS_GetMilliSeconds() - timeCheck < 100);
                timeCheck = TIMERS_GetMilliSeconds();
                break;
        }

    }

}
/*switch behavior
 * case ServoCW;
 *  ServoPWM +=1;
 * 
 * Case: ReadPing
 * pingGetdistance P1&P2&PWM
 * Case: 
 * 
 */
#endif