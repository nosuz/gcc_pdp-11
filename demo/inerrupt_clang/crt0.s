    .macro push reg
        mov \reg, -(sp)
    .endm

    .macro pop reg
        mov  (sp)+, \reg
    .endm

    .globl  start
    .globl  _main

    // GCC inserts automatically
    .globl ___main
    // The error message is
    // undefined reference to `__main'.
    // But it refers ___main as same as main.
    // confirmed by
    // pdp11-aout-nm blinky.o | grep __main

    .global _interrupt_wrapper

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
    rts     pc

_interrupt_wrapper:
    // save registers if required
    // R2-5 are saved by callee
    //push    r0
    //push    r1

    jsr     pc, _interrupt_handler

    //pop     r1
    //pop     r0

    rti

    .end
