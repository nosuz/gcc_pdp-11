import sys
import struct

O_MAGIC = 0o407  # a.out magic number for PDP-11


def parse_absolute_loader(file_path):
    with open(file_path, "rb") as f:
        header = f.read(6)
        marker, reserved, size, entry = struct.unpack("<BBHH", header)

        data_size = size - 6  # Exclude header size

        print(f"Format: Absolute Loader")
        print(f"Size: {data_size} bytes")
        print(f"Entry address: {entry:06o}")

        data = f.read(data_size)
        if len(data) != data_size:
            print("Insufficient data.")
            return

        for i in range(0, data_size, 2):
            if i + 1 < data_size:
                word = struct.unpack("<H", data[i:i+2])[0]
                addr = entry + (i // 2) * 2
                print(f"{addr:06o} {word:06o}")
            else:
                print("Warning: Size is odd, and the last byte has been ignored.")


def parse_aout(file_path):
    header_format = "<HHHHHHHH"
    header_size = struct.calcsize(header_format)

    with open(file_path, "rb") as f:
        header_data = f.read(header_size)
        magic, text_size, data_size, bss_size, syms_size, entry, tr_size, dr_size = struct.unpack(
            header_format, header_data)

        if magic != O_MAGIC:
            raise ValueError("Unexpected file format")

        print(f"Format: a.out")
        print(f"Text size: {text_size} bytes")
        print(f"Data size: {data_size} bytes")
        print(f"Entry address: {entry:06o}")

        exec_data = f.read(text_size + data_size)
        for i in range(0, len(exec_data), 2):
            if i + 1 < len(exec_data):
                word = struct.unpack("<H", exec_data[i:i+2])[0]
                addr = entry + i
                print(f"{addr:06o} {word:06o}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bin2dump.py <input_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "rb") as f:
            magic_check = f.read(2)
            if struct.unpack("<H", magic_check)[0] == O_MAGIC:
                parse_aout(file_path)
            else:
                parse_absolute_loader(file_path)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)
