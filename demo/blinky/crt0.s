.globl  start
.globl  _main

// GCC inserts automatically
.globl ___main
// The error message is
// undefined reference to `__main'.
// But it refers ___main as same as main.
// confirmed by
// pdp11-aout-nm blinky.o | grep __main

.text
start:
    mov     $-020000, sp

    // clear BSS section
    mov     $_sbss, r1
    mov     $_ebss, r0
    sub     r1, r0
    beq     done
loop:
    clrb    (r1)+
    sob     r0, loop
done:
    jsr     pc, _main
    halt

___main:
    rts pc

.end
