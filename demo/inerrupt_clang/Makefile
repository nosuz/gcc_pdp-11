TARGET = interrupt
SRC = $(TARGET).c crt0.s
CC = pdp11-aout-gcc
AS = pdp11-aout-as
LD = pdp11-aout-ld
CFLAGS = -Wall -O2 -I/usr/local/lib/gcc/pdp11-aout/14.2.0/include -ffreestanding
LDFLAGS = -T linker.ld

OBJ = $(SRC:.c=.o)
OBJ := $(OBJ:.s=.o)

.PHONY: all clean

all: $(TARGET).out $(TARGET).ptap

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.s
	$(AS) $< -o $@

$(TARGET).out: $(OBJ)
	$(LD) $(LDFLAGS) $^ -o $@

$(TARGET).ptap: $(TARGET).out
	python3 ../aout2abs.py $(TARGET).out

clean:
	rm -f $(OBJ) $(TARGET).out $(TARGET).ptap
