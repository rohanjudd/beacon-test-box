
char VERSION[5] = "0.1";

void setup() 
{
  Serial.begin(115200);
  Serial.println("Starting");
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() 
{
  if (Serial.available()) 
  {
    char c = Serial.read();
    switch (c) 
    {
      case 't':
      {
        Serial.println("p");
        break;
      }
      case 'v':
      {
        Serial.print("version: ");
        Serial.print(VERSION);
        break;
      }
      case 'b':
      {
        digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(200);                       // wait for a second
        digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
        delay(200);
        digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(200);                       // wait for a second
        digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
        delay(200);        // wait for a second
        break;
      }
      default: 
      break;
    }
  }
}
