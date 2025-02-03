
from itertools import chain
import struct

from PIL import Image

from pybc7 import decode_dds

FIELDS = (
    "file_path",
    "width",
    "height"
)



def test_decoding(dds_sample):
    with open(dds_sample.file_path, "rb") as f:
        pixels = decode_dds(
            f,
            dds_sample.width,
            dds_sample.height,
            dds_sample.format
        )

        # Optionally save the image with Pillow
        im = Image.frombytes("RGBA", (WIDTH, HEIGHT), bytes(final_pixels))
        im.save(f'my.png')


