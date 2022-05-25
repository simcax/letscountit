import pytest
import letscountit.base
from letscountit.base import Counterthing
import uuid


def test_class_loads():  
    x = letscountit.base.Basecounting()
    from types import ModuleType as MT
    all = [k for k, v in globals().items() if type(v) is MT and not k.startswith('__')]
    ", ".join(all)
    assert 'letscountit' in all


def test_get_count_obj():
    uid = uuid.uuid4()
    counterthing1 = Counterthing(uid)
    count_obj = counterthing1
    assert count_obj.uuid == uid


def test_increase_counter_on_counterthing():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    count_obj.up()
    assert count_obj.count == 1


def test_increase_counter_with_ten_on_counterthing():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    for i in range(10):
        count_obj.up()
    assert count_obj.count == 10


def test_increase_counter_with_ten_on_counterthing_by_number():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    count_obj.up(10)
    assert count_obj.count == 10


def test_increase_counter_with_ten_on_counterthing_exception():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    with pytest.raises(Exception):
        count_obj.up('a')

def test_inistialize_decreasing_counter():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid, startCount=30)
    assert count_obj.count == 30

def test_decrease_counter():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid, startCount=30)
    count_obj.down()
    assert count_obj.count == 29

def test_decrease_non_integer_value_fails():
    uid = uuid.uuid4()
    count_obj = Counterthing(uid,30)
    with pytest.raises(Exception):
        count_obj.down('a')