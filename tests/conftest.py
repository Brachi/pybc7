from dataclasses import dataclass

import pytest


@dataclass
class DDSSample:
    file_path: str = "tests/data/image-0001.dds"



@pytest.fixture
def dds_sample():
    # FIXME:  un-hardcode
    return DDSSample()
