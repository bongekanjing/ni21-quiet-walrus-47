#!/usr/bin/env python3
"""Publish entry.png to the output directory the grader gives the program.

The renderer writes entry.png at the repository root. This script re-checks the
file as the gate will read it - signature, every chunk's length and CRC walked
to IEND, no trailing bytes, the 1 MiB cap, and the pixel limit from IHDR - and
only then copies it to $MAKEFUN_OUTPUT_DIR. Nothing depends on the clock, the
network, or the hash seed, so two runs write identical bytes.
"""

import os
import pathlib
import shutil
import struct
import sys
import zlib

SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def walk(data):
    """Return (width, height) or raise ValueError naming the first fault."""
    if not data.startswith(SIG):
        raise ValueError("not a PNG: signature is %r" % data[:8])
    pos = len(SIG)
    first = True
    width = height = None
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header at %d" % pos)
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        end = pos + 8 + length
        if end + 4 > len(data):
            raise ValueError("chunk %r runs past the file" % ctype)
        body = data[pos + 8:end]
        (crc,) = struct.unpack(">I", data[end:end + 4])
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            raise ValueError("bad CRC on chunk %r" % ctype)
        if first:
            if ctype != b"IHDR" or length != 13:
                raise ValueError("first chunk is %r, not a 13-byte IHDR" % ctype)
            width, height = struct.unpack(">II", body[:8])
            first = False
        if ctype == b"IEND":
            seen_iend = True
            pos = end + 4
            break
        pos = end + 4
    if not seen_iend:
        raise ValueError("no IEND: the image is incomplete")
    if pos != len(data):
        raise ValueError("%d stray bytes after IEND" % (len(data) - pos))
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError("image is %dx%d, over the %d px limit" % (width, height, MAX_SIDE))
    return width, height


def main():
    here = pathlib.Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.exists():
        sys.exit("entry.png missing: run build/render.sh first")
    data = src.read_bytes()
    if len(data) > MAX_BYTES:
        sys.exit("entry.png is %d bytes, over the %d cap" % (len(data), MAX_BYTES))
    try:
        w, h = walk(data)
    except ValueError as exc:
        sys.exit("entry.png would fail the gate: %s" % exc)

    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    print("wrote %s: %d bytes, %dx%d" % (dst, len(data), w, h))


if __name__ == "__main__":
    main()
