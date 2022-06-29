#!/usr/bin/env python3
import json
import os
import random
import shutil
import sys
from typing import Dict, Sequence

from PIL import Image


def main(inp: Dict[str, str], argv: Sequence[str] = ()) -> None:
    data_object_path = inp["data_object"]
    annotation_path = inp["annotation"]
    output_dir = inp["output_dir"]
    transform_name = inp["transform_name"]

    transform_args = [int(x) for x in argv[1:]]
    if len(transform_args) > 3:
        print(
            "ERROR: Too many args\n"
            "usage: random_rotate.py [ [start] stop [step] ]",
            file=sys.stderr,
        )
        sys.exit(1)
    if not transform_args:
        transform_args = [360]
    degrees = random.randrange(*transform_args)
    orig_image = Image.open(data_object_path)
    file_name_base, ext = os.path.splitext(os.path.basename(data_object_path))
    if ext.lstrip("."):
        fmt = None
    else:
        fmt = orig_image.format or "PNG"
        ext = ""

    str_args = "-".join(map(str, transform_args))
    new_image = orig_image.rotate(degrees)
    file_name_base = f"{file_name_base}-{transform_name}-{str_args}".replace(
        ".",
        "-",
    )
    obj_file_path = os.path.join(output_dir, f"{file_name_base}{ext}")
    annot_file_path = os.path.join(output_dir, f"{file_name_base}.json")
    new_image.save(obj_file_path, format=fmt)
    shutil.copy2(annotation_path, annot_file_path)


if __name__ == "__main__":
    main(json.loads(sys.stdin.read()), sys.argv)
