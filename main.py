"""Entry point: place the finished front page where the harness expects it.

The newspaper image itself is produced by gen_frontpage_v2.py. This script
does not draw anything; it only copies the finished PNG into the output
directory and verifies the copy, so the submitted artefact is byte-identical
to the image in this repository.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1024 * 1024  # 1 MiB: harness limit for the output image


def _repo_file(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, name)


def _sha256_hex(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source = _repo_file("entry.png")
    destination = "/output/entry.png"

    if not os.path.isfile(source):
        print(f"missing source image: {source}", file=sys.stderr)
        return 1

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(
            f"source image too large: {size} bytes (limit {MAX_BYTES})",
            file=sys.stderr,
        )
        return 1

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copyfile(source, destination)

    # Integrity check: the copy must be byte-identical to the source image.
    if _sha256_hex(source) != _sha256_hex(destination):
        print("copy mismatch: destination differs from source", file=sys.stderr)
        return 1

    copied = os.path.getsize(destination)
    print(
        f"wrote {destination} ({copied} bytes, "
        f"sha256 {_sha256_hex(destination)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
