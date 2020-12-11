import sys
crc = 0
while True:
    ch = sys.stdin.read(1)
    if not ch:
        break
    crc ^= ord(ch) << 8
    for _ in range(8):
        crc = crc << 1 if (crc & 0x8000) == 0 else (crc << 1) ^ 0x8001
    crc &= 0xffff
print(format(crc, '04x'))