/* 
 * File:   main.c
 * Author: Jerek
 *
 * Created on March 7, 2024, 7:23 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "BOARD.h"
#include "serial.h"
#include "AD.h"
#include "PING.h"
#include "pwm.h"
#include "Buttons.h"
#include "timers.h"

// OPTIONAL COMPILATION DEFINES
#define MAIN_ACTIVE 1 // Enables the main function in this file.
#define SERVO_TEST_BUTTONS 0 // SERVO_TEST_BUTTONS when enabled, disables the state machine and ties servo motion directly to the PIC32 Buttons
#define SERVO_DEBUG 0 // Enables debug printfs

#define STATE_MACHINE_ENABLE !SERVO_TEST_BUTTONS // Inverse macro for easy code reading

// PROGRAM DEFINES
#define SERVO_PWM PWM_PORTZ06 // OC1 Register or Pin 3 on I/O Shield
#define SERVO_MIN 36 // Minimum duty cycle at which rotations begin
#define SERVO_1RAD_FROM_MIN 233 // 180 degrees from minimum position
#define SERVO_MAX 263 // Maximum duty cycle at which the servo does not rotate
#define DATA_COLLECTION_TIME_MILSEC 50

#define PING_BUFFER 1 // The number of data points that the sonar will collect at each position


/*
 * 
 */

/* STATE MACHINE LOGIC
 * 
 * 1. Starts in serial_idle state, which will wait until a connection and start 
 * command from the user interface (WIP).
 * 
 * 2. After starting, it will sweep CounterClockwise, starting at the lowest 
 * PWM Duty cycle fro the servo. The sweep occurs by incrementing (Or
 * decrementing when in clockwise) the PWM duty cycle.
 * 
 * 3. After every increment of the PWM duty cycle, it will enter one of the 
 * PING_EN states and begin collecting samples at that orientation up to the 
 * buffer size macro, outputting the average.
 * 
 * 4. In sweep_counterClockWise, when the PWM duty cycle reaches the 180 
 * degree mark value, it will then switch to sweep_clockwise, collecting data
 * with it's own PING_EN state, then going back to sweep counterClockwise. The
 * State machine will cycle between sweep_clockWise and sweep_counterClockWise
 * until a command is sent by the UI (WIP) or the PIC is unplugged.
 */
typedef enum {
    sweep_counterClockWise = 0x6, // This state sets the servo PWM to move counterClockwise
    sweep_clockWise = 0x66, // This state sets the the servo PWM to move clockWise
    serial_idle = 0x67, // This state is the control state for the 
    PING_EN_counter = 0x68, // This state will begin collecting new data from the ping sensors when moving counter clockwise. 
    PING_EN_clock = 0x69, // This state will begin collecting new data from the ping sensors when moving clockwise.
} States;



#if MAIN_ACTIVE

