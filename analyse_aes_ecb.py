#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import hashlib
import math
from PIL import Image, ImageDraw

INPUT = Path("aes.bmp.enc")
BLOCK_SIZE = 16
MAP_WIDTH = 320
CELL_SIZE = 3

def colour_for_block(block: bytes) -> tuple[int, int, int]:
    """Stable artificial colour: same block -> same colour."""
    digest = hashlib.sha256(block).digest()
    # Keep colours visible, while remembering these are arbitrary labels.
    return tuple(55 + (b % 170) for b in digest[:3])

def main():
    if not INPUT.exists():
        raise SystemExit(
            f"Cannot find {INPUT.resolve()}\n"
            "Put this script in the same folder as aes.bmp.enc, then run it there."
        )

    data = INPUT.read_bytes()
    full_len = (len(data) // BLOCK_SIZE) * BLOCK_SIZE
    full_data = data[:full_len]
    trailing = data[full_len:]
    blocks = [
        full_data[i:i + BLOCK_SIZE]
        for i in range(0, len(full_data), BLOCK_SIZE)
    ]
    counts = Counter(blocks)

    lines = [
        "AES-ECB ciphertext block analysis (exploratory; not decryption)",
        f"Input file: {INPUT}",
        f"File size: {len(data)} bytes",
        f"Block size: {BLOCK_SIZE} bytes",
        f"Complete blocks: {len(blocks)}",
        f"Unique complete blocks: {len(counts)}",
        f"Repeated block types (count > 1): {sum(1 for n in counts.values() if n > 1)}",
        f"Most frequent block occurrences: {max(counts.values(), default=0)}",
        f"Trailing bytes outside complete blocks: {len(trailing)}",
        f"Trailing bytes (hex): {trailing.hex() or '(none)'}",
        "",
        "Top 10 most frequent blocks:",
    ]
    for block, n in counts.most_common(10):
        lines.append(f"{n:>8} occurrences  {block.hex()}")
    Path("block_analysis.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    rows = math.ceil(len(blocks) / MAP_WIDTH)
    image = Image.new("RGB", (MAP_WIDTH * CELL_SIZE, rows * CELL_SIZE), (245, 247, 250))
    draw = ImageDraw.Draw(image)
    for i, block in enumerate(blocks):
        x = (i % MAP_WIDTH) * CELL_SIZE
        y = (i // MAP_WIDTH) * CELL_SIZE
        draw.rectangle(
            [x, y, x + CELL_SIZE - 1, y + CELL_SIZE - 1],
            fill=colour_for_block(block)
        )
    image.save("block_identity_map.png")

    print("\n".join(lines))
    print("\nCreated block_analysis.txt")
    print("Created block_identity_map.png")
    print("\nReminder: the map visualises block identity only; it is not a recovered/decrypted BMP.")

if __name__ == "__main__":
    main()
