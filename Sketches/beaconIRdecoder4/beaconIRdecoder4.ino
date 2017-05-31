// Decodes IR Beacon signals
// Messages encoded by timing between pulses
// SYNC 4 3 2 1 0 SYNC
// Input: Pin D8 
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

const int SYS2SYNC = 15000, SYS2LOGIC0 = 7500, SYS2LOGIC1 = 5000;

const int SYS4SYNC = 13732, SYS4LOGIC0 = 6866, SYS4LOGIC1 = 4577;

const int TOLERANCE = 100;

int sync, sync_l, sync_h, logic0, logic0_l, logic0_h, logic1, logic1_l, logic1_h;

const boolean SYS2 = false;
const boolean SYS4 = true;
boolean mode;

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

    if(!foundSync)
  {
    if(elapsedTime >= sync_l && elapsedTime <= sync_h)
    {
      foundSync = true;
    }
  }
  else
  {
    if(elapsedTime >= logic0_l && elapsedTime <= logic0_h)
    {
      bitWrite(data, index, 0);
      index--;
    }
    else
    {
      if(elapsedTime >= logic1_l && elapsedTime <= logic1_h)
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
    }
  }

  if(index < 0) // must have filled up all 5 bits
  {
    complete = true;
    TIMSK1 = 0;    // no more interrupts for now
  }
}

void prepareInterrupts()
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
  Serial.begin(115200);       
  Serial.println("IR Beacon Decoder");
  setMode(SYS2);
  prepareInterrupts ();  // set up for interrupts 
}

void loop() 
{
  if (!complete) // Wait until we have a good message
      return;
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
  prepareInterrupts();   
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
  sync_l = sync - TOLERANCE;
  sync_h = sync + TOLERANCE;
  logic0_l = logic0 - TOLERANCE;
  logic0_h = logic0 + TOLERANCE;
  logic1_l = logic1 - TOLERANCE;
  logic1_h = logic1 + TOLERANCE;
}


