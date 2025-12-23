/* 
 * File:   GenTone_Main.c
 * Author: Bulls
 *
 * Created on January 12, 2024, 5:09 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include "pwm.h"
#include "ToneGeneration.h"
#include "BOARD.h"
#include "AD.h"
#include "Buttons.h"

/*
 * 
 */
//#define Hardcode
//#define Tone_pot
#define Button
#define ADpin AD_A0


#ifdef Hardcode

int main() {
    BOARD_Init();
    ToneGeneration_Init();

    while (1) {
        //set frequency to preset tone  
        ToneGeneration_SetFrequency(TONE_659);
        ToneGeneration_ToneOn();

    }
}
#endif 

/**
 * @Function TEMAFilter(uint16_t currentValue, uint16_t previousValue, float a)
 * @param -CurrentValue - value read from potentiometer
 *        -Previous value- value read previously
 *        -a - (alpha) smoothing factor
 * @return Uint16_t filtered value
 * @brief  Uses a filter to smooth the values for our Potentiometer
 * @note  None.
 * @author */
uint16_t EMAFilter(uint16_t currentValue, uint16_t previousValue, float a) {
    return (uint16_t) ((a * currentValue) + ((1 - a) * previousValue));
}
#ifdef Tone_pot

int main() {
    BOARD_Init();
    ToneGeneration_Init();
    AD_Init();
    AD_AddPins(ADpin);
    float a = 0.32; //smoothing factor, larger = more reactive, worse smoothing
    // smaller = less reactive, better smoothing
    uint16_t filteredValue = 0;
    while (1) {
        uint16_t currentSample = AD_ReadADPin(ADpin);
        filteredValue = EMAFilter(currentSample, filteredValue, a);
        ToneGeneration_SetFrequency(filteredValue);
        ToneGeneration_ToneOn();

    }
}
#endif

#ifdef Button

int main() {
    //initializations
    BOARD_Init();
    ToneGeneration_Init();
    AD_Init();
    ButtonsInit();
    AD_AddPins(ADpin);
    //smoothing factor, larger = more reactive, worse smoothing
    // smaller = less reactive, better smoothing
    float a = 0.19;

    //variables 

    uint8_t ButtonEvents = 0; //track button bitmask
    uint16_t filteredValue = 0; //filter value output
    uint16_t offsetVal = 0; //DC offset for frequency

    while (1) {
        ButtonEvents = ButtonsCheckEvents();
        //btn1 press 
        if ((ButtonEvents & BUTTON_EVENT_1DOWN)) {
            while (!(ButtonEvents & BUTTON_EVENT_1UP)) { //while btn1 not up
                ButtonEvents = ButtonsCheckEvents();

                uint16_t currentSample = AD_ReadADPin(ADpin);
                filteredValue = EMAFilter(currentSample, filteredValue, a);
                offsetVal = filteredValue / 3;

                ToneGeneration_SetFrequency(TONE_196 + offsetVal);
                ToneGeneration_ToneOn();
            }
            ToneGeneration_ToneOff();
        }
        //btn 2 down  
        if (ButtonEvents & BUTTON_EVENT_2DOWN) {
            while (!(ButtonEvents & BUTTON_EVENT_2UP)) { //while btn2 not up
                ButtonEvents = ButtonsCheckEvents();

                uint16_t currentSample = AD_ReadADPin(ADpin);
                filteredValue = EMAFilter(currentSample, filteredValue, a);
                offsetVal = filteredValue / 3;

                ToneGeneration_SetFrequency(TONE_293 + offsetVal);
                ToneGeneration_ToneOn();
            }
            ToneGeneration_ToneOff();
        }
        //btn3 down
        if (ButtonEvents & BUTTON_EVENT_3DOWN) {
            while (!(ButtonEvents & BUTTON_EVENT_3UP)) { //while btn3 not up
                ButtonEvents = ButtonsCheckEvents();

                uint16_t currentSample = AD_ReadADPin(ADpin);
                filteredValue = EMAFilter(currentSample, filteredValue, a);
                offsetVal = filteredValue / 3;

                ToneGeneration_SetFrequency(TONE_440 + offsetVal);
                ToneGeneration_ToneOn();
            }
            ToneGeneration_ToneOff();
        }
        //btn4 down
        if (ButtonEvents & BUTTON_EVENT_4DOWN) {
            while (!(ButtonEvents & BUTTON_EVENT_4UP)) { //while btn4 not up
                ButtonEvents = ButtonsCheckEvents();

                uint16_t currentSample = AD_ReadADPin(ADpin);
                filteredValue = EMAFilter(currentSample, filteredValue, a);
                offsetVal = filteredValue / 3;

                ToneGeneration_SetFrequency(TONE_659 + offsetVal);
                ToneGeneration_ToneOn();
            }
            ToneGeneration_ToneOff();
        }
    }
}
#endif
