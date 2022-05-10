import pytest
import letscountit.base

def test_class_loads():  
    x = letscountit.base.basecounting()
    from types import ModuleType as MT
    all = [k for k,v in globals().items() if type(v) is MT and not k.startswith('__')]
    ", ".join(all)
    assert 'letscountit' in all