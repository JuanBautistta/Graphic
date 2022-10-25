void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    if (Serial.read() == 'g'){
      srand(50);
      int data = (rand() % 10) + 1;
      Serial.println(data);
    }
  }
}
