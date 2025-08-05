import sys
import os
import struct

O_MAGIC = 0o407


def parse_aout_header(file):

    header_format = "<HHHHHHHH"  # a.out header has 8 fields
    header_size = struct.calcsize(header_format)

    with open(file, "rb") as f:
        header_data = f.read(header_size)
        magic, text_size, data_size, bss_size, syms_size, entry, tr_size, dr_size = struct.unpack(
            header_format, header_data)
        # print(struct.unpack(header_format, header_data))
        if magic != O_MAGIC:
            raise ValueError("Unexpected file format")
        exec_data = f.read(text_size + data_size)

    return entry, exec_data


def convert_to_abs(aout_file, abs_file):
    entry, exec_data = parse_aout_header(aout_file)
    size = len(exec_data)

    size = len(exec_data) + 6  # 6: absolute loader file's header size
    checksum_data = (0x01 + 0x00 + (size & 0xFF) + (size >> 8) +
                     (entry & 0xFF) + (entry >> 8) + sum(exec_data)) & 0xFF
    checksum_data = (checksum_data ^ 0xFF) + 1  # 2の補数

    # block for the entry point
    entry_point = [0x01, 0x00, 0x06, 0x00, (entry & 0xFF), (entry >> 8)]
    checksum_entry = ((sum(entry_point) & 0xFF) ^ 0xFF) + 1

    with open(abs_file, "wb") as f:
        # Absolute Loader format: [0x01, 0x00, size_lo, size_hi, address_lo, address_hi, data..., checksum]
        f.write(struct.pack("<BBHH", 0x01, 0x00, size, entry))
        f.write(exec_data)
        f.write(struct.pack("<B", checksum_data))

        # entry point block
        f.write(bytes(entry_point))
        f.write(struct.pack("<B", checksum_entry))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    aout_file = sys.argv[1]
    if not os.path.isfile(aout_file):
        print(f"Error: File '{aout_file}' not found.")
        sys.exit(1)

    abs_file = os.path.splitext(aout_file)[0] + ".ptap"
    convert_to_abs(aout_file, abs_file)
    print(f"Converted {aout_file} -> {abs_file}")
