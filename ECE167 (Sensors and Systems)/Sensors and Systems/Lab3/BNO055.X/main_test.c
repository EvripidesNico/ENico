/* 
 * File:   main_test.c
 * Author: Bulls
 *
 * Created on February 22, 2024, 6:08 PM
 */

#include <stdio.h>
#include <stdlib.h>
#include "BNO055.h"
#include "BOARD.h"
#include "I2C.h"
#include "pwm.h"

#include <xc.h>

#include "serial.h"
#define POWERPIN_LAT LATFbits.LATF1
#define POWERPIN_TRIS TRISFbits.TRISF1




//#define BNO055_GYRO

#ifdef BNO055_GYRO
int main(void) {
    char initResult;
    BOARD_Init();

    // printf("Welcome to the BNO055 test compiled at " __DATE__ " " __TIME__ ". Sensor will be brought up and then values displayed\r\n");
    while (!IsTransmitEmpty());
    POWERPIN_LAT = 0;
    POWERPIN_TRIS = 0;
    POWERPIN_LAT = 1;

    float xgyro = 0, ygyro = 0, zgyro = 0;
    float xbias = -12.33636364;
    float ybias = -9.918181818;
    float zbias = 11.59090909;
    float zscalar = (-21700)  / 180;
    float xscalar = 21000 / 180;
    float yscalar = 12000 / 90;

    float zint = 0;
    float xint = 0;
    float yint = 0;
    DelayMicros(100000);
    initResult = BNO055_Init();
    
    if (initResult != TRUE) {
        printf("Initialization of IMU failed, stopping here\r\n");
    } else {
        printf("Initialization succeeded\r\n");
        while (1) {
            // gyroscope bias implementation
            xgyro += ((BNO055_ReadGyroX() - xbias)* 0.1);
            ygyro += ((BNO055_ReadGyroY() - ybias)* 0.1);
            zgyro += ((BNO055_ReadGyroZ() - zbias)* 0.1);
            // gyro scalar 
            zint = zgyro / zscalar;
            xint = xgyro / xscalar;
            yint = ygyro / yscalar;
            //print values of gyroscope
            if (IsTransmitEmpty()) {
                printf("%+06f %+06f %+06f", xint, yint, zint);
               // printf("%+06d, %+06d, %+06d    ", BNO055_ReadGyroX(), BNO055_ReadGyroY(), BNO055_ReadGyroZ());
                // printf("Temp: %+06d", BNO055_ReadTemp());
                printf("\r\n");
                DelayMicros(100000);
            }
        }
    }
    while (1);
}
#endif


//#define BNO055_ACCEL

#ifdef BNO055_ACCEL
int main(void) {
    char initResult;
    BOARD_Init();

    // printf("Welcome to the BNO055 test compiled at " __DATE__ " " __TIME__ ". Sensor will be brought up and then values displayed\r\n");
    while (!IsTransmitEmpty());
    POWERPIN_LAT = 0;
    POWERPIN_TRIS = 0;
    POWERPIN_LAT = 1;

    float xaccel = 0, yaccel = 0, zaccel= 0;
    float xbias = 10.932529162248102;
    float ybias = 48.966368515205716;
    float zbias = -1.125300721732174;

 
    DelayMicros(100000);
    initResult = BNO055_Init();
    //scaled value = (measurement - bias)* -scalar
    
    if (initResult != TRUE) {
        printf("Initialization of IMU failed, stopping here\r\n");
    } else {
        printf("Initialization succeeded\r\n");
        while (1) {
            // accel bias implementation
            xaccel = ((BNO055_ReadAccelX() - xbias)* -0.001);
            yaccel = ((BNO055_ReadAccelY() - ybias)* -0.001);
            zaccel = ((BNO055_ReadAccelZ() - zbias)* 0.001);
           
            //print values of accel
            if (IsTransmitEmpty()) {
               printf("Accel: (%+06f, %+06f, %+06f)   ", xaccel, yaccel, zaccel);
               // printf("%+06d %+06d %+06d   ", BNO055_ReadAccelX(), BNO055_ReadAccelY(), BNO055_ReadAccelZ());
                printf("\r\n");
                DelayMicros(100000);
            }
        }
    }
    while (1);
}
#endif


//#define BNO055_MAG

#ifdef BNO055_MAG
int main(void) {
    char initResult;
    BOARD_Init();

    // printf("Welcome to the BNO055 test compiled at " __DATE__ " " __TIME__ ". Sensor will be brought up and then values displayed\r\n");
    while (!IsTransmitEmpty());
    POWERPIN_LAT = 0;
    POWERPIN_TRIS = 0;
    POWERPIN_LAT = 1;

    //magnometer bias, scale and variables
    float xmag= 0, ymag = 0, zmag= 0;
    float xbias = 31.916797488226060;
    float ybias = 210.8995290423862;
    float zbias = 937.392464678179;
    
    float xscal = 0.016389189189189;
    float yscal= -0.01576216216216;
    float zscal = 0.015589189189189;
 
    DelayMicros(100000);
    initResult = BNO055_Init();
    //scaled value = (measurement - bias)* -scalar
    
    if (initResult != TRUE) {
        printf("Initialization of IMU failed, stopping here\r\n");
    } else {
        printf("Initialization succeeded\r\n");
        while (1) {
            // magnometer bias implementation
            xmag = ((BNO055_ReadMagX() - xbias) / xscal);
            ymag = ((BNO055_ReadMagY() - ybias)/ yscal);
            zmag = ((BNO055_ReadMagZ() - zbias)/ zscal);
            
            //print values of magnometer
            if (IsTransmitEmpty()) {
               printf("mag: (%+06f, %+06f, %+06f)   ", xmag, ymag, zmag);
               //printf("%+06d %+06d %+06d", BNO055_ReadMagX(), BNO055_ReadMagY(), BNO055_ReadMagZ());
                printf("\r\n");
                DelayMicros(100000);
            }
        }
    }
    while (1);
}
#endif