// Interface for Testing IR Timing Beacons     RJ Feb 2017
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

const boolean SYS2 = false, SYS4 = true;
const int SYS2SYNC = 938, SYS2LOGIC0 = 469, SYS2LOGIC1 = 313;
const int SYS4SYNC = 858, SYS4LOGIC0 = 429, SYS4LOGIC1 = 286;
const int TOLERANCE = 8, PULSE_WIDTH = 3;
const int REPEAT = 250;
const int PB5 = 5;

int sync, sync_l, sync_h, logic0, logic0_l, logic0_h, logic1, logic1_l, logic1_h;

int outPin = 13;
boolean mode, split;

volatile boolean first, foundSync, complete;
volatile unsigned long overflowCount, startTime, elapsedTime, finishTime;
volatile byte data;
volatile int index;

ISR (TIMER1_OVF_vect) // timer overflows (every 65536 counts)
{
  overflowCount++;
}

ISR (TIMER1_CAPT_vect)
{
  unsigned int timer1CounterValue = ICR1;  // Grab counter value
  unsigned long overflowCopy = overflowCount;

  if ((TIFR1 & bit (TOV1)) && timer1CounterValue < 0x7FFF) // if just missed an overflow
    overflowCopy++;

  if (complete) // wait until we noticed last one
      return;

  if (first)
  {
    startTime = (overflowCopy << 16) + timer1CounterValue;
    first = false;
    return;  
  }

  finishTime = (overflowCopy << 16) + timer1CounterValue;
  elapsedTime = finishTime - startTime;
  startTime = finishTime; // restart counting for next edge

    if(!foundSync) && (elapsedTime >= sync_l && elapsedTime <= sync_h)
    foundSync = true;
  else if(elapsedTime >= logic0_l && elapsedTime <= logic0_h)
  {
    bitWrite(data, index, 0);
    index--;
  }
  else if(elapsedTime >= logic1_l && elapsedTime <= logic1_h)
  {
    bitWrite(data, index, 1);
    index--;
  }
  else //found error need to start again
  {
    data = 0;
    foundSync = false;
    index = 4;
  }

  if(index < 0) // must have filled up all 5 bits
  {
    complete = true;
    TIMSK1 = 0;    // no more interrupts for now
  }
}

void setRXinterrupt()
{
  noInterrupts();  // protected code
  index = 4;
  complete = false;  // re-arm for next time
  first = true;
  data = 0;
  foundSync = false;

  TCCR1A = 0;  // reset Timer 1
  TCCR1B = 0;

  TIFR1 = bit (ICF1) | bit (TOV1);  // clear flags so we don't get a bogus interrupt
  TCNT1 = 0;          // Counter to zero
  overflowCount = 0;  // Therefore no overflows yet

  // Timer 1 - counts clock pulses
  TIMSK1 = bit (TOIE1) | bit (ICIE1);   // interrupt on Timer 1 overflow and input capture
  // start Timer 1, no prescaler
  TCCR1B =  bit (CS10) | bit (ICES1);  // plus Input Capture Edge Select (rising on D8)
  interrupts ();
}

void setup() 
{
  pinMode(outPin, OUTPUT); 
  Serial.begin(115200);       
  setMode(SYS2);
  splitMode(split);
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
    if(ser == 's')
    {
      splitMode(!split);
    }
    if(ser == 'l')
    {
      Serial.println("Transmitting all codes in sequence");
      for(int v=0; v<32; v++)
      {
        transmit(v, REPEAT);
      }
    }
    if(ser == 'r')
    {
      Serial.println("Recieving press any key to stop");
      recieve();
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
  sync_l =   (sync   - TOLERANCE) * 16;
  sync_h =   (sync   + TOLERANCE) * 16;
  logic0_l = (logic0 - TOLERANCE) * 16;
  logic0_h = (logic0 + TOLERANCE) * 16;
  logic1_l = (logic1 - TOLERANCE) * 16;
  logic1_h = (logic1 - TOLERANCE) * 16;
}

void splitMode(boolean newmode)
{
  split = newmode;
  if(split)
    Serial.println("Split Mode Enabled");
  else
    Serial.println("Split Mode Disabled");
}

void transmit(byte b, int repeat)
{
  Serial.println(b, HEX);
  for(int x=0; x<repeat; x++)
  {
    if(x==0)
      pulse();
    delayMicroseconds(sync);
    for(int i=4; i>=0; i--)
    {
      pulse();
      if(bitRead(b, i))
        delayMicroseconds(logic1);
      else
        delayMicroseconds(logic0);
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

void recieve()
{
  setRXinterrupt ();  // set up for interrupts 
  while (!Serial.available()) 
  {  
    if (complete) // We have a good message
    {
      if(data > 0x0F) // Must be a split
      {
        data = data - 0x10;
        Serial.print(data, HEX);
        Serial.println(" - SPLIT");
      }
      else
      {
        Serial.println(data, HEX);
      }
      delay (100);
      setRXinterrupt ();  // set up for the next one
    }
  }
}

void printMenu()
{
  Serial.println("IR Beacon Tester -RJ FEB17")  
}




