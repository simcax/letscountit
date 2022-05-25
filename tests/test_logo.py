import pytest
from letscountit.logo import Logo


def test_logo():
    logo_obj = Logo()
    assert len(logo_obj.logo) == 409
