/* 
 * File:   Hello_AD.c
 * Author: Bulls
 *
 * Created on January 12, 2024, 4:38 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include "BOARD.h"
#include "serial.h"
#include "AD.h"

/*
 * 
 */
#define ADpin AD_A0
char string[1024];

int main(void) {
    BOARD_Init();
    AD_Init();
    AD_AddPins(ADpin);
    while (1) {
    
        if (AD_IsNewDataReady()) {
            sprintf(string, "%d\n", AD_ReadADPin(ADpin));
            puts(string);
        }

    }

}

