#define GPIO_ADDR 0177570

volatile unsigned int *gpio = (unsigned int *)GPIO_ADDR;

void delay()
{
  unsigned int count = 50000;
  while (count--)
  {
    asm volatile("nop"); // work?
  }
}

int main()
{
  while (1)
  {
    // 118 bytes
    // *gpio = !*gpio;
    // delay();

    // 112 bytes
    *gpio = *gpio ^ 1;
    delay();

    // 110 bytes
    // *gpio = 1; // LED ON
    // delay();

    // *gpio = 0; // LED OFF
    // delay();
  }
  return 0;
}
