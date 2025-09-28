# pybc7

⚠️
This is a work in progress
⚠️


Python bindings for [bc7enc_rdo](https://github.com/richgel999/bc7enc_rdo), a state of the art RDO BC1-7 GPU texture encoder library.

## Development

CMake is required to build the bc7enc as a shared library.

```
# Development
pip install -e .[tests]

# Build wheel for the current platform (only Windows and Linux supported (64))
pip wheel
# or using build, which will provide a more verbose output
python -m build --wheel

# Running tests
pytest
```


## Usage


The API for now focus on cases for unpacking the dds data where no header might be present, hence the need to specify width, height and format
I

```
from PIL import Image  # Optional
from pybc7 import unpack_dds

# Decoding

with open("/path/to/image.dds", "rb") as f:
    pixels = unpack_dds(
        f,
        1024, # width
        1024, # height
        "DXT1", # format -> DXT1 or BC7
        128,  # Start of DDS Data, always 128 except when using the optional struct DDS_HEADER_DXT10
    )
    # Use the raw pixels to create a png image
    im = Image.frombytes("RGBA", (1024, 1024), bytes(pixels))
    im.save("/path/to/image.png")

# Encoding
TODO
```
