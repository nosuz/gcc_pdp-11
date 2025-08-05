import sys
import os
import re

# convert ODT output to dump by sed
# sed -n 's/^@*\([0-9]*\)\/\([0-9]*\)$/\1 \2/p' odt.txt > dump.txt

# convert from an Absolute loader formatted file
# python3 abs2dump.py ABS_FILE | python3 dump2bootstrap.py OUTPUT_FILE_BASE


def convert_oct_file(input_file, output_base_name):
    output_text_file = output_base_name + ".dump"
    output_bin_file = output_base_name + ".bin"

    # Read lines from the input file or stdin
    if input_file:
        with open(input_file, "r") as infile:
            lines = infile.readlines()
    else:
        lines = sys.stdin.readlines()

    with open(output_text_file, "w") as outfile, open(output_bin_file, "wb") as binfile:
        block = []
        mask = [1] * 32  # Initialize with 1 (no data)
        start_addr = None
        block_start_addr = None
        data_positions = []

        for line in lines:
            # Skip comments, empty lines, and lines not starting with a digit
            if re.match(r'^[^0-9]', line) or re.match(r'^\s*#|^\s*\/\/|^\s*$', line):
                continue

            parts = line.split()
            if len(parts) < 2:
                continue
            addr = int(parts[0], 8)  # Convert address from octal to integer
            data = int(parts[1], 8)  # Convert data from octal to integer

            if start_addr is None:
                start_addr = addr  # Set the first address as a boot address

            # Split 16-bit data into low and high bytes
            low_byte = data & 0xFF
            high_byte = (data >> 8) & 0xFF

            if block_start_addr is None:
                block_start_addr = addr & ~0x1F  # Align to 32-byte boundary

            # Fill gaps with zeros
            while block_start_addr + len(block) < addr:
                block.append(0)
                data_positions.append(1)  # 1 = no data

            block.append(low_byte)
            block.append(high_byte)
            data_positions.append(0)  # 0 = data present
            data_positions.append(0)

            if len(block) == 32:
                # Create mask data
                mask = [sum((data_positions[i + j] << j)
                            for j in range(8)) for i in range(0, 32, 8)]

                # Split address into low and high bytes
                addr_low = start_addr & 0xFF
                addr_high = (start_addr >> 8) & 0xFF

                # Write to the text file
                outfile.write(f"{addr_low:02X} {addr_high:02X}\n")
                outfile.write(" ".join(f"{b:02X}" for b in block) + "\n")
                outfile.write(" ".join(f"{m:02X}" for m in mask) + "\n")

                # Write to the binary file
                binfile.write(bytes([addr_low, addr_high]))
                binfile.write(bytes(block))
                binfile.write(bytes(mask))

                # Start next block
                block = []
                data_positions = []
                block_start_addr += 32
                start_addr = None

        # Process remaining data
        if block:
            while len(block) < 32:
                block.append(0)
                data_positions.append(1)

            mask = [sum((data_positions[i + j] << j)
                        for j in range(8)) for i in range(0, 32, 8)]
            addr_low = block_start_addr & 0xFF
            addr_high = (block_start_addr >> 8) & 0xFF

            outfile.write(f"{addr_low:02X} {addr_high:02X}\n")
            outfile.write(" ".join(f"{b:02X}" for b in block) + "\n")
            outfile.write(" ".join(f"{m:02X}" for m in mask) + "\n")

            binfile.write(bytes([addr_low, addr_high]))
            binfile.write(bytes(block))
            binfile.write(bytes(mask))


if __name__ == "__main__":
    if len(sys.argv) == 2 and not sys.stdin.isatty():
        # Input from stdin, output to specified base name
        convert_oct_file(None, sys.argv[1])
    elif len(sys.argv) == 2:
        # Input from specified file
        convert_oct_file(sys.argv[1], os.path.splitext(sys.argv[1])[0])
    else:
        print("Usage: python3 dump2bootstrap.py <input_file> or use stdin with <output_base_name>")
        sys.exit(1)
