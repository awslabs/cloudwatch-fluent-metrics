# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

# Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

#    http://aws.amazon.com/asl/

# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License.


import logging
import arrow
import uuid
import boto3
import boto3.session

logger = logging.getLogger('metric')
logger.addHandler(logging.NullHandler())


class Timer(object):
    def __init__(self):
        self.start = arrow.utcnow()

    def elapsed(self):
        return arrow.utcnow() - self.start

    def elapsed_in_ms(self):
        return self.elapsed().total_seconds() * 1000

    def elapsed_in_seconds(self):
        return self.elapsed().total_seconds()


class FluentMetric(object):
    def __init__(self, **kwargs):
        self.stream_id = str(uuid.uuid4())
        self.dimensions = []
        self.timers = {}
        self.dimension_stack = []
        self.with_dimension('MetricStreamId', self.stream_id)
        profile = kwargs.get('Profile')
        if profile:
            session = boto3.session.Session(profile_name=profile)
            self.client = session.client('cloudwatch')
        else:
            self.client = boto3.client('cloudwatch')

    def with_stream_id(self, id):
        self.stream_id = id
        self.with_dimension('MetricStreamId', self.stream_id)
        return self

    def with_namespace(self, namespace):
        self.namespace = namespace
        return self

    def with_dimension(self, name, value):
        self.without_dimension(name)
        self.dimensions.append({'Name': name, 'Value': value})
        return self

    def without_dimension(self, name):
        if not self.does_dimension_exist(name):
            return
        self.dimensions = \
            [item for item in self.dimensions if not item['Name'] == name]
        return self

    def does_dimension_exist(self, name):
        d = [item for item in self.dimensions if item['Name'] == name]
        if d:
            return True
        else:
            return False

    def get_dimension_value(self, name):
        d = [item for item in self.dimensions if item['Name'] == name]
        if d:
            return d[0]['Value']
        else:
            return None

    def with_timer(self, timer):
        self.timers[timer] = Timer()
        return self

    def without_timer(self, timer):
        if timer in self.timers.keys():
            del self.timers[timer]
        return self

    def get_timer(self, timer):
        if timer in self.timers.keys():
            return self.timers[timer]
        else:
            return None

    def push_dimensions(self):
        self.dimension_stack.append(self.dimensions)
        self.dimensions = []
        self.with_stream_id(self.stream_id)
        return self

    def pop_dimensions(self):
        self.dimensions = self.dimension_stack.pop()
        return self

    def elapsed(self, **kwargs):
        tn = kwargs.get('TimerName')
        mn = kwargs.get('MetricName')
        if tn not in self.timers.keys():
            logger.warn('No timer named {}'.format(tn))
            return
        self.log(Value=self.timers[tn].elapsed_in_ms(),
                 Unit='Milliseconds',
                 MetricName=mn)
        return self

    def countsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Count/Second',
                 MetricName=mn)
        return self

    def tbitsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Terabits/Second',
                 MetricName=mn)
        return self

    def gbitsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Gigabits/Second',
                 MetricName=mn)
        return self

    def mbitsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Megabits/Second',
                 MetricName=mn)
        return self

    def kbitsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Kilobits/Second',
                 MetricName=mn)
        return self

    def bitsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Bits/Second',
                 MetricName=mn)
        return self

    def tbsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Terabytes/Second',
                 MetricName=mn)
        return self

    def gbsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Gigabytes/Second',
                 MetricName=mn)
        return self

    def mbsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Megabytes/Second',
                 MetricName=mn)
        return self

    def kbsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Kilobytes/Second',
                 MetricName=mn)
        return self

    def bsec(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Bytes/Second',
                 MetricName=mn)
        return self

    def pct(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Percent',
                 MetricName=mn)
        return self

    def tbits(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Terabits',
                 MetricName=mn)
        return self

    def gbits(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Gigabits',
                 MetricName=mn)
        return self

    def mbits(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Megabits',
                 MetricName=mn)
        return self

    def kbits(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Kilobits',
                 MetricName=mn)
        return self

    def bits(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Bits',
                 MetricName=mn)
        return self

    def tb(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Terabytes',
                 MetricName=mn)
        return self

    def gb(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Gigabytes',
                 MetricName=mn)
        return self

    def mb(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Megabytes',
                 MetricName=mn)
        return self

    def kb(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Kilobytes',
                 MetricName=mn)
        return self

    def bytes(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Bytes',
                 MetricName=mn)
        return self

    def milliseconds(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Microseconds',
                 MetricName=mn)
        return self

    def microseconds(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Microseconds',
                 MetricName=mn)
        return self

    def seconds(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Seconds',
                 MetricName=mn)
        return self

    def count(self, **kwargs):
        mn = kwargs.get('MetricName')
        count = kwargs.get('Value', 1)
        self.log(Value=count,
                 Unit='Count',
                 MetricName=mn)
        return self

    def log(self, **kwargs):
        ts = kwargs.get('TimeStamp', arrow.utcnow()
                        .format('YYYY-MM-DD HH:mm:ss ZZ'))
        value = str(float(kwargs.get('Value')))
        unit = kwargs.get('Unit')
        md = []
        for dimension in self.dimensions:
            md.append({
                        'MetricName': kwargs.get('MetricName'),
                        'Dimensions': [dimension],
                        'Timestamp': ts,
                        'Value': value,
                        'Unit': unit

                    }
            )

        md.append({
                    'MetricName': kwargs.get('MetricName'),
                    'Dimensions': self.dimensions,
                    'Timestamp': ts,
                    'Value': value,
                    'Unit': unit
                  })

        logger.debug('log: {}'.format(md))
        self.client.put_metric_data(
                Namespace=self.namespace,
                MetricData=md
        )
        return self

    def get_metrics(self, **kwargs):
        mn = kwargs.get('MetricName')
        return self.client.list_metrics(Namespace=self.namespace,
                                        MetricName=mn)['Metrics']
