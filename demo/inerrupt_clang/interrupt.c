#pragma GCC diagnostic ignored "-Warray-bounds"

#include <stdint.h>

extern void interrupt_wrapper(void);

#define LED_ADDR ((volatile uint16_t *)0177570)
#define KW11_ADDR ((volatile uint16_t *)0777546)
#define INTERRUPT_VECTOR_ADDR 0100
#define POWER_FREQ_PRESCALE 60 / 2 - 1

#include <stdint.h>

typedef struct
{
  uint16_t address;
  uint16_t psw;
} InterruptVector;

volatile uint8_t led_prescale = POWER_FREQ_PRESCALE;

// called from crt0.s
void interrupt_handler(void)
{
  *KW11_ADDR = 0100; // optional
  if (led_prescale == 0)
  {
    *LED_ADDR ^= 1; // toggle LED
    led_prescale = POWER_FREQ_PRESCALE;
  }
  else
  {
    led_prescale--;
  }
}

void setup_interrupt(void)
{
  InterruptVector *vec = (InterruptVector *)INTERRUPT_VECTOR_ADDR;
  vec->address = (uint16_t)(uintptr_t)interrupt_wrapper;
  vec->psw = 0300; // br6

  // enable interrupt
  *KW11_ADDR = 0100;
}

int main(void)
{
  setup_interrupt();

  while (1)
  {
    __asm__("wait"); // block until interrupt
  }

  return 0;
}
