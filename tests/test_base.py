import pytest
import letscountit.base
from letscountit.base import counterthing
import uuid

def test_class_loads():  
    x = letscountit.base.basecounting()
    from types import ModuleType as MT
    all = [k for k,v in globals().items() if type(v) is MT and not k.startswith('__')]
    ", ".join(all)
    assert 'letscountit' in all

def test_get_count_obj():
    uid = uuid.uuid4()
    count_obj = counterthing(uid)
    assert count_obj.uuid == uid

def test_increase_counter_on_counterthing():
    uid = uuid.uuid4()
    count_obj = counterthing(uid)
    count_obj.up()
    assert count_obj.count == 1

def test_increase_counter_with_ten_on_counterthing():
    uid = uuid.uuid4()
    count_obj = counterthing(uid)
    for i in range(10):
        count_obj.up()
    assert count_obj.count == 10

def test_increase_counter_with_ten_on_counterthing():
    uid = uuid.uuid4()
    count_obj = counterthing(uid)
    count_obj.up(10)
    assert count_obj.count == 10

def test_increase_counter_with_ten_on_counterthing():
    uid = uuid.uuid4()
    count_obj = counterthing(uid)
    with pytest.raises(Exception):
        count_obj.up('a')
