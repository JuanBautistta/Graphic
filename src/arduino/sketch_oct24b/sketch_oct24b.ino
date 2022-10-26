/**
*Purpose: receive and print data from a sensor via an analog input.
*testSensor.ino

*@author Juan Carlos Bautista Sandoval.
*@version 1.0.0
**/

int ldr = A0;
int value = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    if (Serial.read() == 'g'){
      //srand(50);
      //int data = (rand() % 10) + 1;
      //Serial.println(data);
      value = analogRead(ldr);
      Serial.println(value);
    }
  }
}
