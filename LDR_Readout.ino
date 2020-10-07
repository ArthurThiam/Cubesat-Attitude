int LDR1 = A0;
int LDR2 = A1; 
int LDR3 = A2; 
int LDR4 = A3; 
int LDR5 = A4; 
int LDR6 = A5;
int LDR7 = A6; 
int LDR8 = A7; 
int LDR9 = A8; 
int LDR10 = A9; 
int LDR11 = A10; 
int LDR12 = A11; 

int LDR1_value; 
int LDR2_value;
int LDR3_value;
int LDR4_value;
int LDR5_value;
int LDR6_value;
int LDR7_value;
int LDR8_value;
int LDR9_value;
int LDR10_value;
int LDR11_value;
int LDR12_value;

void setup() {
  Serial.begin(9600);
}

void loop() {

  // read the value from the sensor
  LDR1_value = analogRead(LDR1);
  LDR2_value = analogRead(LDR2);
  LDR3_value = analogRead(LDR3);
  LDR4_value = analogRead(LDR4);
  LDR5_value = analogRead(LDR5);
  LDR6_value = analogRead(LDR6);
  LDR7_value = analogRead(LDR7);
  LDR8_value = analogRead(LDR8);
  LDR9_value = analogRead(LDR9);
  LDR10_value = analogRead(LDR10);
  LDR11_value = analogRead(LDR11);
  LDR12_value = analogRead(LDR12);
  
  // output current LDR values
  Serial.println(',');
  Serial.println(LDR1_value);
  Serial.println(LDR2_value);
  Serial.println(LDR3_value);
  Serial.println(LDR4_value);
  Serial.println(LDR5_value);
  Serial.println(LDR6_value);
  Serial.println(LDR7_value);
  Serial.println(LDR8_value);
  Serial.println(LDR9_value);
  Serial.println(LDR10_value);
  Serial.println(LDR11_value);
  Serial.println(LDR12_value);
  
  // Loop delay
  delay(1000);

}
