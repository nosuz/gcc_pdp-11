    .macro push reg
        mov \reg, -(sp)
    .endm

    .macro pop reg
        mov  (sp)+, \reg
    .endm

    .globl start

    KWS  =  0177546
    VEC  =  0100      // interrupt vector
    PSW  =  0300    // br6

    LED  =  0177570
    FREQ = 29 // a half of power line frequency 60 Hz (29 = 60 / 2 - 1)

    .text
start:
    mov     $-020000, sp // in kernel mode

    // set interrupt vector and priority
    mov     $alarm, @$VEC
    mov     $PSW, @$VEC+2

    mov     $FREQ, @$CNTR // 60 Hz
    mov     $0100, @$KWS // $0x40 clear timeup and enable interrupt

loop:
    wait
    br loop

alarm:
    // save registers if required
    // R2-5 are saved by callee
    //push    r0
    //push    r1

    mov     $0100, @$KWS // optional
    dec     @$CNTR
    beq     timeup
    br      return

timeup:
    mov     $FREQ, @$CNTR

    mov     @$LED, r0
    bit     $1, r0  // check LED status
    bne     led_off // branch if set. Not equal 0

led_on:
    bis     $1, r0
    mov     r0, @$LED
    br      return

led_off:
    bic     $1, r0
    mov     r0, @$LED
    br      return

return:
    //pop     r1
    //pop     r0
    rti

    .data
CNTR:
    .word   0
    .end
