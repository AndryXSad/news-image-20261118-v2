#!/usr/bin/env python3
"""Write the v2 front-page image to the output path.

The entry image is the front page rendered for this repository
(entry.png) and this program copies it byte for byte to
/output/entry.png. Python 3.13 standard library only, no network,
fully deterministic: the same input bytes always produce the same
output bytes.
"""
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if os.path.getsize(src) > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
