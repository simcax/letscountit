"""Unit tests for the Let's Count IT project"""
import uuid
from types import ModuleType as MT
import pytest
import letscountit.base
from letscountit.base import Counterthing


def test_class_loads():  
    """Test it is possible to assign the class object"""
    base_obj = letscountit.base.Basecounting()
    
    all_obj = [k for k, v in globals().items() if type(v) is MT and not k.startswith('__')]
    ", ".join(all_obj)
    assert 'letscountit' in all_obj


def test_get_count_obj():
    """Test the uid is being assigned in the object"""
    uid = uuid.uuid4()
    counter_thing1 = Counterthing(uid)
    count_obj = counter_thing1
    assert count_obj.uuid == uid


def test_increase_counter_on_counterthing():
    """Test counting one up"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    count_obj.up()
    assert count_obj.count == 1


def test_increase_counter_with_ten_on_counterthing():
    """Test counting up 10 times"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    for i in range(10):
        count_obj.up()
    assert count_obj.count == 10


def test_increase_counter_with_ten_on_counterthing_by_number():
    """Test a counter increasing by 10"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    count_obj.up(10)
    assert count_obj.count == 10


def test_increase_counter_with_ten_on_counterthing_exception():
    """Test the counter will fail if given a string"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid)
    with pytest.raises(Exception):
        count_obj.up('a')

def test_inistialize_decreasing_counter():
    """Test is is possible to set a start count"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid, start_count=30)
    assert count_obj.count == 30

def test_decrease_counter():
    """Test initializing a counter and then decrease the counter"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid, start_count=30)
    count_obj.down()
    assert count_obj.count == 29

def test_decrease_non_integer_value_fails():
    """Test decreasing a counter with a string will fail"""
    uid = uuid.uuid4()
    count_obj = Counterthing(uid,30)
    with pytest.raises(Exception):
        count_obj.down('a')

