#include <string.h>
/**
*Purpose: receive and print data from a sensor via an analog input.
*testSensor.ino

*@author Juan Carlos Bautista Sandoval.
*@version 1.0.0
**/

int ldr = A0; //Set A0(Analog Input) for LDR.
int value = 0;

/**
*   Configure the initial data of the program.
**/
void setup() {
    Serial.begin(9600);
}

/**
* Function to be repeated indefinitely on some type of device.
**/
void loop()
{
    value=analogRead(ldr); //Reads the value of LDR(light).
    String result = "plot1 " + String(value);
    Serial.println(result); //Print the read value 
}
