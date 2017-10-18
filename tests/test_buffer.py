import mock, boto3, logging, unittest
from moto import mock_cloudwatch

from fluentmetrics import BufferedFluentMetric, buffer

log = logging.getLogger('metric')
Metric = BufferedFluentMetric

def with_metric(*dimensions):
    def decorator(func):
        @mock_cloudwatch
        @mock.patch('fluentmetrics.buffer.PAGE_SIZE', 3)
        def wrapper(*args, **kwargs):
            cw = Dummy()
            m = Metric(cw)
            m.with_namespace('namespace')
            m.without_dimension('MetricStreamId') # probably should remove it entirely as a default
            for name, value in dimensions:
                m.with_dimension(name, value)
            kwargs['m'] = m
            kwargs['cw'] = cw
            func(*args, **kwargs)
        return wrapper
    return decorator
    
class TestBuffer(unittest.TestCase):
    @with_metric()
    def test_autoflush_exactly_one_page(self, m, cw):
        m.count(MetricName='counter', Value=1)
        m.count(MetricName='counter', Value=2)
        m.count(MetricName='counter', Value=3)

        assert len(cw.calls) == 1
        data = cw.calls[0]['MetricData']
        assert len(data) == 3
        values = [d['Value'] for d in data if d['MetricName'] == 'counter']
        self.assertSequenceEqual(values, [1, 2, 3])

    @with_metric()
    def test_autoflush_1_and_half_pages(self, m, cw):
        m.count(MetricName='counter', Value=1)
        m.count(MetricName='counter', Value=2)
        m.count(MetricName='counter', Value=3)
        assert len(m.buffers['namespace']) == 0
        m.count(MetricName='counter', Value=4)

        assert len(cw.calls) == 1
        data = cw.calls[0]['MetricData']
        assert len(data) == 3
        values = [d['Value'] for d in data if d['MetricName'] == 'counter']
        self.assertSequenceEqual(values, [1, 2, 3])

        m.flush()

        assert len(cw.calls) == 2
        data = cw.calls[1]['MetricData']
        assert len(data) == 1
        values = [d['Value'] for d in data if d['MetricName'] == 'counter']
        self.assertSequenceEqual(values, [4])

    @with_metric()
    def test_flush_3_pages(self, m, cw):
        # this should send 9 records for each count
        for dim in range(9):
            name = 'dim{}'.format(dim + 1)
            m.with_dimension(dim, dim)
        m.count(MetricName='counter', Value=1)

        assert len(cw.calls) == 3

        for i in range(3):
            data = cw.calls[i]['MetricData']
            assert len(data) == 3
            values = [d['Value'] for d in data if d['MetricName'] == 'counter']
            self.assertSequenceEqual(values, [1, 1, 1])


class Dummy(object):
    def __init__(self):
        self.calls = []

    def put_metric_data(self, **kwargs):
        self.calls.append(kwargs)
