/* 
 * File:   helloworld.c
 * Author: Bulls
 *
 * Created on January 12, 2024, 3:58 PM
 */

#include <stdio.h>
#include <stdlib.h>

#include "BOARD.h"
#include "serial.h"

/*
 * 
 */
int main(void) {
    BOARD_Init();
    printf("Hello World!\n");
    BOARD_End();

    while (1);
}
