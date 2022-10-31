#include <string.h>
#include <time.h>
#include <stdlib.h>

/**
*Purpose: receive and print data from a sensor via an analog input.
*testSensor.ino

*@author Juan Carlos Bautista Sandoval.
*@version 1.0.0
**/

int ldr = A0; //Set A0(Analog Input) for LDR.
int value1 = 0;
int value2 = 0;
int value3 = 0;


/**
*   Configure the initial data of the program.
**/
void setup() {
    srand(time(NULL));
    Serial.begin(9600);
}

/**
* Function to be repeated indefinitely on some type of device.
**/
void loop()
{
    value1=analogRead(ldr); //Reads the value of LDR(light).
    String result1 = "plot1 " + String(value1);
    Serial.println(result1); //Print the read value 

    value2 = rand() % 100;
    String result2 = "plot2 " + String(value2);
    Serial.println(result2);

    value3 = rand() % 50;
    String result3 = "plot3 " + String(value3);
    Serial.println(result3);
}
