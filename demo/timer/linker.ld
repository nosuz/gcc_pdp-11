ENTRY(start)

MEMORY
{
  RAM    (xrw)    : ORIGIN = 0400,   LENGTH = 4088K
}

SECTIONS
{
  .text :
  {
     crt0.o(.text)
    *(.text)
    . = ALIGN(2);
  } >RAM

  .data :
  {
    *(.data)
    . = ALIGN(2);
  } >RAM

  .bss :
  {
    _sbss = .;
    *(.bss)
    . = ALIGN(2);
    _ebss = .;
  } >RAM
}
