# pybc7

⚠️
This is still rough
⚠️


Python bindings for [bc7enc_rdo](https://github.com/richgel999/bc7enc_rdo), a state of the art RDO BC1-7 GPU texture encoder library.

## Compiling

`./compile.sh`


## Usage


    from itertools import chain
    import struct

    from PIL import Image

    from pybc7 import decode_bc7, encode_bc7, DDS_FORMAT


    # Decoding
    with open("my.dds", "rb") as f:
        WIDTH, HEIGHT = 1024, 1024
        pixels = decode_bc7(f, WIDTH, HIGHT, DDS_FORMAT.DXT5)

        # Optionally save the image with Pillow
        im = Image.frombytes("RGBA", (WIDTH, HEIGHT), bytes(final_pixels))
        im.save(f'my.png')

    # Encoding
    rgba = struct.pack('64B', chain.from_iterable((255, 0, 0, 255) for _ in range(16))))
    bc7_params = bc7enc_compress_block_params_init()

    data_bytes = encode_bc7(rgba, bc7_params)

    # To see the result of the encoding decode back and save as png
    pixels = decode_bc7(f, WIDTH, HIGHT, DDS_FORMAT.DXT5)
    im = Image.frombytes("RGBA", (4, 4), bytes(pixels))
    im.save(rgba.png')
