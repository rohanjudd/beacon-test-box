// Transmits IR Beacon signals
// Messages encoded by timing between pulses
// SYNC 4 3 2 1 0 SYNC ...
// IR Rx Pin : D8 
// IR Tx Pin : D13 (PB5)
//
// SYS2 Timing  Frequency = 3.2768 MHz
// T = 1/F * 512 = 156.25 us
// Sync    =  938us  =  15000 ticks
// logic 0 =  469us  =  7500  ticks
// logic 1 =  313us  =  5000  ticks
//
// SYS4 Timing  Frequency = 3.5795 MHz
// T = 1/F * 512 = 143.05 us
// Sync    =  858us  =  13732 ticks
// logic 0 =  286us  =  6866  ticks
// logic 1 =  429us  =  4577  ticks

#define PB5 5
int outPin = 13;  // Use digital pin 13 as output

const int SYS2SYNC = 938, SYS2LOGIC0 = 469, SYS2LOGIC1 = 313;

const int SYS4SYNC = 858, SYS4LOGIC0 = 429, SYS4LOGIC1 = 286;

const int PULSE_WIDTH = 3; //approx 3us pulse width
const int REPEAT = 250;

int sync, logic0, logic1;

const boolean SYS2 = false;
const boolean SYS4 = true;
boolean mode;
boolean split;

void setup() 
{
  pinMode(outPin, OUTPUT);  
  Serial.begin(115200);       
  Serial.println("IR Beacon Transmitter");
  setMode(SYS2);
  splitMode(split);
  Serial.println("m to change mode or value to transmit");
}

void loop() 
{
  if (Serial.available()) 
  {
    char ser = Serial.read();

    if(ser == 'm')
    {
      setMode(!mode);
    }
    else if(ser == 's')
    {
      splitMode(!split);
    }
    else if(ser == 'l')
    {
      Serial.println("Transmitting all codes in sequence");
      for(int v=0; v<32; v++)
      {
        transmit(v, REPEAT);
      }
    }
    else if((ser >= 48) && (ser <= 57)) // Characters 0 through 9
    {
      byte b = ser - 48; // convert ascii code to byte hex value
      bitWrite(b, 4, split); // write split value to MSB
      transmit(b, REPEAT);
    }
    else if((ser >= 97) && (ser <= 102)) // Characters a through f
    {
      byte b = ser - 87; // convert ascii code to byte hex value
      bitWrite(b, 4, split); // write split value to MSB
      transmit(b, REPEAT);
    }
  }
  delay(100);
}

void transmit(byte b, int times)
{
  Serial.println(b, HEX);
  for(int x=0; x<times+1; x++)
  {
    if(x==0)
      pulse();
    delayMicroseconds(sync);
    for(int i=4; i>=0; i--)
    {
      pulse();
      if(bitRead(b, i))
      {
        delayMicroseconds(logic1);
      }
      else
      {
        delayMicroseconds(logic0);
      }
    }
    pulse();
  }
}

void pulse()
{
  PORTB |= 1<<PB5;       // sets pin13 high
  delayMicroseconds(PULSE_WIDTH);
  PORTB &= ~(1<<PB5);    // sets pin13 low
}

void setMode(boolean newmode)
{
  mode = newmode;
  if(newmode == SYS2)
  {
    Serial.println("SYS2 Mode Enabled");
    sync = SYS2SYNC -10;
    logic0 = SYS2LOGIC0 -10;
    logic1 = SYS2LOGIC1 -10;
  }
  else
  {
    Serial.println("SYS4 Mode Enabled");
    sync = SYS4SYNC;
    logic0 = SYS4LOGIC0;
    logic1 = SYS4LOGIC1;
  }
}

void splitMode(boolean newmode)
{
  split = newmode;
  if(split == true)
  {
    Serial.println("Split Mode Enabled");
  }
  else
  {
    Serial.println("Split Mode Disabled");
  }
}

