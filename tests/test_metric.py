# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Licensed under the Amazon Software License (the "License"). You may not use
# this file except in compliance with the License. A copy of the License is
# located at

#    http://aws.amazon.com/asl/

# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or
# implied. See the License for the specific language governing permissions and
# limitations under the License.


import arrow
import time
from fluentmetrics import FluentMetric
import mock
from moto import mock_cloudwatch


@mock_cloudwatch
def test_setting_namespace_sets_namespace():
    test_value = 'test_namespace'
    m = FluentMetric()
    m.with_namespace(test_value)
    assert m.namespace == test_value


def test_adding_dimension_adds_dimension():
    test_name = 'test_name'
    test_value = 'test_value'
    m = FluentMetric()
    m.with_dimension(test_name, test_value)
    assert m.does_dimension_exist(test_name)


def test_removing_dimension_removes_dimension():
    test_name = 'test_name'
    test_value = 'test_value'
    m = FluentMetric()
    m.with_dimension(test_name, test_value)
    assert m.does_dimension_exist(test_name)
    m.without_dimension(test_name)
    assert not m.does_dimension_exist(test_name)


def test_dimension_does_not_duplicate():
    test_name = 'test_name'
    test_value1 = 'test_value1'
    test_value2 = 'test_value2'
    m = FluentMetric()
    m.with_dimension(test_name, test_value1)
    assert m.get_dimension_value(test_name) == test_value1
    m.with_dimension(test_name, test_value2)
    assert m.get_dimension_value(test_name) == test_value2


def test_adding_timer_starts_timer():
    name = 'test_timer'
    m = FluentMetric()
    m.with_timer(name)
    time.sleep(1)
    t = m.get_timer(name)
    assert t.start < arrow.utcnow()
    assert t.elapsed_in_ms() > 1000 and t.elapsed_in_ms() < 2000


def test_can_add_multiple_timers():
    name1 = 'test_timer_1'
    name2 = 'test_timer_2'
    m = FluentMetric()
    m.with_timer(name1)
    time.sleep(1)
    t = m.get_timer(name1)
    assert t.start < arrow.utcnow()
    assert t.elapsed_in_ms() > 1000 and t.elapsed_in_ms() < 2000

    m.with_timer(name2)
    time.sleep(1)
    u = m.get_timer(name2)
    assert u.start < arrow.utcnow()
    assert u.elapsed_in_ms() > 1000 and u.elapsed_in_ms() < 2000
    assert t.elapsed_in_ms() > 2000


def test_removing_timer_removes_timer():
    name = 'test_timer'
    m = FluentMetric()
    m.with_timer(name)
    time.sleep(1)
    t = m.get_timer(name)
    assert t.start < arrow.utcnow()
    assert t.elapsed_in_ms() > 1000 and t.elapsed_in_ms() < 2000
    m.without_timer(name)
    t = m.get_timer(name)
    assert not t


def test_can_push_dimensions():
    test_name = 'test_name'
    test_value = 'test_value'
    m = FluentMetric()
    m.with_dimension(test_name, test_value)
    assert m.does_dimension_exist(test_name)
    m.push_dimensions()
    assert len(m.dimensions) == 1
    m.pop_dimensions()
    assert len(m.dimensions) == 2


@mock.patch('fluentmetrics.FluentMetric.log')
def test_can_log_count(fm_log):
    m = FluentMetric().with_namespace('Performance')
    m.count(MetricName='test', Count=2)
    fm_log.assert_called()


def test_can_set_resolution():
    m = FluentMetric().with_namespace('Performance').with_storage_resolution(1)
    assert m.storage_resolution == 1