int main(int argc, char** argv) {
    /*
     * LIBRARY INITIALIZIATIONS
     */
    BOARD_Init();
    SERIAL_Init();
    PWM_Init();
    TIMERS_Init();
    PING_Init(); // PING INIT MUST GO LAST (Or after PWM_Init)


    // SERVO_TEST_BUTTONS
    // Initialization for the buttons for the SERVO_TEST_BUTTONS condition
#if SERVO_TEST_BUTTONS 
    ButtonsInit();
    unsigned int timeCount = TIMERS_GetMilliSeconds();
    unsigned int debounce = TIMERS_GetMilliSeconds();
    uint8_t press = 0;
    //TRISDbits.TRISD1 = 0;
    //TRISDbits.TRISD2 = 0;
    
    //PORTDbits.RD1 = 1;
    //PORTDbits.RD2 = 1;

    struct buttons {
        uint8_t but1On : 1;
        uint8_t but2On : 1;
        uint8_t but3On : 1;
        uint8_t but4On : 1;
    } buttonState;
#endif

    // INITIAL VARIABLE DECLARATIONS
    uint16_t servoControlVal = SERVO_MIN; // PWM_duty cycle for the servo.
    uint8_t state = serial_idle; // current state variable
    unsigned int stateTimer; // Timer for state changes, deprecated
    unsigned int p1Buffer[PING_BUFFER]; // May be deprecated, flag for deletion.
    unsigned int p2Buffer[PING_BUFFER]; // May be deprecated, flag for deletion.
    uint8_t pingInc = 0; // Used for writing to the buffer, deprecated, flag for deletion.
    unsigned int tempP1Sum = 0; // Used to sum Ping data values for averaging
    unsigned int tempP2Sum = 0; // Used to sum Ping data values for averaging
    //uint32_t PAUSETIME = 0; // Deprecated test variable.


    /*
     *  INITIAL CODE EXECUTION
     */

    // SERVO PWM INITIALIZATION
    PWM_SetFrequency(MIN_PWM_FREQ);
    PWM_AddPins(SERVO_PWM);
    PWM_SetDutyCycle(SERVO_PWM, SERVO_MIN - 1);

    // TIME CODE
    time_t programStartTime = 1710358560; //LOCAL UNIX EPOCH TIME AT INSTANTIATION, UPDATE AS NEEDED
    time(&programStartTime);
    printf("PROGRAM START TIME: %s\n\r", ctime(&programStartTime)); // OUTPUT IS TIME GMT
    stateTimer = TIMERS_GetMilliSeconds();
    printf("SAMPLE PER CHANGE: %i\n\r", PING_BUFFER);

    
    static uint8_t p1Test;
    static uint8_t p2Test;

    while (1) {

#if STATE_MACHINE_ENABLE
        switch (state) {

            case serial_idle: // SERIAL STATE FOR UI COMMANDS. (WIP)
                if (TIMERS_GetMilliSeconds() - stateTimer > 5000) {
                    printf("INITIALIZING STATE MACHINE\n\r");
                    state = sweep_counterClockWise; // Initial 0 position sweeps counterclockwise (Servo orientation))
                }
                break;

            case sweep_clockWise: // Servo Sweeping clockwise

                // Break condition if area has been swept.
                if (servoControlVal == SERVO_MIN) {
                    state = sweep_counterClockWise;
                    break;
                }

                // Ternary operator for incrementing servo PWM duty cycle.
                servoControlVal = ((servoControlVal - 1) < SERVO_MIN) ? SERVO_MIN : servoControlVal - 1;
                PWM_SetDutyCycle(SERVO_PWM, servoControlVal);

                // Change to PING data Collection
                state = PING_EN_clock;

#if SERVO_DEBUG
                printf("SWEEPING CLOCKWISE, LAST PWM: %i\n\r", servoControlVal);
#endif
                break;

            case sweep_counterClockWise: // Servo sweeping clockwise

                // Break condition if area has been swept.
                if (servoControlVal == SERVO_1RAD_FROM_MIN) {
                    state = sweep_clockWise;
                    break;
                }

                // Ternary operator for incrementing servo PWM duty cycle.
                servoControlVal = ((servoControlVal + 1) > SERVO_1RAD_FROM_MIN) ? SERVO_1RAD_FROM_MIN : servoControlVal + 1;
                PWM_SetDutyCycle(SERVO_PWM, servoControlVal);

                // Change to PING data Collection
                state = PING_EN_counter;

#if SERVO_DEBUG
                printf("SWEEPING COUNTER-CLOCKWISE, LAST PWM: %i\n\r", servoControlVal);
#endif
                break;

            case PING_EN_clock: // Data Collection State for clockwise

                p1Test = PING_P1_NewDataAvailable() | p1Test;
                p2Test = PING_P2_NewDataAvailable() | p2Test;
                if (PING_P1_NewDataAvailable()) {

                    // Data collection and storage
                    p1Buffer[pingInc] = PING_GetDistance_P1();
                    tempP1Sum += p1Buffer[pingInc];
                    p2Buffer[pingInc] = PING_GetDistance_P2();
                    tempP2Sum += p2Buffer[pingInc];
                    pingInc = pingInc + 1;

                    // Changing states once data buffer is filled. Prints average
                    if (pingInc >= PING_BUFFER) {
                        pingInc = 0;
                        printf("%d,%d,%d\n\r", (tempP1Sum / PING_BUFFER), (tempP2Sum / PING_BUFFER), servoControlVal);
                        tempP1Sum = 0;
                        tempP2Sum = 0;
                        state = sweep_clockWise;
                    }

                }


                break;

            case PING_EN_counter: // Data Collection State for counter clockwise

                p1Test = PING_P1_NewDataAvailable() | p1Test;
                p2Test = PING_P2_NewDataAvailable() | p2Test;

                if (p1Test && p2Test) {

                    //Data collection and storage
                    p1Buffer[pingInc] = PING_GetDistance_P1();
                    tempP1Sum += p1Buffer[pingInc];
                    p1Buffer[pingInc] = PING_GetDistance_P2();
                    tempP2Sum += p2Buffer[pingInc];

                    pingInc = pingInc + 1;
                    p1Test = 0;
                    p2Test = 0;
                    // Changing states once data buffer is filled. Prints average
                    if (pingInc >= PING_BUFFER) {
                        pingInc = 0;
                        printf("%d,%d,%d\n\r", (tempP1Sum / PING_BUFFER), (tempP2Sum / PING_BUFFER), servoControlVal);
                        tempP1Sum = 0;
                        tempP2Sum = 0;
                        state = sweep_counterClockWise;

                    }
                }
                break;
        }
        // END OF STATE MACHINE
#endif

#if SERVO_TEST_BUTTONS

        /* Button 1: increment of 1 to duty cycle
         * Button 2: decrement of 1 to duty cycle  
         * Button 3: increment of 5 to duty cycle
         * Button 4: decrement of 5 to duty cycle
         */

        // BUTTON CODE FOR USER SERVO CONTROL
        press = ButtonsCheckEvents();
        if (press && (TIMERS_GetMilliSeconds() - debounce > 10)) {
            debounce = TIMERS_GetMilliSeconds();

            buttonState.but1On = ((BUTTON_EVENT_1DOWN & press) || buttonState.but1On) && !(BUTTON_EVENT_1UP & press);
            buttonState.but2On = ((BUTTON_EVENT_2DOWN & press) || buttonState.but2On) && !(BUTTON_EVENT_2UP & press);
            buttonState.but3On = ((BUTTON_EVENT_3DOWN & press) || buttonState.but3On) && !(BUTTON_EVENT_3UP & press);
            buttonState.but4On = ((BUTTON_EVENT_4DOWN & press) || buttonState.but4On) && !(BUTTON_EVENT_4UP & press);

        }

        if (TIMERS_GetMilliSeconds() - timeCount > 150) {
            //currentDistance =
            timeCount = TIMERS_GetMilliSeconds();
            printf("PWM ticker. PWM_VAL %i\n", servoControlVal);

            if (buttonState.but1On) {
                servoControlVal = ((servoControlVal + 1) > 999) ? 1000 : servoControlVal + 1;
                printf("BUTTON ONE\n");
                
            }
            if (buttonState.but2On) {
                servoControlVal = ((servoControlVal - 1) < 1) ? 0 : servoControlVal - 1;
                //PORTFbits.RF1 = 0;
                printf("BUTTON TWO\n");
            }
            if (buttonState.but3On) {
                servoControlVal = ((servoControlVal + 5) > 999) ? 1000 : servoControlVal + 5;
                printf("BUTTON THREE\n");
            }
            if (buttonState.but4On) {
                servoControlVal = ((servoControlVal - 5) < 1) ? 0 : servoControlVal - 5;
                printf("BUTTON FOUR\n");
            }
            PWM_SetDutyCycle(SERVO_PWM, servoControlVal);

        }

#endif 
    }

    return (EXIT_SUCCESS);
}

#endif
