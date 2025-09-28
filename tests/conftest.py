import os
from dataclasses import dataclass

import pytest

DATA_DIR = "tests/data"
DATA_OUT_DIR = "tests-output"


@dataclass
class DDSSample:
    file_dir: str
    file_name: str
    width: int
    height: int
    format: str


DATA = [
    DDSSample(
        DATA_DIR,
        "cameraman-BC1-NOMIPS.dds",
        256, 256, "DXT1"
    )
]

@pytest.fixture(params=DATA)
def dds_sample(request):
    return request.param


def pytest_sessionstart():
    try:
        os.mkdir(DATA_OUT_DIR)
    except FileExistsError:
        pass

