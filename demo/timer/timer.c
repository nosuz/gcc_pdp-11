#define GPIO_ADDR 0160004
#define TIMER_ADDR 0177546
#define TIMEUP 0x80
/*
bit 7: timeup
*/

#define POWER_FREQ 60

volatile unsigned int *gpio = (unsigned int *)GPIO_ADDR;
volatile unsigned int *timer = (unsigned int *)TIMER_ADDR;

void wait()
{
  for (int i = 0; i < (POWER_FREQ / 2); i++)
  {
    while (!(*timer & TIMEUP)) // wait timeup
    {
      asm volatile("nop"); // work?
    }
    // clear timeup
    *timer = *timer & ~TIMEUP;
  }
}

int main()
{
  // clear timeup
  *timer = *timer & ~TIMEUP;

  while (1)
  {
    *gpio = *gpio ^ 1;
    wait();
  }
  return 0;
}
