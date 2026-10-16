
from pathlib import Path
from PIL import Image
from collections import Counter

data = Path("aes.bmp.enc").read_bytes()

WIDTH = 640
HEIGHT = 480
HEADER_SIZE = 54
BLOCK_SIZE = 16

print("File size:", len(data))
print("Expected 640x480 BMP size:", 54 + WIDTH * HEIGHT * 3)

# Test whether the file has the expected total size.
if len(data) != HEADER_SIZE + WIDTH * HEIGHT * 3:
    print("Size does not match a 640x480, 24-bit BMP.")
    print("Do not assume these dimensions are correct.")
else:
    print("Exact size match for 640x480, 24-bit BMP!")

# ECB ciphertext block visualization.
# 640 * 3 = 1920 bytes per row.
# 1920 / 16 = 120 AES blocks per row.
row_bytes = WIDTH * 3
blocks_per_row = row_bytes // BLOCK_SIZE
print("AES blocks per row:", blocks_per_row)

pixel_data = data[HEADER_SIZE:]
blocks = [
    pixel_data[i:i + BLOCK_SIZE]
    for i in range(0, len(pixel_data), BLOCK_SIZE)
]

counts = Counter(blocks)
print("Unique blocks:", len(counts))
print("Most common block:", counts.most_common(1)[0][1], "occurrences")

# Give each distinct ciphertext block a grayscale shade based on
# its frequency. This is a diagnostic map, NOT decrypted pixels.
def shade(block):
    frequency = counts[block] / len(blocks)
    return max(0, min(255, int(255 * frequency * 100)))

img = Image.new("L", (blocks_per_row, len(blocks) // blocks_per_row))
img.putdata([shade(b) for b in blocks])
img = img.resize((WIDTH, HEIGHT), Image.Resampling.NEAREST)
img.save("ecb_frequency_640x480.png")

print("Saved ecb_frequency_640x480.png")
