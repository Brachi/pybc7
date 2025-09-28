import os

from PIL import Image
from tests.conftest import DATA_OUT_DIR

from pybc7 import unpack_dds


def test_decoding(dds_sample):
    file_path = os.path.join(dds_sample.file_dir, dds_sample.file_name)
    with open(file_path, "rb") as f:
        pixels = unpack_dds(
            f,
            dds_sample.width,
            dds_sample.height,
            dds_sample.format,
            128,
        )
        im = Image.frombytes("RGBA", (dds_sample.width, dds_sample.height), bytes(pixels))
        im.save(f"{os.path.join(DATA_OUT_DIR, dds_sample.file_name)}.png")


