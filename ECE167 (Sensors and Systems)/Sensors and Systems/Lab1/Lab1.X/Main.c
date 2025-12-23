/* 
 * File:   Main.c
 * Author: Bulls
 *
 * Created on January 19, 2024, 12:43 PM
 */

#include <stdio.h>
#include <stdlib.h>

#include "ToneGeneration.h"
#include "BOARD.h"
#include "AD.h"
#include "Adc.h"
#include "pwm.h"


//#define SensorDataTest
//#define NOP_Delay
#define FLAG_Delay

#define DELAY(wait) {for(int del = 0; del < wait; del++) {asm("nop");}}

/**
 * @Function TEMAFilter(uint16_t currentValue, uint16_t previousValue, float a)
 * @param -CurrentValue - value read from potentiometer
 *        -Previous value- value read previously
 *        -a - (alpha) smoothing factor
 * @return Uint16_t filtered value
 * @brief  Uses a filter to smooth the values for our Potentiometer
 * @note  None.
 * @author */
uint16_t EWMAFilter(uint16_t currentValue, uint16_t previousValue, float a) {
    return (uint16_t) ((a * currentValue) + ((1 - a) * previousValue));
}
#ifdef SensorDataTest

int main(void) {
    BOARD_Init();
    ToneGeneration_Init();
    AD_Init();
    AD_AddPins(AD_A1); //flex
    AD_AddPins(AD_A2); //peizo

    //float a = 0.19;
    char string[1024];
    char string2[1024];
    while (1) {
        if (AD_IsNewDataReady()) {
            sprintf(string, "%d\r\n", AD_ReadADPin(AD_A2));
            for (int wait = 0; wait < 18000; wait++) {
                asm("nop");
            }
            puts(string);

            sprintf(string2, "%d\r\n", AD_ReadADPin(AD_A1));
            for (int x = 0; x < 18000; x++) {
                asm("nop");
            }
            puts(string2);
        }
    }

    return (1);
}
#endif

#ifdef NOP_Delay    

int main(void) {
    BOARD_Init();
    ToneGeneration_Init();
    AD_Init();
    PWM_Init();
    AD_AddPins(AD_A1); //flex
    AD_AddPins(AD_A2); //peizo

    float a = 0.19;
    char string[1024];
    int tone = 0;
    uint16_t stone = 0;
    while (1) {
        tone = AD_ReadADPin(AD_A1) + 100; //read flex sensor as tone

        if (AD_ReadADPin(AD_A2) > 55) { //if piezo detected touch
            tone = AD_ReadADPin(AD_A1);
            stone = EWMAFilter(tone, stone, a);

            //            sprintf(string, "%d\r\n", stone); //testing values
            //            puts(string);

            if (abs(stone - tone) > 20) { //check for a noticable change
                ToneGeneration_SetFrequency(stone / 3);
                ToneGeneration_ToneOn();
            }
            //DELAY and turn off
            DELAY(18000);
            ToneGeneration_ToneOff();
        }

    }
    return (1);
}

#endif
#ifdef FLAG_Delay

int main(void) {
    BOARD_Init();
    ToneGeneration_Init();
    AD_Init();
    //PWM_Init();
    AD_AddPins(AD_A1); //flex
    AD_AddPins(AD_A2); //peizo

    float a = 0.19; //smoothing factor
    int tone = 0; //old tone value
    int finaltone = 0; // final tone
    uint16_t s_tone = 0; // smoothed tone

    int counter = 0; //delay conuter
    int flag = 0; // flag for counter to start


    while (1) {
        tone = AD_ReadADPin(AD_A1); //read flex sensor as tone

        if (abs(AD_ReadADPin(AD_A2)) > 55) { //if piezo detected touch
            flag = 1; // set flag that piezo was pressed 
            tone = AD_ReadADPin(AD_A1);
            s_tone = EWMAFilter(tone, s_tone, a);
        }

        if (flag == 1) {//while flag is raised counter increments by 1
            counter++;
            //reset counter if piezo triggered again
            if (abs(AD_ReadADPin(AD_A2)) > 55) { 
                counter = 0;
            }
            if (abs(s_tone - tone) > 50) { //check for change from previous to new tone
                finaltone = s_tone;
            }
            ToneGeneration_SetFrequency(finaltone / 1.2); //set tone
            ToneGeneration_ToneOn(); //turn speaker on 
        }
        if (counter == 10000) { //sets delay that turns off speaker when reached
            flag = 0; //reset Flag and counter
            counter = 0;
            ToneGeneration_ToneOff(); //turn speaker off
        }
    }
    return (1);
}
#endif