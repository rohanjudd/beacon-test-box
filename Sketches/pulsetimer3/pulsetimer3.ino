// Decodes IR Beacon signals
// Messages encoded by timing between pulses
// SYNC 4 3 2 1 0 SYNC
// Input: Pin D8 

volatile boolean first;
volatile boolean triggered;
volatile unsigned long overflowCount;
volatile unsigned long startTime;
volatile unsigned long finishTime;
volatile unsigned long timings[12];
volatile unsigned int count;

const int sys2sync = 15000;
const int sys2logic0 = 7500;
const int sys2logic1 = 5000;
const int tolerance = 10;

//readable values for debugging
const char* value_text[]={"0", "1", "s", "?"};

// timer overflows (every 65536 counts)
ISR (TIMER1_OVF_vect) 
{
  overflowCount++;
}  // end of TIMER1_OVF_vect

ISR (TIMER1_CAPT_vect)
{
  // grab counter value before it changes any more
  unsigned int timer1CounterValue;
  timer1CounterValue = ICR1;  // see datasheet, page 117 (accessing 16-bit registers)
  unsigned long overflowCopy = overflowCount;

  // if just missed an overflow
  if ((TIFR1 & bit (TOV1)) && timer1CounterValue < 0x7FFF)
    overflowCopy++;

  // wait until we noticed last one
  if (triggered)
    return;

  if (first)
  {
    startTime = (overflowCopy << 16) + timer1CounterValue;
    first = false;
    return;  
  }

  finishTime = (overflowCopy << 16) + timer1CounterValue;
  triggered = true;
  TIMSK1 = 0;    // no more interrupts for now
}

void prepareForInterrupts ()
{
  noInterrupts ();  // protected code
  first = true;
  triggered = false;  // re-arm for next time
  // reset Timer 1
  TCCR1A = 0;
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

void setup () 
{
  Serial.begin(115200);       
  Serial.println("Pulse Timer");
  // set up for interrupts
  prepareForInterrupts ();   
}

void loop () 
{
  // wait till we have a reading
  if (!triggered)
    return;

  unsigned long elapsedTime = finishTime - startTime;

  Serial.print(value_text[getPulseValue(elapsedTime)]);
  //Serial.print ("Pulse Gap: ");
  //Serial.print ((elapsedTime * 0.0625)); // each tick is 62.5 ns at 16 MHz
  //Serial.println (" us");

  delay (31);

  prepareForInterrupts ();   
}

byte getPulseValue(unsigned long ticks)
{
  byte val = 3;
  // 0 for logic 0
  // 1 for logic 1
  // 2 for sync
  // 3 for error
  if((ticks >= sys2sync - tolerance) && (ticks <= sys2sync + tolerance))
    val = 2;
  else
  {
    if((ticks >= sys2logic0 - tolerance) && (ticks <= sys2logic0 + tolerance))
      val = 0;
    else
    {
      if((ticks >= sys2logic1 - tolerance) && (ticks <= sys2logic1 + tolerance))
        val = 1; 
    }
  }

  return val;
}

