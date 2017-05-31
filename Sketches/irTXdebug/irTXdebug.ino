// Transmits IR Beacon signals
// Messages encoded by timing between pulses
// SYNC 4 3 2 1 0 SYNC ...
// Output: Pin D13 (PB5)
//
// SYS2 Timing - Frequency = 3.2768 MHz
// T = 1/F * 512 = 156.25 us
// Number of timer ticks = T * 16 = 2500 ticks
// Sync = 15000 ticks
// logic 0 = 7500 ticks
// logic 1 = 5000 ticks
//
// SYS4 Timing - Frequency = 3.5795 MHz
// T = 1/F * 512 = 143.05 us
// Number of timer ticks = T * 16 = 2289 ticks
// Sync = 13732 ticks
// logic 0 = 6866 ticks
// logic 1 = 4577 ticks

#define PB5 5
int outPin = 13;  // Use digital pin 13 as output

const int SYS2SYNC = 15000, SYS2LOGIC0 = 7500, SYS2LOGIC1 = 5000;

const int SYS4SYNC = 13732, SYS4LOGIC0 = 6866, SYS4LOGIC1 = 4577;

const int PULSE_WIDTH = 3; //approx 3us pulse width
const int REPEAT = 1;

int sync, logic0, logic1;

const boolean SYS2 = false;
const boolean SYS4 = true;
boolean mode;

void setup() 
{
  pinMode(outPin, OUTPUT);  
  Serial.begin(115200);       
  Serial.println("IR Beacon Transmitter");
  setMode(SYS2);
  Serial.println("m to change mode or value to transmit");
}

void loop() 
{
  if (Serial.available()) 
  {
    char ser = Serial.read();

    if(ser == 'm'){
      setMode(!mode);
    }
    else if((ser >= 48) && (ser <= 57)) // Characters 0 through 9
    {
      transmit(ser - 48, REPEAT);
    }
    else if((ser >= 97) && (ser <= 102)) // Characters a through f
    {
      transmit(ser - 87, REPEAT);
    }
  }
  delay(100);
}

void transmit(byte b, int times)
{
  for(int x=0; x<times; x++)
  {
    pulse();
    delay(800);
    Serial.print("s");
    for(int i=4; i>=0; i--)
    {
      pulse();
      if(bitRead(b, i))
      {
        Serial.print("1");
        delay(200);
      }
      else
      {
        Serial.print("0");
        delay(300);
      }
    }
    pulse();
    Serial.println();
  }
}

void pulse()
{
  Serial.print("_");
  PORTB |= 1<<PB5;       // sets pin13 high
  delay(200);
  PORTB &= ~(1<<PB5);    // sets pin13 low
}

void setMode(boolean newmode)
{
  mode = newmode;
  if(newmode == SYS2)
  {
    Serial.println("SYS2 Mode Enabled");
    sync = SYS2SYNC;
    logic0 = SYS2LOGIC0;
    logic1 = SYS2LOGIC1;
  }
  else
  {
    Serial.println("SYS4 Mode Enabled");
    sync = SYS4SYNC;
    logic0 = SYS4LOGIC0;
    logic1 = SYS4LOGIC1;
  }
}


