#!/usr/bin/env python3
"""Génère les icônes PNG pour la PWA"""
import struct, zlib, base64

def make_png(size, bg=(10,12,17), fg=(0,212,255)):
    """Crée un PNG simple avec logo LiveTV"""
    def write_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    # Header PNG
    sig = b'\x89PNG\r\n\x1a\n'

    # IHDR
    ihdr_data = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    ihdr = write_chunk(b'IHDR', ihdr_data)

    # Image data
    rows = []
    cx, cy = size // 2, size // 2
    r = size * 0.4

    for y in range(size):
        row = [0]  # filter byte
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5

            if dist < r * 0.95:
                # Background circle
                row.extend([20, 25, 40])
            else:
                row.extend(list(bg))

            # Draw a simple "play" triangle in the center
            # Triangle: roughly centered
            tx, ty = x - cx, y - cy
            in_triangle = (
                tx > -r * 0.25 and
                ty > -r * 0.3 and
                ty < r * 0.3 and
                tx < r * 0.3 - abs(ty) * 0.8
            )

            if dist < r * 0.95 and in_triangle:
                # Overwrite with accent color
                row[-3:] = list(fg)

        rows.append(bytes(row))

    raw = b''.join(rows)
    compressed = zlib.compress(raw)
    idat = write_chunk(b'IDAT', compressed)
    iend = write_chunk(b'IEND', b'')

    return sig + ihdr + idat + iend

import os
os.makedirs('icons', exist_ok=True)

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    png = make_png(size)
    with open(name, 'wb') as f:
        f.write(png)
    print(f'✅ {name} généré ({size}x{size})')

print('Icons générées !')
