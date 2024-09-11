"""Unit tests for the Let's Count IT project"""

import uuid
from types import ModuleType as MT

import pytest

import letscountit.base
from letscountit.base import Counterthing


def test_class_loads():
    """Test it is possible to assign the class object"""
    letscountit.base.Basecounting()

    all_obj = [k for k, v in globals().items() if type(v) is MT and not k.startswith("__")]
    ", ".join(all_obj)
    assert "letscountit" in all_obj


def test_get_count_obj():
    """Test the uid is being assigned in the object"""
    counter_thing1 = Counterthing(name="my test counter")
    count_obj = counter_thing1
    assert isinstance(count_obj.uuid, uuid.UUID)


def test_increase_counter_on_counterthing():
    """Test counting one up"""
    count_obj = Counterthing(name="my test counter")
    count_obj.up()
    assert count_obj.count == 1


def test_increase_counter_with_ten_on_counterthing():
    """Test counting up 10 times"""
    count_obj = Counterthing(name="my test counter")
    for i in range(10):
        count_obj.up()
    assert count_obj.count == 10


def test_increase_counter_with_ten_on_counterthing_by_number():
    """Test a counter increasing by 10"""
    count_obj = Counterthing(name="my test counter")
    count_obj.up(10)
    assert count_obj.count == 10


def test_increase_counter_with_ten_on_counterthing_exception():
    """Test the counter will fail if given a string"""
    count_obj = Counterthing(name="my test counter")
    with pytest.raises(Exception):
        count_obj.up("a")


def test_inistialize_decreasing_counter():
    """Test is is possible to set a start count"""
    name = "some counter"
    count_obj = Counterthing(name=name, start_count=30)
    assert count_obj.count == 30
    assert count_obj.name == name


def test_decrease_counter():
    """Test initializing a counter and then decrease the counter"""
    uid = uuid.uuid4()
    name = "some counter"
    count_obj = Counterthing(name=name, uuid=uid, start_count=30)
    count_obj.down()
    assert count_obj.count == 29
    assert name == count_obj.name


def test_decrease_non_integer_value_fails():
    """Test decreasing a counter with a string will fail"""
    uid = uuid.uuid4()
    name = "some counter"
    count_obj = Counterthing(name=name, uuid=uid, start_count=30)
    with pytest.raises(Exception):
        count_obj.down("a")
